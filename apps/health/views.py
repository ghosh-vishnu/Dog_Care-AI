from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from .models import Vaccination, HealthRecord
from .serializers import (
    VaccinationSerializer,
    VaccinationListSerializer,
    VaccinationDetailSerializer,
    HealthRecordSerializer,
    HealthRecordListSerializer,
    HealthRecordDetailSerializer,
)
from apps.accounts.permissions import IsAdmin, IsPetOwnerOrAdmin
from apps.pets.models import Pet


class VaccinationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vaccination model with CRUD operations.
    Users can only access vaccinations for their own pets.
    Admins can access all vaccinations.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return VaccinationListSerializer
        elif self.action == 'retrieve':
            return VaccinationDetailSerializer
        return VaccinationSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        Users can only see vaccinations for their own pets.
        """
        queryset = Vaccination.objects.select_related('pet', 'pet__owner', 'veterinarian')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        
        return queryset.filter(pet__owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new vaccination.
        Permission check is done on the pet object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.validated_data.get('pet')
        self.check_object_permissions(request, pet)
        
        vaccination = serializer.save()
        
        response_serializer = VaccinationDetailSerializer(vaccination)
        return Response(
            {
                'message': _('Vaccination created successfully.'),
                'vaccination': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve vaccination details.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        vaccination = self.get_object()
        self.check_object_permissions(request, vaccination)
        
        serializer = self.get_serializer(vaccination)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update vaccination information.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        vaccination = self.get_object()
        self.check_object_permissions(request, vaccination)
        
        serializer = self.get_serializer(vaccination, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.validated_data.get('pet', vaccination.pet)
        self.check_object_permissions(request, pet)
        
        serializer.save()
        
        response_serializer = VaccinationDetailSerializer(vaccination)
        return Response(
            {
                'message': _('Vaccination updated successfully.'),
                'vaccination': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update vaccination information.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        vaccination = self.get_object()
        self.check_object_permissions(request, vaccination)
        
        serializer = self.get_serializer(vaccination, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if 'pet' in serializer.validated_data:
            pet = serializer.validated_data.get('pet')
            self.check_object_permissions(request, pet)
        
        serializer.save()
        
        response_serializer = VaccinationDetailSerializer(vaccination)
        return Response(
            {
                'message': _('Vaccination updated successfully.'),
                'vaccination': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete vaccination.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        vaccination = self.get_object()
        self.check_object_permissions(request, vaccination)
        
        vaccination.delete()
        
        return Response(
            {'message': _('Vaccination deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_pets_vaccinations(self, request):
        """
        Get all vaccinations for current user's pets.
        """
        vaccinations = Vaccination.objects.filter(
            pet__owner=request.user
        ).select_related('pet', 'pet__owner', 'veterinarian')
        
        page = self.paginate_queryset(vaccinations)
        
        if page is not None:
            serializer = VaccinationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = VaccinationListSerializer(vaccinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        """
        Get all pending vaccinations for current user's pets.
        """
        vaccinations = Vaccination.objects.filter(
            pet__owner=request.user,
            status='pending'
        ).select_related('pet', 'pet__owner', 'veterinarian')
        
        page = self.paginate_queryset(vaccinations)
        
        if page is not None:
            serializer = VaccinationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = VaccinationListSerializer(vaccinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def overdue(self, request):
        """
        Get all overdue vaccinations for current user's pets.
        """
        vaccinations = Vaccination.objects.filter(
            pet__owner=request.user,
            status='overdue'
        ).select_related('pet', 'pet__owner', 'veterinarian')
        
        page = self.paginate_queryset(vaccinations)
        
        if page is not None:
            serializer = VaccinationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = VaccinationListSerializer(vaccinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for HealthRecord model with CRUD operations.
    Users can only access health records for their own pets.
    Admins can access all health records.
    """
    permission_classes = [IsPetOwnerOrAdmin]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return HealthRecordListSerializer
        elif self.action == 'retrieve':
            return HealthRecordDetailSerializer
        return HealthRecordSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        Users can only see health records for their own pets.
        """
        queryset = HealthRecord.objects.select_related('pet', 'pet__owner', 'veterinarian')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        
        return queryset.filter(pet__owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new health record.
        Permission check is done on the pet object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.validated_data.get('pet')
        self.check_object_permissions(request, pet)
        
        health_record = serializer.save()
        
        response_serializer = HealthRecordDetailSerializer(health_record)
        return Response(
            {
                'message': _('Health record created successfully.'),
                'health_record': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve health record details.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        health_record = self.get_object()
        self.check_object_permissions(request, health_record)
        
        serializer = self.get_serializer(health_record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update health record information.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        health_record = self.get_object()
        self.check_object_permissions(request, health_record)
        
        serializer = self.get_serializer(health_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.validated_data.get('pet', health_record.pet)
        self.check_object_permissions(request, pet)
        
        serializer.save()
        
        response_serializer = HealthRecordDetailSerializer(health_record)
        return Response(
            {
                'message': _('Health record updated successfully.'),
                'health_record': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update health record information.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        health_record = self.get_object()
        self.check_object_permissions(request, health_record)
        
        serializer = self.get_serializer(health_record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if 'pet' in serializer.validated_data:
            pet = serializer.validated_data.get('pet')
            self.check_object_permissions(request, pet)
        
        serializer.save()
        
        response_serializer = HealthRecordDetailSerializer(health_record)
        return Response(
            {
                'message': _('Health record updated successfully.'),
                'health_record': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete health record.
        Permission is handled by IsPetOwnerOrAdmin permission class.
        """
        health_record = self.get_object()
        self.check_object_permissions(request, health_record)
        
        health_record.delete()
        
        return Response(
            {'message': _('Health record deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_pets_records(self, request):
        """
        Get all health records for current user's pets.
        """
        health_records = HealthRecord.objects.filter(
            pet__owner=request.user
        ).select_related('pet', 'pet__owner', 'veterinarian')
        
        page = self.paginate_queryset(health_records)
        
        if page is not None:
            serializer = HealthRecordListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = HealthRecordListSerializer(health_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def pet_records(self, request, pk=None):
        """
        Get all health records for a specific pet.
        Users can only access records for their own pets.
        """
        pet = get_object_or_404(Pet, id=pk)
        
        self.check_object_permissions(request, pet)
        
        health_records = HealthRecord.objects.filter(
            pet=pet
        ).select_related('pet', 'pet__owner', 'veterinarian')
        
        page = self.paginate_queryset(health_records)
        
        if page is not None:
            serializer = HealthRecordListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = HealthRecordListSerializer(health_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
