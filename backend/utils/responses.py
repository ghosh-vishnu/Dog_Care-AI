"""
Standardized API response helpers for consistent response formatting.
All API responses follow a consistent structure for better client-side handling.
"""

from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, Optional, List
from django.core.paginator import Paginator


def success_response(
    data: Any = None,
    message: str = None,
    status_code: int = status.HTTP_200_OK,
    extra: Optional[Dict] = None
) -> Response:
    """
    Create a standardized success response.
    
    Args:
        data: Response data (dict, list, or any serializable object)
        message: Success message
        status_code: HTTP status code (default: 200)
        extra: Additional fields to include in response
    
    Returns:
        Response: Standardized success response
        
    Example:
        success_response(
            data={'id': 1, 'name': 'Fluffy'},
            message='Pet created successfully',
            status_code=status.HTTP_201_CREATED
        )
    """
    response_data = {
        'success': True,
        'message': message or 'Operation completed successfully',
    }
    
    if data is not None:
        response_data['data'] = data
    
    if extra:
        response_data.update(extra)
    
    return Response(response_data, status=status_code)


def error_response(
    message: str,
    errors: Optional[Dict[str, List[str]]] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    error_code: Optional[str] = None,
    extra: Optional[Dict] = None
) -> Response:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        errors: Field-specific errors (dict of field -> list of errors)
        status_code: HTTP status code (default: 400)
        error_code: Application-specific error code
        extra: Additional fields to include in response
    
    Returns:
        Response: Standardized error response
        
    Example:
        error_response(
            message='Validation failed',
            errors={'email': ['This field is required.']},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    """
    response_data = {
        'success': False,
        'message': message,
    }
    
    if errors:
        response_data['errors'] = errors
    
    if error_code:
        response_data['error_code'] = error_code
    
    if extra:
        response_data.update(extra)
    
    return Response(response_data, status=status_code)


def validation_error_response(
    errors: Dict[str, List[str]],
    message: str = 'Validation failed',
    status_code: int = status.HTTP_400_BAD_REQUEST
) -> Response:
    """
    Create a standardized validation error response.
    
    Args:
        errors: Field-specific validation errors
        message: Error message (default: 'Validation failed')
        status_code: HTTP status code (default: 400)
    
    Returns:
        Response: Standardized validation error response
        
    Example:
        validation_error_response(
            errors={
                'email': ['This field is required.', 'Enter a valid email address.'],
                'password': ['Password must be at least 8 characters.']
            }
        )
    """
    return error_response(
        message=message,
        errors=errors,
        status_code=status_code,
        error_code='VALIDATION_ERROR'
    )


def paginated_response(
    queryset,
    serializer_class,
    request,
    message: str = None,
    page_size: int = 20
) -> Response:
    """
    Create a standardized paginated response.
    
    Args:
        queryset: Django queryset to paginate
        serializer_class: DRF serializer class
        request: HTTP request object
        message: Success message
        page_size: Number of items per page
    
    Returns:
        Response: Standardized paginated response
        
    Example:
        paginated_response(
            queryset=Pet.objects.all(),
            serializer_class=PetListSerializer,
            request=request
        )
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.query_params.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except Exception:
        page = paginator.page(1)
    
    serializer = serializer_class(page.object_list, many=True)
    
    response_data = {
        'success': True,
        'message': message or 'Data retrieved successfully',
        'data': serializer.data,
        'pagination': {
            'count': paginator.count,
            'page': page.number,
            'pages': paginator.num_pages,
            'page_size': page_size,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'next': page.next_page_number() if page.has_next() else None,
            'previous': page.previous_page_number() if page.has_previous() else None,
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


def not_found_response(
    message: str = 'Resource not found',
    resource: str = None
) -> Response:
    """
    Create a standardized 404 not found response.
    
    Args:
        message: Error message
        resource: Resource type that was not found
    
    Returns:
        Response: Standardized 404 response
    """
    extra = {}
    if resource:
        extra['resource'] = resource
    
    return error_response(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code='NOT_FOUND',
        extra=extra
    )


def permission_denied_response(
    message: str = 'You do not have permission to perform this action'
) -> Response:
    """
    Create a standardized 403 permission denied response.
    
    Args:
        message: Error message
    
    Returns:
        Response: Standardized 403 response
    """
    return error_response(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        error_code='PERMISSION_DENIED'
    )


def unauthorized_response(
    message: str = 'Authentication required'
) -> Response:
    """
    Create a standardized 401 unauthorized response.
    
    Args:
        message: Error message
    
    Returns:
        Response: Standardized 401 response
    """
    return error_response(
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_code='UNAUTHORIZED'
    )


def server_error_response(
    message: str = 'An internal server error occurred',
    error_code: str = 'SERVER_ERROR'
) -> Response:
    """
    Create a standardized 500 server error response.
    Never expose internal error details in production.
    
    Args:
        message: Error message
        error_code: Application-specific error code
    
    Returns:
        Response: Standardized 500 response
    """
    return error_response(
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code=error_code
    )

