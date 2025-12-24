from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from .models import Appointment
from apps.accounts.permissions import IsAdmin, IsAppointmentOwnerOrAdmin
from apps.pets.models import Pet


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment model with CRUD operations.
    Users can only access appointments for their own pets.
    Admins can access all appointments.
    """
    permission_classes = [IsAppointmentOwnerOrAdmin]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        from .serializers import (
            AppointmentSerializer,
            AppointmentListSerializer,
            AppointmentDetailSerializer,
        )
        if self.action == 'list':
            return AppointmentListSerializer
        elif self.action == 'retrieve':
            return AppointmentDetailSerializer
        return AppointmentSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        Users can only see appointments for their own pets.
        """
        queryset = Appointment.objects.select_related('pet', 'pet__owner', 'owner', 'veterinarian')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        
        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAppointmentOwnerOrAdmin()]
        return [IsAppointmentOwnerOrAdmin()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new appointment.
        Permission check is done on the pet object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.validated_data.get('pet')
        self.check_object_permissions(request, pet)
        
        appointment = serializer.save(owner=request.user)
        
        from .serializers import AppointmentDetailSerializer
        response_serializer = AppointmentDetailSerializer(appointment)
        return Response(
            {
                'message': _('Appointment created successfully.'),
                'appointment': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve appointment details.
        Permission is handled by IsAppointmentOwnerOrAdmin permission class.
        """
        appointment = self.get_object()
        self.check_object_permissions(request, appointment)
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update appointment information.
        Permission is handled by IsAppointmentOwnerOrAdmin permission class.
        """
        appointment = self.get_object()
        self.check_object_permissions(request, appointment)
        
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if 'pet' in serializer.validated_data:
            pet = serializer.validated_data.get('pet')
            self.check_object_permissions(request, pet)
        
        serializer.save()
        
        from .serializers import AppointmentDetailSerializer
        response_serializer = AppointmentDetailSerializer(appointment)
        return Response(
            {
                'message': _('Appointment updated successfully.'),
                'appointment': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update appointment information.
        Permission is handled by IsAppointmentOwnerOrAdmin permission class.
        """
        appointment = self.get_object()
        self.check_object_permissions(request, appointment)
        
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if 'pet' in serializer.validated_data:
            pet = serializer.validated_data.get('pet')
            self.check_object_permissions(request, pet)
        
        serializer.save()
        
        from .serializers import AppointmentDetailSerializer
        response_serializer = AppointmentDetailSerializer(appointment)
        return Response(
            {
                'message': _('Appointment updated successfully.'),
                'appointment': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete appointment.
        Permission is handled by IsAppointmentOwnerOrAdmin permission class.
        """
        appointment = self.get_object()
        self.check_object_permissions(request, appointment)
        
        appointment.delete()
        
        return Response(
            {'message': _('Appointment deleted successfully.')},
            status=status.HTTP_200_OK
        )
