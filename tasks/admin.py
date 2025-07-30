from django.contrib import admin
from .models import Task, TaskComment


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'status', 'priority', 'assigned_to', 'due_date', 'is_overdue', 'tenant']
    list_filter = ['status', 'priority', 'tenant', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'client__first_name', 'client__last_name', 'client__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'completed_at']
    inlines = [TaskCommentInline]
    fieldsets = (
        ('Task Information', {
            'fields': ('tenant', 'client', 'title', 'description', 'status', 'priority')
        }),
        ('Assignment & Dates', {
            'fields': ('assigned_to', 'due_date', 'completed_at')
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


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'task__title', 'author__username']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
