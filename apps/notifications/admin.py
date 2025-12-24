from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Notification model with proper hardening.
    """
    list_display = [
        'user',
        'get_user_email',
        'notification_type',
        'get_type_badge',
        'title',
        'is_read',
        'get_read_badge',
        'created_at',
    ]
    list_filter = [
        'notification_type',
        'is_read',
        'created_at',
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'title',
        'message',
    ]
    readonly_fields = [
        'created_at',
        'get_type_badge',
        'get_read_badge',
    ]
    date_hierarchy = 'created_at'
    raw_id_fields = ['user']
    list_per_page = 25
    ordering = ['-created_at']

    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Notification Details'), {
            'fields': (
                'notification_type',
                'get_type_badge',
                'title',
                'message',
                'is_read',
                'get_read_badge',
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at',)
        }),
    )

    def get_queryset(self, request):
        """
        Optimize queryset for admin list view.
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')

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

    def get_type_badge(self, obj):
        """
        Display notification type badge with color coding.
        """
        type_colors = {
            'appointment_reminder': '#17a2b8',
            'vaccination_due': '#ffc107',
            'medication_reminder': '#dc3545',
            'health_update': '#28a745',
            'system': '#6c757d',
            'other': '#6c757d',
        }
        color = type_colors.get(obj.notification_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_notification_type_display()
        )
    get_type_badge.short_description = 'Type Badge'

    def get_read_badge(self, obj):
        """
        Display read status badge.
        """
        if obj.is_read:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">READ</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">UNREAD</span>'
        )
    get_read_badge.short_description = 'Read Status'

    def delete_model(self, request, obj):
        """
        Add confirmation message before deletion.
        """
        self.message_user(
            request,
            _('Notification deleted. This action cannot be undone.'),
            messages.WARNING
        )
        super().delete_model(request, obj)

    actions = ['mark_as_read', 'mark_as_unread', 'delete_read_notifications']

    def mark_as_read(self, request, queryset):
        """
        Admin action to mark notifications as read.
        """
        count = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(
            request,
            _('Successfully marked %(count)d notification(s) as read.') % {'count': count},
            messages.SUCCESS
        )
    mark_as_read.short_description = _('Mark selected notifications as read')

    def mark_as_unread(self, request, queryset):
        """
        Admin action to mark notifications as unread.
        """
        count = queryset.filter(is_read=True).update(is_read=False)
        self.message_user(
            request,
            _('Successfully marked %(count)d notification(s) as unread.') % {'count': count},
            messages.SUCCESS
        )
    mark_as_unread.short_description = _('Mark selected notifications as unread')

    def delete_read_notifications(self, request, queryset):
        """
        Admin action to delete read notifications.
        """
        count = queryset.filter(is_read=True).count()
        queryset.filter(is_read=True).delete()
        self.message_user(
            request,
            _('Successfully deleted %(count)d read notification(s).') % {'count': count},
            messages.WARNING
        )
    delete_read_notifications.short_description = _('Delete selected read notifications')
