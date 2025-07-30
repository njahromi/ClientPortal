from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Client
from .forms import ClientForm, ClientSearchForm
from tasks.models import Task
from documents.models import Document


@login_required
def client_list(request):
    """List all clients for the current tenant with search and filtering"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    clients = Client.objects.filter(tenant=tenant)
    
    # Handle search and filtering
    search_form = ClientSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        status = search_form.cleaned_data.get('status')
        company = search_form.cleaned_data.get('company')
        
        if search:
            clients = clients.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search)
            )
        
        if status:
            clients = clients.filter(status=status)
        
        if company:
            clients = clients.filter(company__icontains=company)
    
    # Pagination
    paginator = Paginator(clients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_clients': clients.count(),
    }
    
    return render(request, 'clients/client_list.html', context)


@login_required
def client_detail(request, pk):
    """Show detailed view of a client with related tasks and documents"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    client = get_object_or_404(Client, pk=pk, tenant=tenant)
    
    # Get related tasks and documents
    tasks = Task.objects.filter(client=client).order_by('-created_at')
    documents = Document.objects.filter(client=client).order_by('-created_at')
    
    context = {
        'client': client,
        'tasks': tasks,
        'documents': documents,
        'total_tasks': tasks.count(),
        'pending_tasks': tasks.filter(status='pending').count(),
        'total_documents': documents.count(),
    }
    
    return render(request, 'clients/client_detail.html', context)


@login_required
def client_create(request):
    """Create a new client"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    if request.method == 'POST':
        form = ClientForm(request.POST, user=request.user)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client "{client.full_name}" created successfully.')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Add New Client',
    }
    
    return render(request, 'clients/client_form.html', context)


@login_required
def client_update(request, pk):
    """Update an existing client"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    client = get_object_or_404(Client, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client, user=request.user)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client "{client.full_name}" updated successfully.')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client, user=request.user)
    
    context = {
        'form': form,
        'client': client,
        'title': f'Edit Client: {client.full_name}',
    }
    
    return render(request, 'clients/client_form.html', context)


@login_required
def client_delete(request, pk):
    """Delete a client"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    client = get_object_or_404(Client, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        client_name = client.full_name
        client.delete()
        messages.success(request, f'Client "{client_name}" deleted successfully.')
        return redirect('client_list')
    
    context = {
        'client': client,
    }
    
    return render(request, 'clients/client_confirm_delete.html', context)
