from django.db import models
from django.contrib.auth.models import User
from accounts.models import Tenant
from django.utils import timezone


class Client(models.Model):
    """Client model with tenant isolation"""
    CLIENT_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('former', 'Former Client'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=CLIENT_STATUS, default='active')
    notes = models.TextField(blank=True)
    address = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['tenant', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_tasks(self):
        return self.tasks.count()
    
    @property
    def pending_tasks(self):
        return self.tasks.filter(status='pending').count()
    
    @property
    def total_documents(self):
        return self.documents.count()
