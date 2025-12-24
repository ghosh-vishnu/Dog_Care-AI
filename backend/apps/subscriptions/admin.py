from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for SubscriptionPlan model with proper hardening.
    """
    list_display = [
        'name',
        'plan_type',
        'get_plan_type_badge',
        'price',
        'duration_days',
        'max_pets',
        'is_active',
        'get_active_badge',
        'get_subscribers_count',
        'created_at',
    ]
    list_filter = [
        'plan_type',
        'is_active',
        'created_at',
    ]
    search_fields = [
        'name',
        'description',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_plan_type_badge',
        'get_active_badge',
        'get_subscribers_count',
    ]
    list_per_page = 25
    ordering = ['plan_type', 'name']

    fieldsets = (
        (_('Plan Information'), {
            'fields': (
                'plan_type',
                'get_plan_type_badge',
                'name',
                'description',
            )
        }),
        (_('Pricing & Duration'), {
            'fields': (
                'price',
                'duration_days',
            )
        }),
        (_('Features & Limits'), {
            'fields': (
                'max_pets',
                'features',
            )
        }),
        (_('Status'), {
            'fields': (
                'is_active',
                'get_active_badge',
            )
        }),
        (_('Statistics'), {
            'fields': ('get_subscribers_count',),
            'classes': ('collapse',),
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def get_queryset(self, request):
        """
        Optimize queryset with subscriber count.
        """
        from django.db.models import Count
        qs = super().get_queryset(request)
        return qs.annotate(subscribers_count=Count('user_subscriptions'))

    def get_plan_type_badge(self, obj):
        """
        Display plan type badge with color coding.
        """
        colors = {
            'free': '#28a745',
            'premium': '#ffc107',
        }
        color = colors.get(obj.plan_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_plan_type_display().upper()
        )
    get_plan_type_badge.short_description = 'Plan Type'

    def get_active_badge(self, obj):
        """
        Display active status badge.
        """
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">INACTIVE</span>'
        )
    get_active_badge.short_description = 'Status'

    def get_subscribers_count(self, obj):
        """
        Display count of active subscribers.
        """
        count = obj.user_subscriptions.filter(is_active=True, status='active').count()
        if count > 0:
            url = reverse('admin:subscriptions_usersubscription_changelist') + f'?plan__id__exact={obj.id}'
            return format_html('<a href="{}">{} active subscriber(s)</a>', url, count)
        return '0 subscribers'
    get_subscribers_count.short_description = 'Active Subscribers'

    def delete_model(self, request, obj):
        """
        Prevent deletion of plans with active subscriptions.
        """
        active_count = obj.user_subscriptions.filter(is_active=True, status='active').count()
        if active_count > 0:
            messages.error(
                request,
                _('Cannot delete plan with %(count)d active subscription(s). Deactivate the plan instead.') % {'count': active_count}
            )
            return
        
        self.message_user(
            request,
            _('Subscription plan deleted. This action cannot be undone.'),
            messages.WARNING
        )
        super().delete_model(request, obj)

    actions = ['activate_plans', 'deactivate_plans']

    def activate_plans(self, request, queryset):
        """
        Admin action to activate plans.
        """
        count = queryset.update(is_active=True)
        self.message_user(
            request,
            _('Successfully activated %(count)d plan(s).') % {'count': count},
            messages.SUCCESS
        )
    activate_plans.short_description = _('Activate selected plans')

    def deactivate_plans(self, request, queryset):
        """
        Admin action to deactivate plans.
        """
        count = queryset.update(is_active=False)
        self.message_user(
            request,
            _('Successfully deactivated %(count)d plan(s).') % {'count': count},
            messages.WARNING
        )
    deactivate_plans.short_description = _('Deactivate selected plans')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for UserSubscription model with proper hardening.
    """
    list_display = [
        'user',
        'get_user_email',
        'plan',
        'get_plan_type',
        'start_date',
        'end_date',
        'get_status_badge',
        'is_active',
        'get_days_remaining',
        'auto_renew',
        'created_at',
    ]
    list_filter = [
        'status',
        'is_active',
        'auto_renew',
        'plan',
        'start_date',
        'end_date',
        'created_at',
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'plan__name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'cancelled_at',
        'get_status_badge',
        'get_days_remaining',
    ]
    date_hierarchy = 'start_date'
    raw_id_fields = ['user', 'plan']
    list_per_page = 25
    ordering = ['-start_date', '-created_at']

    fieldsets = (
        (_('User & Plan'), {
            'fields': (
                'user',
                'plan',
            )
        }),
        (_('Subscription Period'), {
            'fields': (
                'start_date',
                'end_date',
                'get_days_remaining',
            )
        }),
        (_('Status'), {
            'fields': (
                'status',
                'get_status_badge',
                'is_active',
                'auto_renew',
            )
        }),
        (_('Cancellation'), {
            'fields': ('cancelled_at',)
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def get_queryset(self, request):
        """
        Optimize queryset with select_related.
        """
        qs = super().get_queryset(request)
        return qs.select_related('user', 'plan')

    def get_user_email(self, obj):
        """
        Display user email with link.
        """
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.id])
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.user.email
            )
        return '-'
    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'

    def get_plan_type(self, obj):
        """
        Display plan type.
        """
        if obj.plan:
            return obj.plan.get_plan_type_display()
        return '-'
    get_plan_type.short_description = 'Plan Type'
    get_plan_type.admin_order_field = 'plan__plan_type'

    def get_status_badge(self, obj):
        """
        Display status badge with color coding.
        """
        status_colors = {
            'active': '#28a745',
            'expired': '#6c757d',
            'cancelled': '#dc3545',
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    get_status_badge.short_description = 'Status Badge'

    def get_days_remaining(self, obj):
        """
        Display days remaining in subscription.
        """
        if obj.is_active and obj.status == 'active' and obj.end_date:
            today = timezone.now().date()
            if obj.end_date >= today:
                days = (obj.end_date - today).days
                if days > 30:
                    color = '#28a745'
                elif days > 7:
                    color = '#ffc107'
                else:
                    color = '#dc3545'
                return format_html(
                    '<span style="color: {}; font-weight: bold;">{} days remaining</span>',
                    color,
                    days
                )
        return format_html('<span style="color: #999;">N/A</span>')
    get_days_remaining.short_description = 'Days Remaining'

    def delete_model(self, request, obj):
        """
        Add confirmation message before deletion.
        """
        if obj.is_active:
            messages.warning(
                request,
                _('Deleting an active subscription. This action cannot be undone.')
            )
        super().delete_model(request, obj)

    actions = ['cancel_subscriptions', 'activate_subscriptions']

    def cancel_subscriptions(self, request, queryset):
        """
        Admin action to cancel subscriptions.
        """
        cancelled_count = 0
        for subscription in queryset.exclude(status='cancelled'):
            subscription.cancel()
            cancelled_count += 1
        
        self.message_user(
            request,
            _('Successfully cancelled %(count)d subscription(s).') % {'count': cancelled_count},
            messages.WARNING
        )
    cancel_subscriptions.short_description = _('Cancel selected subscriptions')

    def activate_subscriptions(self, request, queryset):
        """
        Admin action to activate subscriptions.
        """
        count = queryset.update(status='active', is_active=True)
        self.message_user(
            request,
            _('Successfully activated %(count)d subscription(s).') % {'count': count},
            messages.SUCCESS
        )
    activate_subscriptions.short_description = _('Activate selected subscriptions')
