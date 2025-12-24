from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDataSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserListSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from .permissions import IsAdmin, IsUserSelfOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model with role-based access control.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return UserListSerializer
        elif self.action in ['retrieve', 'me']:
            return UserDataSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        return UserDataSerializer

    def get_permissions(self):
        """
        Return appropriate permissions based on action.
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAdmin()]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            return [IsUserSelfOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related.
        """
        queryset = User.objects.all()
        
        if self.action == 'list':
            if self.request.user.role != 'ADMIN':
                queryset = queryset.filter(id=self.request.user.id)
        
        return queryset.select_related()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Register a new user account.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': _('User registered successfully.'),
                'user': UserDataSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get or update current user's profile.
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserDataSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {
                    'message': _('Profile updated successfully.'),
                    'user': UserDataSerializer(user).data
                },
                status=status.HTTP_200_OK
            )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='change-password'
    )
    def change_password(self, request):
        """
        Change user password.
        """
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {'message': _('Password changed successfully.')},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete user (deactivate instead of delete).
        """
        user = self.get_object()
        
        if user == request.user:
            return Response(
                {'error': _('You cannot delete your own account.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = False
        user.save()
        
        return Response(
            {'message': _('User deactivated successfully.')},
            status=status.HTTP_200_OK
        )


class UserLoginView(generics.GenericAPIView):
    """
    User login view with JWT token generation.
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': _('Login successful.'),
                'user': UserDataSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            status=status.HTTP_200_OK
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view with user data.
    """
    def post(self, request, *args, **kwargs):
        """
        Override to include user data in response.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data.get('email'))
            response.data['user'] = UserDataSerializer(user).data
        
        return response


class UserProfileViewSet(viewsets.ViewSet):
    """
    ViewSet for UserProfile model.
    Provides endpoints to fetch and update user profile.
    """
    permission_classes = [IsUserSelfOrAdmin]

    def get_queryset(self):
        """
        Return queryset optimized for profile access.
        """
        return UserProfile.objects.select_related('user')

    def retrieve(self, request, pk=None):
        """
        Retrieve user profile.
        Permission is handled by IsUserSelfOrAdmin permission class.
        """
        if pk and pk != 'me':
            profile = get_object_or_404(UserProfile, user_id=pk)
            self.check_object_permissions(request, profile)
        else:
            profile, created = UserProfile.objects.get_or_create(
                user=request.user
            )
        
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, pk=None):
        """
        Update user profile.
        Permission is handled by IsUserSelfOrAdmin permission class.
        """
        if pk and pk != 'me':
            profile = get_object_or_404(UserProfile, user_id=pk)
            self.check_object_permissions(request, profile)
        else:
            profile, created = UserProfile.objects.get_or_create(
                user=request.user
            )
        
        serializer = UserProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_serializer = UserProfileSerializer(profile)
        return Response(
            {
                'message': _('Profile updated successfully.'),
                'profile': response_serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get or update current user's profile.
        """
        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserProfileUpdateSerializer(
                profile,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            response_serializer = UserProfileSerializer(profile)
            return Response(
                {
                    'message': _('Profile updated successfully.'),
                    'profile': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
