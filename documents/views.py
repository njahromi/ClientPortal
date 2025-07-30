from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import Document
from .forms import DocumentForm, DocumentSearchForm
from clients.models import Client


@login_required
def document_list(request):
    """List all documents for the current tenant with search and filtering"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    documents = Document.objects.filter(tenant=tenant)
    
    # Handle search and filtering
    search_form = DocumentSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        document_type = search_form.cleaned_data.get('document_type')
        client = search_form.cleaned_data.get('client')
        
        if search:
            documents = documents.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(client__first_name__icontains=search) |
                Q(client__last_name__icontains=search)
            )
        
        if document_type:
            documents = documents.filter(document_type=document_type)
        
        if client:
            documents = documents.filter(client=client)
    
    # Pagination
    paginator = Paginator(documents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_documents': documents.count(),
    }
    
    return render(request, 'documents/document_list.html', context)


@login_required
def document_detail(request, pk):
    """Show detailed view of a document"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    document = get_object_or_404(Document, pk=pk, tenant=tenant)
    
    context = {
        'document': document,
    }
    
    return render(request, 'documents/document_detail.html', context)


@login_required
def document_create(request):
    """Create a new document"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.title}" uploaded successfully.')
            return redirect('documents:document_detail', pk=document.pk)
    else:
        form = DocumentForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Upload New Document',
    }
    
    return render(request, 'documents/document_form.html', context)


@login_required
def document_update(request, pk):
    """Update an existing document"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    document = get_object_or_404(Document, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document, user=request.user)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.title}" updated successfully.')
            return redirect('documents:document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document, user=request.user)
    
    context = {
        'form': form,
        'document': document,
        'title': f'Edit Document: {document.title}',
    }
    
    return render(request, 'documents/document_form.html', context)


@login_required
def document_delete(request, pk):
    """Delete a document"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    document = get_object_or_404(Document, pk=pk, tenant=tenant)
    
    if request.method == 'POST':
        document_title = document.title
        document.delete()
        messages.success(request, f'Document "{document_title}" deleted successfully.')
        return redirect('documents:document_list')
    
    context = {
        'document': document,
    }
    
    return render(request, 'documents/document_confirm_delete.html', context)


@login_required
def document_download(request, pk):
    """Download a document file"""
    if not hasattr(request.user, 'profile'):
        return render(request, 'accounts/setup_required.html')
    
    tenant = request.user.profile.tenant
    document = get_object_or_404(Document, pk=pk, tenant=tenant)
    
    # Check if file exists
    if not document.file or not os.path.exists(document.file.path):
        raise Http404("File not found")
    
    # Open and serve the file
    with open(document.file.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
        return response
