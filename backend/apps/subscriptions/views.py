from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription
from .serializers import (
    SubscriptionPlanSerializer,
    SubscriptionPlanListSerializer,
    UserSubscriptionSerializer,
    UserSubscriptionListSerializer,
    UserSubscriptionDetailSerializer,
)
from apps.accounts.permissions import IsAdmin, IsSubscriptionOwnerOrAdmin


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SubscriptionPlan model with CRUD operations.
    Only admins can create, update, or delete plans.
    All authenticated users can view active plans.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return SubscriptionPlanListSerializer
        elif self.action == 'retrieve':
            return SubscriptionPlanSerializer
        return SubscriptionPlanSerializer

    def get_queryset(self):
        """
        Return queryset of subscription plans.
        Regular users see only active plans, admins see all.
        """
        queryset = SubscriptionPlan.objects.all()
        
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('plan_type', 'name')

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new subscription plan.
        Only admins can create plans.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        plan = serializer.save()
        
        response_serializer = SubscriptionPlanSerializer(plan)
        return Response(
            {
                'message': _('Subscription plan created successfully.'),
                'plan': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update subscription plan information.
        Only admins can update plans.
        """
        plan = self.get_object()
        serializer = self.get_serializer(plan, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_serializer = SubscriptionPlanSerializer(plan)
        return Response(
            {
                'message': _('Subscription plan updated successfully.'),
                'plan': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update subscription plan information.
        Only admins can update plans.
        """
        plan = self.get_object()
        serializer = self.get_serializer(plan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_serializer = SubscriptionPlanSerializer(plan)
        return Response(
            {
                'message': _('Subscription plan updated successfully.'),
                'plan': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete subscription plan.
        Only admins can delete plans.
        """
        plan = self.get_object()
        plan.delete()
        
        return Response(
            {'message': _('Subscription plan deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def active(self, request):
        """
        Get all active subscription plans.
        """
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('plan_type', 'name')
        
        page = self.paginate_queryset(plans)
        
        if page is not None:
            serializer = SubscriptionPlanListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = SubscriptionPlanListSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserSubscription model with CRUD operations.
    Users can view their own subscriptions.
    Admins can view and manage all subscriptions.
    """
    permission_classes = [IsSubscriptionOwnerOrAdmin]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return UserSubscriptionListSerializer
        elif self.action == 'retrieve':
            return UserSubscriptionDetailSerializer
        return UserSubscriptionSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        Users can only see their own subscriptions.
        """
        queryset = UserSubscription.objects.select_related('user', 'plan')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        
        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'cancel']:
            return [IsAdmin()]
        return [IsSubscriptionOwnerOrAdmin()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new user subscription.
        Only admins can create subscriptions.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data.get('user')
        plan = serializer.validated_data.get('plan')
        start_date = serializer.validated_data.get('start_date', timezone.now().date())
        
        if not serializer.validated_data.get('end_date'):
            end_date = start_date + timedelta(days=plan.duration_days)
            serializer.validated_data['end_date'] = end_date
        
        subscription = serializer.save()
        
        response_serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(
            {
                'message': _('User subscription created successfully.'),
                'subscription': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve subscription details.
        Permission is handled by IsSubscriptionOwnerOrAdmin permission class.
        """
        subscription = self.get_object()
        self.check_object_permissions(request, subscription)
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update subscription information.
        Only admins can update subscriptions.
        """
        subscription = self.get_object()
        serializer = self.get_serializer(subscription, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        plan = serializer.validated_data.get('plan', subscription.plan)
        start_date = serializer.validated_data.get('start_date', subscription.start_date)
        
        if 'end_date' not in serializer.validated_data:
            end_date = start_date + timedelta(days=plan.duration_days)
            serializer.validated_data['end_date'] = end_date
        
        serializer.save()
        
        response_serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(
            {
                'message': _('Subscription updated successfully.'),
                'subscription': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update subscription information.
        Only admins can update subscriptions.
        """
        subscription = self.get_object()
        serializer = self.get_serializer(subscription, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        plan = serializer.validated_data.get('plan', subscription.plan)
        start_date = serializer.validated_data.get('start_date', subscription.start_date)
        
        if 'end_date' not in serializer.validated_data and 'start_date' in serializer.validated_data:
            end_date = start_date + timedelta(days=plan.duration_days)
            serializer.validated_data['end_date'] = end_date
        
        serializer.save()
        
        response_serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(
            {
                'message': _('Subscription updated successfully.'),
                'subscription': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete subscription.
        Only admins can delete subscriptions.
        """
        subscription = self.get_object()
        subscription.delete()
        
        return Response(
            {'message': _('Subscription deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscription(self, request):
        """
        Get current user's active subscription.
        """
        subscription = UserSubscription.objects.filter(
            user=request.user,
            is_active=True,
            status='active'
        ).select_related('user', 'plan').first()
        
        if not subscription:
            return Response(
                {'detail': _('No active subscription found.')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current(self, request):
        """
        Get current user's subscription (active or most recent).
        """
        subscription = UserSubscription.objects.filter(
            user=request.user
        ).select_related('user', 'plan').order_by('-start_date', '-created_at').first()
        
        if not subscription:
            return Response(
                {'detail': _('No subscription found.')},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdmin],
        url_path='cancel'
    )
    def cancel(self, request, pk=None):
        """
        Cancel a subscription.
        Only admins can cancel subscriptions.
        """
        subscription = self.get_object()
        
        if subscription.status == 'cancelled':
            return Response(
                {'detail': _('Subscription is already cancelled.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.cancel()
        
        serializer = UserSubscriptionDetailSerializer(subscription)
        return Response(
            {
                'message': _('Subscription cancelled successfully.'),
                'subscription': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscriptions(self, request):
        """
        Get all subscriptions for current user.
        """
        subscriptions = UserSubscription.objects.filter(
            user=request.user
        ).select_related('user', 'plan').order_by('-start_date', '-created_at')
        
        page = self.paginate_queryset(subscriptions)
        
        if page is not None:
            serializer = UserSubscriptionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserSubscriptionListSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
