from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """
    Subscription plan model for Free and Premium plans.
    Admin can manage plans.
    """
    PLAN_TYPES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
    ]

    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPES,
        unique=True,
        db_index=True,
        help_text='Type of subscription plan'
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Display name of the plan'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Description of the plan features'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Price of the plan (0.00 for free plan)'
    )
    duration_days = models.PositiveIntegerField(
        default=30,
        help_text='Duration of the subscription in days'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Whether this plan is currently active and available'
    )
    features = models.JSONField(
        default=list,
        blank=True,
        help_text='List of features included in this plan'
    )
    max_pets = models.PositiveIntegerField(
        default=1,
        help_text='Maximum number of pets allowed in this plan'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscription_plans'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['plan_type', 'name']
        indexes = [
            models.Index(fields=['plan_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"

    def clean(self):
        """
        Validate subscription plan data.
        """
        if self.plan_type == 'free' and self.price > 0:
            raise ValidationError({
                'price': 'Free plan must have price 0.00.'
            })
        
        if self.duration_days <= 0:
            raise ValidationError({
                'duration_days': 'Duration must be greater than 0.'
            })
        
        if self.max_pets <= 0:
            raise ValidationError({
                'max_pets': 'Maximum pets must be greater than 0.'
            })

    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)


class UserSubscription(models.Model):
    """
    User subscription model linking users to subscription plans.
    Tracks start date, end date, and active status.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        db_index=True
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='user_subscriptions',
        db_index=True
    )
    start_date = models.DateField(
        db_index=True,
        help_text='Start date of the subscription'
    )
    end_date = models.DateField(
        db_index=True,
        help_text='End date of the subscription'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True,
        help_text='Current status of the subscription'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Whether this subscription is currently active'
    )
    auto_renew = models.BooleanField(
        default=False,
        help_text='Whether subscription should auto-renew'
    )
    cancelled_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Date and time when subscription was cancelled'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_subscriptions'
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
        ordering = ['-start_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['end_date', 'status']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.start_date} to {self.end_date})"

    def clean(self):
        """
        Validate subscription data.
        """
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({
                    'end_date': 'End date must be after start date.'
                })
            
            today = timezone.now().date()
            if self.start_date > today:
                raise ValidationError({
                    'start_date': 'Start date cannot be in the future.'
                })

    def save(self, *args, **kwargs):
        """
        Override save to update status and is_active based on dates.
        """
        self.full_clean()
        
        today = timezone.now().date()
        
        if self.start_date and self.end_date:
            if self.status != 'cancelled':
                if today < self.start_date:
                    self.status = 'active'
                    self.is_active = False
                elif today >= self.start_date and today <= self.end_date:
                    self.status = 'active'
                    self.is_active = True
                else:
                    self.status = 'expired'
                    self.is_active = False
        
        if self.status == 'cancelled':
            self.is_active = False
            if not self.cancelled_at:
                self.cancelled_at = timezone.now()
        
        super().save(*args, **kwargs)

    def cancel(self):
        """
        Cancel the subscription.
        """
        self.status = 'cancelled'
        self.is_active = False
        self.cancelled_at = timezone.now()
        self.save()

    def is_currently_active(self):
        """
        Check if subscription is currently active based on dates.
        """
        if self.status == 'cancelled':
            return False
        
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
