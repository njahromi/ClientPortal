from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from clients.models import Client
from tasks.models import Task
from documents.models import Document


@login_required
def dashboard(request):
    """Main dashboard view with overview statistics"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    
    # Get date ranges
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Client statistics
    total_clients = Client.objects.filter(tenant=tenant).count()
    active_clients = Client.objects.filter(tenant=tenant, status='active').count()
    new_clients_this_month = Client.objects.filter(
        tenant=tenant, 
        created_at__date__gte=thirty_days_ago
    ).count()
    
    # Task statistics
    total_tasks = Task.objects.filter(tenant=tenant).count()
    pending_tasks = Task.objects.filter(tenant=tenant, status='pending').count()
    overdue_tasks = Task.objects.filter(
        tenant=tenant,
        status__in=['pending', 'in_progress'],
        due_date__lt=timezone.now()
    ).count()
    tasks_due_today = Task.objects.filter(
        tenant=tenant,
        status__in=['pending', 'in_progress'],
        due_date__date=today
    ).count()
    
    # Document statistics
    total_documents = Document.objects.filter(tenant=tenant).count()
    documents_this_month = Document.objects.filter(
        tenant=tenant,
        created_at__date__gte=thirty_days_ago
    ).count()
    
    # Recent activity
    recent_clients = Client.objects.filter(tenant=tenant).order_by('-created_at')[:5]
    recent_tasks = Task.objects.filter(tenant=tenant).order_by('-created_at')[:5]
    recent_documents = Document.objects.filter(tenant=tenant).order_by('-created_at')[:5]
    
    # Tasks by status
    tasks_by_status = Task.objects.filter(tenant=tenant).values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Clients by status
    clients_by_status = Client.objects.filter(tenant=tenant).values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'new_clients_this_month': new_clients_this_month,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_due_today': tasks_due_today,
        'total_documents': total_documents,
        'documents_this_month': documents_this_month,
        'recent_clients': recent_clients,
        'recent_tasks': recent_tasks,
        'recent_documents': recent_documents,
        'tasks_by_status': tasks_by_status,
        'clients_by_status': clients_by_status,
    }
    
    return render(request, 'dashboard.html', context) 