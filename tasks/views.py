from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, TaskComment
from .forms import TaskForm, TaskCommentForm, TaskSearchForm
from clients.models import Client


@login_required
def task_list(request):
    """List all tasks for the current tenant with search and filtering"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    tasks = Task.objects.filter(tenant=tenant)
    
    # Handle search and filtering
    search_form = TaskSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        status = search_form.cleaned_data.get('status')
        priority = search_form.cleaned_data.get('priority')
        assigned_to = search_form.cleaned_data.get('assigned_to')
        
        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(client__first_name__icontains=search) |
                Q(client__last_name__icontains=search)
            )
        
        if status:
            tasks = tasks.filter(status=status)
        
        if priority:
            tasks = tasks.filter(priority=priority)
        
        if assigned_to:
            tasks = tasks.filter(assigned_to=assigned_to)
    
    # Pagination
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_tasks': tasks.count(),
        'pending_tasks': tasks.filter(status='pending').count(),
        'overdue_tasks': tasks.filter(status__in=['pending', 'in_progress'], due_date__lt=timezone.now()).count(),
    }
    
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    """Show detailed view of a task with comments"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    task = get_object_or_404(Task, pk=pk, tenant=tenant)
    
    # Handle comment form
    if request.method == 'POST':
        comment_form = TaskCommentForm(request.POST, user=request.user)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        comment_form = TaskCommentForm(user=request.user)
    
    context = {
        'task': task,
        'comment_form': comment_form,
        'comments': task.comments.all(),
    }
    
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    """Create a new task"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" created successfully.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Add New Task',
    }
    
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, pk):
    """Update an existing task"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    task = get_object_or_404(Task, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" updated successfully.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user)
    
    context = {
        'form': form,
        'task': task,
        'title': f'Edit Task: {task.title}',
    }
    
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_delete(request, pk):
    """Delete a task"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    task = get_object_or_404(Task, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully.')
        return redirect('tasks:task_list')
    
    context = {
        'task': task,
    }
    
    return render(request, 'tasks/task_confirm_delete.html', context)


@login_required
def task_complete(request, pk):
    """Mark a task as completed"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    task = get_object_or_404(Task, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        task.mark_completed()
        messages.success(request, f'Task "{task.title}" marked as completed.')
        return redirect('tasks:task_detail', pk=task.pk)
    
    context = {
        'task': task,
    }
    
    return render(request, 'tasks/task_confirm_complete.html', context)


@login_required
def task_comment(request, pk):
    """Add a comment to a task via AJAX"""
    if not hasattr(request.user, 'profile'):
        return JsonResponse({'error': 'User profile not found'}, status=400)
    
    tenant = request.user.profile.tenant
    task = get_object_or_404(Task, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        form = TaskCommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            return JsonResponse({
                'success': True,
                'comment': {
                    'author': comment.author.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })
        else:
            return JsonResponse({'error': 'Invalid comment data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
