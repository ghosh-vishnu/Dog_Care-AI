from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Pet model with delete protection.
    """
    list_display = [
        'name',
        'pet_type',
        'breed',
        'age',
        'weight',
        'gender',
        'owner',
        'get_owner_email',
        'is_deleted',
        'get_status_badge',
        'created_at',
    ]
    list_filter = [
        'pet_type',
        'gender',
        'is_deleted',
        'created_at',
        'deleted_at',
    ]
    search_fields = [
        'name',
        'breed',
        'microchip_number',
        'owner__email',
        'owner__first_name',
        'owner__last_name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'deleted_at',
        'profile_picture_preview',
        'get_health_records_count',
        'get_vaccinations_count',
    ]
    ordering = ['-created_at']
    raw_id_fields = ['owner']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Owner Information'), {
            'fields': ('owner',)
        }),
        (_('Basic Information'), {
            'fields': (
                'name',
                'pet_type',
                'breed',
                'gender',
            )
        }),
        (_('Physical Details'), {
            'fields': (
                'age',
                'weight',
                'date_of_birth',
                'color',
                'profile_picture',
                'profile_picture_preview',
            )
        }),
        (_('Identification'), {
            'fields': ('microchip_number',)
        }),
        (_('Additional Information'), {
            'fields': ('notes',)
        }),
        (_('Statistics'), {
            'fields': (
                'get_health_records_count',
                'get_vaccinations_count',
            ),
            'classes': ('collapse',),
        }),
        (_('Status'), {
            'fields': (
                'is_deleted',
                'deleted_at',
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
        return qs.select_related('owner').prefetch_related(
            'health_records',
            'vaccinations'
        )

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
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">DELETED</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">ACTIVE</span>'
        )
    get_status_badge.short_description = 'Status'
    get_status_badge.admin_order_field = 'is_deleted'

    def profile_picture_preview(self, obj):
        """
        Display profile picture preview in admin.
        """
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 5px;" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    profile_picture_preview.short_description = 'Profile Picture Preview'

    def get_health_records_count(self, obj):
        """
        Display count of health records.
        """
        count = obj.health_records.count()
        if count > 0:
            url = reverse('admin:health_healthrecord_changelist') + f'?pet__id__exact={obj.id}'
            return format_html('<a href="{}">{} record(s)</a>', url, count)
        return '0 records'
    get_health_records_count.short_description = 'Health Records'

    def get_vaccinations_count(self, obj):
        """
        Display count of vaccinations.
        """
        count = obj.vaccinations.count()
        if count > 0:
            url = reverse('admin:health_vaccination_changelist') + f'?pet__id__exact={obj.id}'
            return format_html('<a href="{}">{} vaccination(s)</a>', url, count)
        return '0 vaccinations'
    get_vaccinations_count.short_description = 'Vaccinations'

    def get_readonly_fields(self, request, obj=None):
        """
        Make owner readonly if pet is being edited.
        """
        readonly = list(self.readonly_fields)
        if obj:
            readonly.append('owner')
        return readonly

    def delete_model(self, request, obj):
        """
        Prevent hard delete, use soft delete instead.
        """
        if not obj.is_deleted:
            obj.delete()
            self.message_user(
                request,
                _('Pet has been soft-deleted. Use "Permanently delete" action to remove completely.'),
                messages.WARNING
            )
        else:
            messages.error(
                request,
                _('Pet is already deleted. Use "Permanently delete" action to remove completely.')
            )

    def delete_queryset(self, request, queryset):
        """
        Prevent bulk hard delete, use soft delete instead.
        """
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
        
        self.message_user(
            request,
            _('Selected pets have been soft-deleted. Use "Permanently delete" action to remove completely.'),
            messages.WARNING
        )

    actions = ['restore_pets', 'hard_delete_pets']

    def restore_pets(self, request, queryset):
        """
        Admin action to restore soft-deleted pets.
        """
        restored_count = 0
        for pet in queryset.filter(is_deleted=True):
            pet.restore()
            restored_count += 1
        
        if restored_count > 0:
            self.message_user(
                request,
                _('Successfully restored %(count)d pet(s).') % {'count': restored_count},
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                _('No deleted pets selected.'),
                messages.WARNING
            )
    restore_pets.short_description = _('Restore selected pets')

    def hard_delete_pets(self, request, queryset):
        """
        Admin action to permanently delete pets with confirmation.
        """
        count = queryset.count()
        if count == 0:
            self.message_user(
                request,
                _('No pets selected.'),
                messages.WARNING
            )
            return
        
        deleted_count = 0
        for pet in queryset:
            pet.hard_delete()
            deleted_count += 1
        
        self.message_user(
            request,
            _('Successfully deleted %(count)d pet(s) permanently. This action cannot be undone.') % {'count': deleted_count},
            messages.WARNING
        )
    hard_delete_pets.short_description = _('⚠️ Permanently delete selected pets (IRREVERSIBLE)')
