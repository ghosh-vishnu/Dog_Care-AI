# API Response Standard & Error Handling

## Overview

This document describes the standardized API response format and error handling system implemented in the Pet Health Backend.

## Standardized Response Format

All API responses follow a consistent structure for better client-side handling.

### Success Response Format

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response Format

```json
{
  "success": false,
  "message": "Error message",
  "errors": {
    "field_name": ["Error message 1", "Error message 2"]
  },
  "error_code": "ERROR_CODE"
}
```

## Response Helpers

### `success_response()`

Create a standardized success response.

```python
from utils.responses import success_response

# Basic success response
return success_response(
    data={'id': 1, 'name': 'Fluffy'},
    message='Pet created successfully',
    status_code=status.HTTP_201_CREATED
)
```

**Parameters:**
- `data`: Response data (dict, list, or any serializable object)
- `message`: Success message (optional)
- `status_code`: HTTP status code (default: 200)
- `extra`: Additional fields to include in response (optional)

### `error_response()`

Create a standardized error response.

```python
from utils.responses import error_response

# Basic error response
return error_response(
    message='Validation failed',
    errors={'email': ['This field is required.']},
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code='VALIDATION_ERROR'
)
```

**Parameters:**
- `message`: Error message (required)
- `errors`: Field-specific errors (dict, optional)
- `status_code`: HTTP status code (default: 400)
- `error_code`: Application-specific error code (optional)
- `extra`: Additional fields (optional)

### `validation_error_response()`

Create a standardized validation error response.

```python
from utils.responses import validation_error_response

return validation_error_response(
    errors={
        'email': ['This field is required.', 'Enter a valid email address.'],
        'password': ['Password must be at least 8 characters.']
    },
    message='Validation failed'
)
```

### `not_found_response()`

Create a standardized 404 response.

```python
from utils.responses import not_found_response

return not_found_response(
    message='Pet not found',
    resource='Pet'
)
```

### `permission_denied_response()`

Create a standardized 403 response.

```python
from utils.responses import permission_denied_response

return permission_denied_response(
    message='You do not have permission to perform this action'
)
```

### `unauthorized_response()`

Create a standardized 401 response.

```python
from utils.responses import unauthorized_response

return unauthorized_response(
    message='Authentication required'
)
```

## Custom Exceptions

### `APIException`

Base exception class for all API exceptions.

```python
from utils.exceptions import APIException

raise APIException(
    detail='Custom error message',
    code='CUSTOM_ERROR',
    status_code=status.HTTP_400_BAD_REQUEST
)
```

### `ValidationException`

Exception for validation errors.

```python
from utils.exceptions import ValidationException

raise ValidationException(
    detail='Validation failed',
    errors={'field': ['Error message']}
)
```

### `NotFoundException`

Exception for resource not found errors.

```python
from utils.exceptions import NotFoundException

raise NotFoundException(
    detail='Pet not found',
    resource='Pet'
)
```

### `PermissionDeniedException`

Exception for permission denied errors.

```python
from utils.exceptions import PermissionDeniedException

raise PermissionDeniedException(
    detail='You do not have permission to perform this action'
)
```

### `BadRequestException`

Exception for bad request errors.

```python
from utils.exceptions import BadRequestException

raise BadRequestException(
    detail='Invalid request data'
)
```

### `ConflictException`

Exception for conflict errors (e.g., duplicate entry).

```python
from utils.exceptions import ConflictException

raise ConflictException(
    detail='A record with this information already exists'
)
```

## Exception Handler

The custom exception handler automatically:

1. **Handles DRF exceptions** - Standardizes DRF exception responses
2. **Handles Django exceptions** - Converts Django exceptions to standardized format
3. **Handles custom exceptions** - Processes custom API exceptions
4. **Prevents information leakage** - Never exposes internal error details in production
5. **Logs errors** - Logs all exceptions for debugging

### Automatic Exception Handling

The following exceptions are automatically handled:

- `APIException` and subclasses
- `Http404` (Django)
- `PermissionDenied` (Django)
- `ValidationError` (Django)
- `IntegrityError` (Django)
- `ObjectDoesNotExist` (Django)
- All DRF exceptions

