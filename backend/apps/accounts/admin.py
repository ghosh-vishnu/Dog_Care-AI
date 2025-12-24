from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.db.models import Count
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced admin interface for custom User model with proper hardening.
    """
    list_display = [
        'email',
        'get_full_name_display',
        'role',
        'is_veterinarian',
        'is_active',
        'is_staff',
        'date_joined',
        'last_login',
        'get_pets_count',
        'get_subscription_status',
    ]
    list_filter = [
        'role',
        'is_veterinarian',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
    ]
    search_fields = [
        'email',
        'first_name',
        'last_name',
        'phone_number',
    ]
    ordering = ['-date_joined']
    readonly_fields = [
        'date_joined',
        'last_login',
        'created_at',
        'updated_at',
        'profile_picture_preview',
        'get_pets_count',
        'get_subscription_status',
    ]
    list_per_page = 25
    list_select_related = True

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'profile_picture',
                'profile_picture_preview',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'role',
                'is_veterinarian',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Statistics'), {
            'fields': (
                'get_pets_count',
                'get_subscription_status',
            ),
            'classes': ('collapse',),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined',
                'created_at',
                'updated_at',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'role',
                'is_veterinarian',
            ),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
    actions = ['deactivate_users', 'activate_users']

    def get_full_name_display(self, obj):
        """
        Display full name or email if name is not available.
        """
        return obj.get_full_name() or obj.email
    get_full_name_display.short_description = 'Full Name'
    get_full_name_display.admin_order_field = 'first_name'

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

    def get_pets_count(self, obj):
        """
        Display count of pets owned by user.
        """
        count = obj.pets.count()
        if count > 0:
            url = reverse('admin:pets_pet_changelist') + f'?owner__id__exact={obj.id}'
            return format_html('<a href="{}">{} pet(s)</a>', url, count)
        return '0 pets'
    get_pets_count.short_description = 'Pets Count'
    get_pets_count.admin_order_field = 'pets__count'

    def get_subscription_status(self, obj):
        """
        Display current subscription status.
        """
        from apps.subscriptions.models import UserSubscription
        subscription = UserSubscription.objects.filter(
            user=obj,
            is_active=True,
            status='active'
        ).first()
        
        if subscription:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                subscription.plan.name
            )
        return format_html('<span style="color: #999;">No active subscription</span>')
    get_subscription_status.short_description = 'Subscription'

    def get_queryset(self, request):
        """
        Optimize queryset for admin list view.
        """
        qs = super().get_queryset(request)
        return qs.select_related().prefetch_related(
            'groups',
            'user_permissions',
            'pets'
        ).annotate(
            pets_count=Count('pets')
        )

    def save_model(self, request, obj, form, change):
        """
        Override save to handle role consistency and prevent unsafe changes.
        """
        if obj.is_superuser:
            obj.role = User.Role.ADMIN
            obj.is_staff = True
        
        if change:
            old_obj = User.objects.get(pk=obj.pk)
            if old_obj.is_superuser and not obj.is_superuser:
                messages.warning(
                    request,
                    _('Removing superuser status may affect system access.')
                )
        
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Prevent deletion of superusers and add confirmation.
        """
        if obj.is_superuser:
            messages.error(
                request,
                _('Cannot delete superuser accounts. Deactivate instead.')
            )
            return
        
        if obj == request.user:
            messages.error(
                request,
                _('You cannot delete your own account.')
            )
            return
        
        super().delete_model(request, obj)

    def deactivate_users(self, request, queryset):
        """
        Admin action to deactivate users safely.
        """
        count = queryset.update(is_active=False)
        self.message_user(
            request,
            _('Successfully deactivated %(count)d user(s).') % {'count': count},
            messages.SUCCESS
        )
    deactivate_users.short_description = _('Deactivate selected users')

    def activate_users(self, request, queryset):
        """
        Admin action to activate users.
        """
        count = queryset.update(is_active=True)
        self.message_user(
            request,
            _('Successfully activated %(count)d user(s).') % {'count': count},
            messages.SUCCESS
        )
    activate_users.short_description = _('Activate selected users')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for UserProfile model.
    """
    list_display = [
        'user',
        'get_user_email',
        'phone',
        'location',
        'is_active',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone',
        'location',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    ordering = ['-created_at']
    raw_id_fields = ['user']
    list_per_page = 25

    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Profile Information'), {
            'fields': (
                'phone',
                'location',
                'is_active',
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def get_user_email(self, obj):
        """
        Display user email.
        """
        return obj.user.email if obj.user else '-'
    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'

    def get_queryset(self, request):
        """
        Optimize queryset for admin list view.
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')
