"""
Custom exception handler for Django REST Framework.
Provides standardized error responses and prevents raw exceptions from being leaked.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .exceptions import (
    APIException,
    ValidationException,
    NotFoundException,
    PermissionDeniedException,
    BadRequestException,
)
from .responses import (
    error_response,
    validation_error_response,
    server_error_response,
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides standardized error responses.
    
    Args:
        exc: The exception that was raised
        context: Dictionary containing context information about the exception
    
    Returns:
        Response: Standardized error response or None to use default handler
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Handle custom API exceptions
    if isinstance(exc, APIException):
        return handle_custom_exception(exc)
    
    # Handle Django exceptions
    if isinstance(exc, Http404):
        return handle_http404(exc)
    
    if isinstance(exc, PermissionDenied):
        return handle_permission_denied(exc)
    
    if isinstance(exc, DjangoValidationError):
        return handle_django_validation_error(exc)
    
    if isinstance(exc, IntegrityError):
        return handle_integrity_error(exc)
    
    if isinstance(exc, ObjectDoesNotExist):
        return handle_object_not_found(exc)
    
    # Handle DRF exceptions
    if response is not None:
        return handle_drf_exception(response, exc)
    
    # Handle unexpected exceptions (never expose internal details in production)
    return handle_unexpected_exception(exc, context)


def handle_custom_exception(exc: APIException) -> Response:
    """
    Handle custom API exceptions.
    
    Args:
        exc: Custom API exception
    
    Returns:
        Response: Standardized error response
    """
    if isinstance(exc, ValidationException):
        errors = exc.errors if hasattr(exc, 'errors') else {}
        return validation_error_response(
            errors=errors,
            message=str(exc.detail),
            status_code=exc.status_code
        )
    
    if isinstance(exc, NotFoundException):
        extra = {}
        if hasattr(exc, 'resource'):
            extra['resource'] = exc.resource
        
        return error_response(
            message=str(exc.detail),
            status_code=exc.status_code,
            error_code=exc.default_code,
            extra=extra if extra else None
        )
    
    return error_response(
        message=str(exc.detail),
        status_code=exc.status_code,
        error_code=exc.default_code
    )


def handle_http404(exc: Http404) -> Response:
    """
    Handle Django Http404 exceptions.
    
    Args:
        exc: Http404 exception
    
    Returns:
        Response: Standardized 404 response
    """
    message = str(exc) if str(exc) else 'Resource not found'
    return error_response(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code='NOT_FOUND'
    )


def handle_permission_denied(exc: PermissionDenied) -> Response:
    """
    Handle Django PermissionDenied exceptions.
    
    Args:
        exc: PermissionDenied exception
    
    Returns:
        Response: Standardized 403 response
    """
    message = str(exc) if str(exc) else 'You do not have permission to perform this action'
    return error_response(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        error_code='PERMISSION_DENIED'
    )


def handle_django_validation_error(exc: DjangoValidationError) -> Response:
    """
    Handle Django ValidationError exceptions.
    
    Args:
        exc: Django ValidationError exception
    
    Returns:
        Response: Standardized validation error response
    """
    errors = {}
    
    if hasattr(exc, 'error_dict'):
        # Field-specific errors
        for field, field_errors in exc.error_dict.items():
            errors[field] = [str(error) for error in field_errors]
    elif hasattr(exc, 'error_list'):
        # Non-field errors
        errors['non_field_errors'] = [str(error) for error in exc.error_list]
    else:
        # Single error message
        errors['non_field_errors'] = [str(exc)]
    
    return validation_error_response(
        errors=errors,
        message='Validation failed',
        status_code=status.HTTP_400_BAD_REQUEST
    )


def handle_integrity_error(exc: IntegrityError) -> Response:
    """
    Handle database IntegrityError exceptions.
    
    Args:
        exc: IntegrityError exception
    
    Returns:
        Response: Standardized error response
    """
    error_message = str(exc)
    
    # Check for common integrity errors
    if 'UNIQUE constraint' in error_message or 'duplicate key' in error_message.lower():
        message = 'A record with this information already exists'
        error_code = 'DUPLICATE_ENTRY'
    elif 'FOREIGN KEY constraint' in error_message:
        message = 'Invalid reference to related resource'
        error_code = 'INVALID_REFERENCE'
    else:
        message = 'Database integrity error occurred'
        error_code = 'INTEGRITY_ERROR'
    
    logger.error(f"IntegrityError: {error_message}")
    
    return error_response(
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code=error_code
    )


def handle_object_not_found(exc: ObjectDoesNotExist) -> Response:
    """
    Handle Django ObjectDoesNotExist exceptions.
    
    Args:
        exc: ObjectDoesNotExist exception
    
    Returns:
        Response: Standardized 404 response
    """
    return error_response(
        message='Resource not found',
        status_code=status.HTTP_404_NOT_FOUND,
        error_code='NOT_FOUND'
    )


def handle_drf_exception(response: Response, exc: Exception) -> Response:
    """
    Handle DRF exceptions and standardize the response format.
    
    Args:
        response: DRF exception response
        exc: Original exception
    
    Returns:
        Response: Standardized error response
    """
    # Get error details from DRF response
    error_data = response.data
    
    # Standardize response format
    standardized_data = {
        'success': False,
    }
    
    # Handle different DRF exception formats
    if isinstance(error_data, dict):
        # Check for validation errors
        if 'detail' in error_data:
            standardized_data['message'] = str(error_data['detail'])
        elif any(isinstance(v, (list, dict)) for v in error_data.values()):
            # Field-specific validation errors
            standardized_data['message'] = 'Validation failed'
            standardized_data['errors'] = error_data
        else:
            standardized_data['message'] = str(error_data.get('detail', 'An error occurred'))
            standardized_data.update(error_data)
    elif isinstance(error_data, list):
        standardized_data['message'] = error_data[0] if error_data else 'An error occurred'
        standardized_data['errors'] = {'non_field_errors': error_data}
    else:
        standardized_data['message'] = str(error_data)
    
    # Add error code if available
    if hasattr(exc, 'default_code'):
        standardized_data['error_code'] = exc.default_code
    
    response.data = standardized_data
    return response


def handle_unexpected_exception(exc: Exception, context: dict) -> Response:
    """
    Handle unexpected exceptions that are not caught by DRF or custom handlers.
    Never expose internal error details in production.
    
    Args:
        exc: Unexpected exception
        context: Exception context
    
    Returns:
        Response: Standardized 500 error response
    """
    # Log the full exception for debugging
    logger.exception(
        f"Unexpected exception: {type(exc).__name__}: {str(exc)}",
        extra={'context': context}
    )
    
    # Return generic error message (never expose internal details)
    return server_error_response(
        message='An internal server error occurred. Please try again later.',
        error_code='SERVER_ERROR'
    )

