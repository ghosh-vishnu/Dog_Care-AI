from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from .models import Pet
from .serializers import (
    PetSerializer,
    PetListSerializer,
    PetDetailSerializer,
)
from apps.accounts.permissions import IsAdmin, IsOwnerOrAdmin


class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pet model with CRUD operations and soft delete support.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return PetListSerializer
        elif self.action == 'retrieve':
            return PetDetailSerializer
        return PetSerializer

    def get_queryset(self):
        """
        Return queryset optimized for current user or admin.
        """
        queryset = Pet.objects.select_related('owner')
        
        if self.request.user.role == 'ADMIN':
            return queryset
        else:
            return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        return [IsOwnerOrAdmin()]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new pet.
        Owner is automatically set to current user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pet = serializer.save(owner=request.user)
        
        response_serializer = PetDetailSerializer(pet)
        return Response(
            {
                'message': _('Pet created successfully.'),
                'pet': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve pet details.
        Permission is handled by IsOwnerOrAdmin permission class.
        """
        pet = self.get_object()
        self.check_object_permissions(request, pet)
        
        serializer = self.get_serializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update pet information.
        Permission is handled by IsOwnerOrAdmin permission class.
        """
        pet = self.get_object()
        self.check_object_permissions(request, pet)
        
        serializer = self.get_serializer(pet, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_serializer = PetDetailSerializer(pet)
        return Response(
            {
                'message': _('Pet updated successfully.'),
                'pet': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update pet information.
        Permission is handled by IsOwnerOrAdmin permission class.
        """
        pet = self.get_object()
        self.check_object_permissions(request, pet)
        
        serializer = self.get_serializer(pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_serializer = PetDetailSerializer(pet)
        return Response(
            {
                'message': _('Pet updated successfully.'),
                'pet': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete pet.
        Permission is handled by IsOwnerOrAdmin permission class.
        """
        pet = self.get_object()
        self.check_object_permissions(request, pet)
        
        pet.delete()
        
        return Response(
            {'message': _('Pet deleted successfully.')},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_pets(self, request):
        """
        Get all pets owned by current user.
        """
        pets = Pet.objects.filter(owner=request.user).select_related('owner')
        page = self.paginate_queryset(pets)
        
        if page is not None:
            serializer = PetListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PetListSerializer(pets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='restore'
    )
    def restore(self, request, pk=None):
        """
        Restore a soft-deleted pet.
        Only admin or original owner can restore.
        """
        pet = get_object_or_404(Pet.all_objects, pk=pk)
        
        if not pet.is_deleted:
            return Response(
                {'detail': _('Pet is not deleted.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.check_object_permissions(request, pet)
        
        pet.restore()
        
        serializer = PetDetailSerializer(pet)
        return Response(
            {
                'message': _('Pet restored successfully.'),
                'pet': serializer.data
            },
            status=status.HTTP_200_OK
        )
