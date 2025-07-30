from django.db import models
from django.contrib.auth.models import User
from accounts.models import Tenant
from clients.models import Client
from django.utils import timezone
import os


def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    return f'documents/{instance.tenant.slug}/{instance.client.id}/{filename}'


class Document(models.Model):
    """Document model with tenant isolation and client association"""
    DOCUMENT_TYPES = [
        ('contract', 'Contract'),
        ('invoice', 'Invoice'),
        ('proposal', 'Proposal'),
        ('report', 'Report'),
        ('other', 'Other'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='documents')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    file = models.FileField(upload_to=document_upload_path)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client.full_name}"
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
    @property
    def file_size(self):
        try:
            return self.file.size
        except:
            return 0
    
    @property
    def file_extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lower()
    
    def delete(self, *args, **kwargs):
        # Delete the file from storage when the model is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
