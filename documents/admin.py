from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'document_type', 'uploaded_by', 'file_size_display', 'created_at', 'tenant']
    list_filter = ['document_type', 'tenant', 'created_at', 'client']
    search_fields = ['title', 'description', 'client__first_name', 'client__last_name', 'client__email']
    readonly_fields = ['created_at', 'updated_at', 'uploaded_by', 'file_size_display']
    fieldsets = (
        ('Document Information', {
            'fields': ('tenant', 'client', 'title', 'document_type', 'description')
        }),
        ('File', {
            'fields': ('file', 'file_size_display')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def file_size_display(self, obj):
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    file_size_display.short_description = 'File Size'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter by tenant for non-superusers
        if hasattr(request.user, 'profile'):
            return qs.filter(tenant=request.user.profile.tenant)
        return qs.none()
