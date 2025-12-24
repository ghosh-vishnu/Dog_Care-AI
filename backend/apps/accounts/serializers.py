from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates and creates new user accounts.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='Password must meet security requirements'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Re-enter password for confirmation'
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'phone_number',
            'role',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'phone_number': {'required': False, 'allow_blank': True},
        }

    def validate_email(self, value):
        """
        Validate email uniqueness and format.
        """
        value = User.objects.normalize_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _('A user with this email already exists.')
            )
        return value

    def validate(self, attrs):
        """
        Validate password confirmation and role assignment.
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        role = attrs.get('role', User.Role.USER)

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': _('Passwords do not match.')
            })

        if role == User.Role.ADMIN:
            raise serializers.ValidationError({
                'role': _('Cannot register with ADMIN role. Contact administrator.')
            })

        attrs.pop('password_confirm', None)
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        validated_data['role'] = User.Role.USER
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login authentication.
    """
    email = serializers.EmailField(
        required=True,
        help_text='User email address'
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        help_text='User password'
    )

    def validate(self, attrs):
        """
        Validate user credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                _('Must include "email" and "password".'),
                code='authorization'
            )

        email = User.objects.normalize_email(email)
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                _('Unable to log in with provided credentials.'),
                code='authorization'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                _('User account is disabled.'),
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class UserDataSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    full_name = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(read_only=True)
    is_regular_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'profile_picture',
            'role',
            'is_veterinarian',
            'is_active',
            'is_admin',
            'is_regular_user',
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'id',
            'email',
            'role',
            'is_active',
            'date_joined',
            'last_login',
        ]

    def get_full_name(self, obj):
        """
        Return full name of the user.
        """
        return obj.get_full_name()


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'is_veterinarian',
        ]

    def validate_phone_number(self, value):
        """
        Validate phone number format if provided.
        """
        if value:
            phone_validator = User._meta.get_field('phone_number').validators[0]
            try:
                phone_validator(value)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Current password'
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='New password must meet security requirements'
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Re-enter new password for confirmation'
    )

    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Old password is incorrect.')
            )
        return value

    def validate(self, attrs):
        """
        Validate password confirmation.
        """
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': _('New passwords do not match.')
            })

        old_password = attrs.get('old_password')
        if old_password == new_password:
            raise serializers.ValidationError({
                'new_password': _('New password must be different from old password.')
            })

        return attrs

    def save(self):
        """
        Update user password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users (minimal information).
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'role',
            'is_veterinarian',
            'is_active',
            'date_joined',
        ]

    def get_full_name(self, obj):
        """
        Return full name of the user.
        """
        return obj.get_full_name()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    Used for fetching and updating user profile information.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'location',
            'is_active',
            'user_email',
            'user_full_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'created_at',
            'updated_at',
        ]

    def get_user_full_name(self, obj):
        """
        Return full name of the associated user.
        """
        return obj.user.get_full_name()

    def validate_phone(self, value):
        """
        Validate phone number format if provided.
        """
        if value:
            phone_validator = UserProfile._meta.get_field('phone').validators[0]
            try:
                phone_validator(value)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating UserProfile.
    Allows partial updates.
    """
    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'location',
            'is_active',
        ]

    def validate_phone(self, value):
        """
        Validate phone number format if provided.
        """
        if value:
            phone_validator = UserProfile._meta.get_field('phone').validators[0]
            try:
                phone_validator(value)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return value