### Example: Automatic Error Handling

```python
# In your ViewSet
def retrieve(self, request, pk=None):
    pet = get_object_or_404(Pet, pk=pk)  # Automatically returns standardized 404
    # ...
```

## Usage Examples

### Example 1: Create Operation

```python
@transaction.atomic
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # Automatically handled
    
    pet = serializer.save(owner=request.user)
    
    return success_response(
        data={'pet': PetDetailSerializer(pet).data},
        message='Pet created successfully',
        status_code=status.HTTP_201_CREATED
    )
```

### Example 2: Update Operation

```python
@transaction.atomic
def update(self, request, *args, **kwargs):
    pet = self.get_object()
    self.check_object_permissions(request, pet)  # Automatically handled
    
    serializer = self.get_serializer(pet, data=request.data)
    serializer.is_valid(raise_exception=True)  # Automatically handled
    
    serializer.save()
    
    return success_response(
        data={'pet': PetDetailSerializer(pet).data},
        message='Pet updated successfully'
    )
```

### Example 3: Custom Error Handling

```python
def destroy(self, request, *args, **kwargs):
    user = self.get_object()
    
    if user == request.user:
        return error_response(
            message='You cannot delete your own account',
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code='CANNOT_DELETE_OWN_ACCOUNT'
        )
    
    user.is_active = False
    user.save()
    
    return success_response(
        message='User deactivated successfully'
    )
```

### Example 4: Using Custom Exceptions

```python
from utils.exceptions import NotFoundException, ConflictException

def retrieve(self, request, pk=None):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        raise NotFoundException(
            detail='Pet not found',
            resource='Pet'
        )
    
    # Check for duplicate
    if Pet.objects.filter(name=pet.name, owner=request.user).exists():
        raise ConflictException(
            detail='A pet with this name already exists'
        )
    
    return success_response(data=PetSerializer(pet).data)
```

## HTTP Status Codes

Standard HTTP status codes used:

- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST (resource created)
- `400 Bad Request` - Validation errors, bad request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `422 Unprocessable Entity` - Well-formed but semantically incorrect
- `500 Internal Server Error` - Server errors (never expose details)

## Error Codes

Common error codes:

- `VALIDATION_ERROR` - Validation failed
- `NOT_FOUND` - Resource not found
- `PERMISSION_DENIED` - Permission denied
- `UNAUTHORIZED` - Authentication required
- `BAD_REQUEST` - Bad request
- `CONFLICT` - Resource conflict
- `DUPLICATE_ENTRY` - Duplicate entry
- `INTEGRITY_ERROR` - Database integrity error
- `SERVER_ERROR` - Internal server error

## Best Practices

1. **Always use response helpers** - Use `success_response()` and `error_response()` instead of raw `Response()`
2. **Use appropriate status codes** - Follow REST conventions
3. **Provide meaningful messages** - Help users understand what went wrong
4. **Include error codes** - Make it easier for clients to handle errors programmatically
5. **Never expose internal details** - Don't leak database errors or stack traces
6. **Log errors** - All exceptions are automatically logged for debugging
7. **Use transactions** - Wrap write operations in `@transaction.atomic`
8. **Validate early** - Use serializer validation, don't validate in views

## Migration Guide

### Before (Old Pattern)

```python
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    pet = serializer.save(owner=request.user)
    
    return Response(
        {
            'message': 'Pet created successfully',
            'pet': PetSerializer(pet).data
        },
        status=status.HTTP_201_CREATED
    )
```

### After (New Pattern)

```python
from utils.responses import success_response

def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # Automatically handled
    pet = serializer.save(owner=request.user)
    
    return success_response(
        data={'pet': PetSerializer(pet).data},
        message='Pet created successfully',
        status_code=status.HTTP_201_CREATED
    )
```

## Testing

All exceptions are automatically handled and return standardized responses. Test your APIs to ensure:

1. Success responses include `success: true`
2. Error responses include `success: false`
3. Validation errors are properly formatted
4. Status codes are appropriate
5. No internal error details are exposed

## Configuration

The exception handler is configured in `config/settings/base.py`:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
    # ... other settings
}
```

