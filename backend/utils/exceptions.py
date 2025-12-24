"""
Custom exceptions for the Pet Health Backend API.
These exceptions provide better error handling and consistent error responses.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class APIException(APIException):
    """
    Base exception class for all API exceptions.
    All custom exceptions should inherit from this.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        """
        Initialize exception with optional detail, code, and status_code.
        
        Args:
            detail: Error message or detail
            code: Error code
            status_code: HTTP status code
        """
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.default_code = code
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail


class ValidationException(APIException):
    """
    Exception for validation errors.
    Use when data validation fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Validation failed'
    default_code = 'VALIDATION_ERROR'

    def __init__(self, detail=None, errors=None, code=None):
        """
        Initialize validation exception.
        
        Args:
            detail: Error message
            errors: Field-specific errors (dict)
            code: Error code
        """
        super().__init__(detail=detail, code=code)
        self.errors = errors or {}


class NotFoundException(APIException):
    """
    Exception for resource not found errors.
    Use when a requested resource does not exist.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found'
    default_code = 'NOT_FOUND'

    def __init__(self, detail=None, resource=None, code=None):
        """
        Initialize not found exception.
        
        Args:
            detail: Error message
            resource: Resource type that was not found
            code: Error code
        """
        super().__init__(detail=detail, code=code)
        self.resource = resource


class PermissionDeniedException(APIException):
    """
    Exception for permission denied errors.
    Use when user lacks required permissions.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action'
    default_code = 'PERMISSION_DENIED'


class BadRequestException(APIException):
    """
    Exception for bad request errors.
    Use when request is malformed or invalid.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request'
    default_code = 'BAD_REQUEST'


class UnauthorizedException(APIException):
    """
    Exception for authentication errors.
    Use when user is not authenticated.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication required'
    default_code = 'UNAUTHORIZED'


class ConflictException(APIException):
    """
    Exception for conflict errors.
    Use when request conflicts with current state (e.g., duplicate entry).
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict occurred'
    default_code = 'CONFLICT'


class UnprocessableEntityException(APIException):
    """
    Exception for unprocessable entity errors.
    Use when request is well-formed but semantically incorrect.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Unprocessable entity'
    default_code = 'UNPROCESSABLE_ENTITY'

