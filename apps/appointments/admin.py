from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Appointment model with proper hardening.
    """
    list_display = [
        'pet',
        'owner',
        'get_owner_email',
        'veterinarian',
        'appointment_date',
        'get_status_badge',
        'get_time_until_appointment',
        'created_at',
    ]
    list_filter = [
        'status',
        'appointment_date',
        'created_at',
    ]
    search_fields = [
        'pet__name',
        'owner__email',
        'owner__first_name',
        'owner__last_name',
        'veterinarian__email',
        'veterinarian__first_name',
        'veterinarian__last_name',
        'reason',
        'notes',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_status_badge',
    ]
    date_hierarchy = 'appointment_date'
    raw_id_fields = ['pet', 'owner', 'veterinarian']
    list_per_page = 25
    ordering = ['-appointment_date', '-created_at']

    fieldsets = (
        (_('Appointment Details'), {
            'fields': (
                'pet',
                'owner',
                'veterinarian',
                'appointment_date',
                'status',
                'get_status_badge',
            )
        }),
        (_('Information'), {
            'fields': (
                'reason',
                'notes',
            )
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
        Optimize queryset for admin list view.
        """
        qs = super().get_queryset(request)
        return qs.select_related('pet', 'pet__owner', 'owner', 'veterinarian')

    def get_owner_email(self, obj):
        """
        Display owner email.
        """
        return obj.owner.email if obj.owner else '-'
    get_owner_email.short_description = 'Owner Email'
    get_owner_email.admin_order_field = 'owner__email'

    def get_status_badge(self, obj):
        """
        Display status badge with color coding.
        """
        status_colors = {
            'scheduled': '#17a2b8',
            'confirmed': '#28a745',
            'in_progress': '#ffc107',
            'completed': '#6c757d',
            'cancelled': '#dc3545',
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    get_status_badge.short_description = 'Status Badge'

    def get_time_until_appointment(self, obj):
        """
        Display time until appointment.
        """
        from django.utils import timezone
        now = timezone.now()
        if obj.appointment_date:
            if obj.appointment_date > now:
                delta = obj.appointment_date - now
                days = delta.days
                hours = delta.seconds // 3600
                if days > 0:
                    return format_html(
                        '<span style="color: #17a2b8;">{} days, {} hours</span>',
                        days,
                        hours
                    )
                elif hours > 0:
                    return format_html(
                        '<span style="color: #ffc107;">{} hours</span>',
                        hours
                    )
                else:
                    return format_html(
                        '<span style="color: #dc3545; font-weight: bold;">UPCOMING</span>'
                    )
            else:
                return format_html(
                    '<span style="color: #6c757d;">PAST</span>'
                )
        return '-'
    get_time_until_appointment.short_description = 'Time Until'

    def delete_model(self, request, obj):
        """
        Add confirmation message before deletion.
        """
        if obj.status == 'completed':
            messages.warning(
                request,
                _('Deleting a completed appointment. This action cannot be undone.')
            )
        super().delete_model(request, obj)

    actions = ['mark_completed', 'cancel_appointments']

    def mark_completed(self, request, queryset):
        """
        Admin action to mark appointments as completed.
        """
        count = queryset.exclude(status='completed').update(status='completed')
        self.message_user(
            request,
            _('Successfully marked %(count)d appointment(s) as completed.') % {'count': count},
            messages.SUCCESS
        )
    mark_completed.short_description = _('Mark selected appointments as completed')

    def cancel_appointments(self, request, queryset):
        """
        Admin action to cancel appointments.
        """
        count = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(
            request,
            _('Successfully cancelled %(count)d appointment(s).') % {'count': count},
            messages.WARNING
        )
    cancel_appointments.short_description = _('Cancel selected appointments')
