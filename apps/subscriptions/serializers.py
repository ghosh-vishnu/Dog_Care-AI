from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for SubscriptionPlan model with full validation.
    """
    plan_type_display = serializers.CharField(
        source='get_plan_type_display',
        read_only=True
    )

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'plan_type',
            'plan_type_display',
            'name',
            'description',
            'price',
            'duration_days',
            'is_active',
            'features',
            'max_pets',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'plan_type_display']

    def validate_plan_type(self, value):
        """
        Validate plan type is valid.
        """
        valid_types = [choice[0] for choice in SubscriptionPlan.PLAN_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f'Plan type must be one of: {", ".join(valid_types)}'
            )
        return value

    def validate_price(self, value):
        """
        Validate price is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError('Price cannot be negative.')
        return value

    def validate(self, attrs):
        """
        Cross-field validation.
        """
        plan_type = attrs.get('plan_type') or (
            self.instance.plan_type if self.instance else None
        )
        price = attrs.get('price') or (
            self.instance.price if self.instance else None
        )

        if plan_type == 'free' and price and price > 0:
            raise serializers.ValidationError({
                'price': 'Free plan must have price 0.00.'
            })

        return attrs


class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing subscription plans.
    """
    plan_type_display = serializers.CharField(
        source='get_plan_type_display',
        read_only=True
    )

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'plan_type',
            'plan_type_display',
            'name',
            'price',
            'duration_days',
            'is_active',
            'max_pets',
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSubscription model with full validation.
    """
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_type = serializers.CharField(source='plan.plan_type', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    is_currently_active = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'user_email',
            'plan',
            'plan_name',
            'plan_type',
            'start_date',
            'end_date',
            'status',
            'status_display',
            'is_active',
            'is_currently_active',
            'auto_renew',
            'cancelled_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'plan_name',
            'plan_type',
            'user_email',
            'status_display',
            'is_currently_active',
            'cancelled_at',
        ]

    def get_is_currently_active(self, obj):
        """
        Check if subscription is currently active.
        """
        return obj.is_currently_active()

    def validate_start_date(self, value):
        """
        Validate start date is not in the future.
        """
        if value > timezone.now().date():
            raise serializers.ValidationError(
                'Start date cannot be in the future.'
            )
        return value

    def validate_end_date(self, value):
        """
        Validate end date is after start date.
        """
        start_date = self.initial_data.get('start_date') or (
            self.instance.start_date if self.instance else None
        )
        
        if start_date and value <= start_date:
            raise serializers.ValidationError(
                'End date must be after start date.'
            )
        return value

    def validate(self, attrs):
        """
        Cross-field validation.
        """
        start_date = attrs.get('start_date') or (
            self.instance.start_date if self.instance else None
        )
        end_date = attrs.get('end_date') or (
            self.instance.end_date if self.instance else None
        )
        plan = attrs.get('plan') or (
            self.instance.plan if self.instance else None
        )

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })

        if plan and start_date:
            from datetime import timedelta
            expected_end_date = start_date + timedelta(days=plan.duration_days)
            if end_date and end_date != expected_end_date:
                pass

        return attrs


class UserSubscriptionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing user subscriptions.
    """
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_type = serializers.CharField(source='plan.plan_type', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'plan',
            'plan_name',
            'plan_type',
            'start_date',
            'end_date',
            'status',
            'status_display',
            'is_active',
        ]


class UserSubscriptionDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user subscription with plan information.
    """
    plan = SubscriptionPlanSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    is_currently_active = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'plan',
            'start_date',
            'end_date',
            'status',
            'status_display',
            'is_active',
            'is_currently_active',
            'auto_renew',
            'cancelled_at',
            'days_remaining',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'user_email',
            'user_name',
            'status_display',
            'is_currently_active',
            'days_remaining',
            'cancelled_at',
        ]

    def get_user_name(self, obj):
        """
        Get user's full name.
        """
        if obj.user:
            return obj.user.get_full_name() or obj.user.email
        return None

    def get_is_currently_active(self, obj):
        """
        Check if subscription is currently active.
        """
        return obj.is_currently_active()

    def get_days_remaining(self, obj):
        """
        Calculate days remaining in subscription.
        """
        if not obj.is_active or obj.status == 'cancelled':
            return 0
        
        today = timezone.now().date()
        if obj.end_date and obj.end_date >= today:
            return (obj.end_date - today).days
        return 0


