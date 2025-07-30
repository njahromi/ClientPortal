from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'status', 'tenant', 'created_by', 'created_at', 'total_tasks', 'pending_tasks']
    list_filter = ['status', 'tenant', 'created_at', 'company']
    search_fields = ['first_name', 'last_name', 'email', 'company', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Status & Details', {
            'fields': ('status', 'address', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter by tenant for non-superusers
        if hasattr(request.user, 'profile'):
            return qs.filter(tenant=request.user.profile.tenant)
        return qs.none()
