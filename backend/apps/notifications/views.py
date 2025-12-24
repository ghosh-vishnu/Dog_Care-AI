from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Notification
from apps.accounts.permissions import IsAdmin, IsNotificationOwnerOrAdmin


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification model with CRUD operations.
    Users can only access their own notifications.
    Admins can access all notifications.
    """
    permission_classes = [IsNotificationOwnerOrAdmin]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        from .serializers import (
            NotificationSerializer,
            NotificationListSerializer,
            NotificationDetailSerializer,
        )
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'retrieve':
            return NotificationDetailSerializer
        return NotificationSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        Users can only see their own notifications.
        """
        queryset = Notification.objects.select_related('user')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        
        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsNotificationOwnerOrAdmin()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new notification.
        Only admins can create notifications.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification = serializer.save()
        
        from .serializers import NotificationDetailSerializer
        response_serializer = NotificationDetailSerializer(notification)
        return Response(
            {
                'message': _('Notification created successfully.'),
                'notification': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve notification details.
        Permission is handled by IsNotificationOwnerOrAdmin permission class.
        """
        notification = self.get_object()
        self.check_object_permissions(request, notification)
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update notification information.
        Only admins can update notifications.
        """
        notification = self.get_object()
        self.check_object_permissions(request, notification)
        
        serializer = self.get_serializer(notification, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        from .serializers import NotificationDetailSerializer
        response_serializer = NotificationDetailSerializer(notification)
        return Response(
            {
                'message': _('Notification updated successfully.'),
                'notification': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update notification information.
        Only admins can update notifications.
        """
        notification = self.get_object()
        self.check_object_permissions(request, notification)
        
        serializer = self.get_serializer(notification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        from .serializers import NotificationDetailSerializer
        response_serializer = NotificationDetailSerializer(notification)
        return Response(
            {
                'message': _('Notification updated successfully.'),
                'notification': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete notification.
        Permission is handled by IsNotificationOwnerOrAdmin permission class.
        """
        notification = self.get_object()
        self.check_object_permissions(request, notification)
        
        notification.delete()
        
        return Response(
            {'message': _('Notification deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_notifications(self, request):
        """
        Get all notifications for current user.
        """
        notifications = Notification.objects.filter(
            user=request.user
        ).select_related('user')
        
        page = self.paginate_queryset(notifications)
        
        if page is not None:
            from .serializers import NotificationListSerializer
            serializer = NotificationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        from .serializers import NotificationListSerializer
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread(self, request):
        """
        Get all unread notifications for current user.
        """
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).select_related('user')
        
        page = self.paginate_queryset(notifications)
        
        if page is not None:
            from .serializers import NotificationListSerializer
            serializer = NotificationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        from .serializers import NotificationListSerializer
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsNotificationOwnerOrAdmin],
        url_path='mark-read'
    )
    def mark_read(self, request, pk=None):
        """
        Mark notification as read.
        """
        notification = self.get_object()
        self.check_object_permissions(request, notification)
        
        notification.is_read = True
        notification.save()
        
        from .serializers import NotificationDetailSerializer
        serializer = NotificationDetailSerializer(notification)
        return Response(
            {
                'message': _('Notification marked as read.'),
                'notification': serializer.data
            },
            status=status.HTTP_200_OK
        )
