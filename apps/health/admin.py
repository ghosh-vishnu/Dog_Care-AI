from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from .models import Vaccination, HealthRecord


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Vaccination model with better UX.
    """
    list_display = [
        'vaccine_name',
        'pet',
        'pet_owner',
        'due_date',
        'get_status_badge',
        'administered_date',
        'get_days_overdue',
        'veterinarian',
        'created_at',
    ]
    list_filter = [
        'status',
        'due_date',
        'administered_date',
        'created_at',
    ]
    search_fields = [
        'vaccine_name',
        'pet__name',
        'pet__owner__email',
        'pet__owner__first_name',
        'pet__owner__last_name',
        'batch_number',
        'notes',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_status_badge',
    ]
    date_hierarchy = 'due_date'
    raw_id_fields = ['pet', 'veterinarian']
    list_per_page = 25
    ordering = ['-due_date', '-created_at']

    fieldsets = (
        (_('Pet Information'), {
            'fields': ('pet',)
        }),
        (_('Vaccination Details'), {
            'fields': (
                'vaccine_name',
                'due_date',
                'status',
                'get_status_badge',
                'administered_date',
                'batch_number',
            )
        }),
        (_('Additional Information'), {
            'fields': (
                'veterinarian',
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
        Optimize queryset with select_related.
        """
        qs = super().get_queryset(request)
        return qs.select_related('pet', 'pet__owner', 'veterinarian')

    def pet_owner(self, obj):
        """
        Display pet owner information with link.
        """
        if obj.pet and obj.pet.owner:
            url = reverse('admin:accounts_user_change', args=[obj.pet.owner.id])
            return format_html(
                '<a href="{}">{} ({})</a>',
                url,
                obj.pet.owner.get_full_name() or obj.pet.owner.email,
                obj.pet.owner.email
            )
        return '-'
    pet_owner.short_description = 'Pet Owner'
    pet_owner.admin_order_field = 'pet__owner__email'

    def get_status_badge(self, obj):
        """
        Display status badge with color coding.
        """
        status_colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'overdue': '#dc3545',
            'scheduled': '#17a2b8',
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    get_status_badge.short_description = 'Status Badge'

    def get_days_overdue(self, obj):
        """
        Display days overdue for pending/overdue vaccinations.
        """
        from django.utils import timezone
        if obj.status in ['pending', 'overdue'] and obj.due_date:
            today = timezone.now().date()
            if obj.due_date < today:
                days = (today - obj.due_date).days
                return format_html(
                    '<span style="color: #dc3545; font-weight: bold;">{} days</span>',
                    days
                )
        return '-'
    get_days_overdue.short_description = 'Days Overdue'

    def delete_model(self, request, obj):
        """
        Add confirmation message before deletion.
        """
        self.message_user(
            request,
            _('Vaccination record deleted. This action cannot be undone.'),
            messages.WARNING
        )
        super().delete_model(request, obj)


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for HealthRecord model with better UX.
    """
    list_display = [
        'pet',
        'pet_owner',
        'weight',
        'record_date',
        'temperature',
        'heart_rate',
        'get_vital_signs_status',
        'veterinarian',
        'created_at',
    ]
    list_filter = [
        'record_date',
        'created_at',
    ]
    search_fields = [
        'pet__name',
        'pet__owner__email',
        'pet__owner__first_name',
        'pet__owner__last_name',
        'notes',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_vital_signs_status',
    ]
    date_hierarchy = 'record_date'
    raw_id_fields = ['pet', 'veterinarian']
    list_per_page = 25
    ordering = ['-record_date', '-created_at']

    fieldsets = (
        (_('Pet Information'), {
            'fields': ('pet',)
        }),
        (_('Health Data'), {
            'fields': (
                'weight',
                'temperature',
                'heart_rate',
                'record_date',
                'get_vital_signs_status',
            )
        }),
        (_('Additional Information'), {
            'fields': (
                'veterinarian',
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
        Optimize queryset with select_related.
        """
        qs = super().get_queryset(request)
        return qs.select_related('pet', 'pet__owner', 'veterinarian')

    def pet_owner(self, obj):
        """
        Display pet owner information with link.
        """
        if obj.pet and obj.pet.owner:
            url = reverse('admin:accounts_user_change', args=[obj.pet.owner.id])
            return format_html(
                '<a href="{}">{} ({})</a>',
                url,
                obj.pet.owner.get_full_name() or obj.pet.owner.email,
                obj.pet.owner.email
            )
        return '-'
    pet_owner.short_description = 'Pet Owner'
    pet_owner.admin_order_field = 'pet__owner__email'

    def get_vital_signs_status(self, obj):
        """
        Display vital signs status with color coding.
        """
        if not obj.temperature and not obj.heart_rate:
            return format_html('<span style="color: #999;">No vital signs recorded</span>')
        
        status_parts = []
        if obj.temperature:
            if 37.5 <= float(obj.temperature) <= 39.5:
                temp_color = '#28a745'
            else:
                temp_color = '#dc3545'
            status_parts.append(
                format_html(
                    '<span style="color: {};">Temp: {}°C</span>',
                    temp_color,
                    obj.temperature
                )
            )
        
        if obj.heart_rate:
            if 60 <= obj.heart_rate <= 180:
                hr_color = '#28a745'
            else:
                hr_color = '#dc3545'
            status_parts.append(
                format_html(
                    '<span style="color: {};">HR: {} bpm</span>',
                    hr_color,
                    obj.heart_rate
                )
            )
        
        return format_html(' | '.join(str(part) for part in status_parts))
    get_vital_signs_status.short_description = 'Vital Signs'

    def delete_model(self, request, obj):
        """
        Add confirmation message before deletion.
        """
        self.message_user(
            request,
            _('Health record deleted. This action cannot be undone.'),
            messages.WARNING
        )
        super().delete_model(request, obj)
