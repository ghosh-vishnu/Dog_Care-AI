from rest_framework import permissions
from django.core.exceptions import PermissionDenied


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user has ADMIN role.
    Prevents unauthorized access to admin-only endpoints.
    """

    def has_permission(self, request, view):
        """
        Check if user is authenticated and has ADMIN role.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for admin access.
        """
        return self.has_permission(request, view)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows read-only access to all authenticated users,
    but write access only to ADMIN users.
    """

    def has_permission(self, request, view):
        """
        Check permissions based on request method.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        """
        return self.has_permission(request, view)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to object owners or ADMIN users.
    Prevents IDOR (Insecure Direct Object Reference) vulnerabilities.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check to prevent IDOR.
        Admin users have full access, regular users can only access their own data.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False


class IsPetOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for pet-related objects.
    Users can only access objects related to their own pets.
    Admins can access all objects.
    Prevents IDOR vulnerabilities for pet-related resources.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for pet-related objects.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'pet'):
            return obj.pet.owner == request.user
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        return False


class IsSubscriptionOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for subscription-related objects.
    Users can only access their own subscriptions.
    Admins can access all subscriptions.
    Prevents IDOR vulnerabilities for subscription resources.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for subscription objects.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsVeterinarianOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to veterinarians or ADMIN users.
    """

    def has_permission(self, request, view):
        """
        Check if user is authenticated and is a veterinarian or admin.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.is_veterinarian or request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        """
        return self.has_permission(request, view)


class IsNotificationOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for notification objects.
    Users can only access their own notifications.
    Admins can access all notifications.
    Prevents IDOR vulnerabilities for notification resources.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for notification objects.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsAppointmentOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for appointment objects.
    Users can only access appointments for their own pets.
    Admins can access all appointments.
    Prevents IDOR vulnerabilities for appointment resources.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for appointment objects.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        if hasattr(obj, 'pet'):
            return obj.pet.owner == request.user
        
        return False


class IsUserSelfOrAdmin(permissions.BasePermission):
    """
    Permission class for user profile operations.
    Users can only access their own profile.
    Admins can access all profiles.
    Prevents IDOR vulnerabilities for user resources.
    """

    def has_permission(self, request, view):
        """
        Base permission check - user must be authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for user objects.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user
