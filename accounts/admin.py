from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tenant, UserProfile


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at', 'user_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_tenant', 'get_role', 'is_staff']
    list_filter = ['profile__role', 'profile__tenant', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    def get_tenant(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.tenant
        return '-'
    get_tenant.short_description = 'Tenant'
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return '-'
    get_role.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
