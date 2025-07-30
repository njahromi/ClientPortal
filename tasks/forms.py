from django import forms
from django.contrib.auth.models import User
from .models import Task, TaskComment
from clients.models import Client


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['client', 'title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter clients and users by tenant
        if self.user and hasattr(self.user, 'profile'):
            tenant = self.user.profile.tenant
            self.fields['client'].queryset = Client.objects.filter(tenant=tenant)
            self.fields['assigned_to'].queryset = User.objects.filter(profile__tenant=tenant)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        if self.user and hasattr(self.user, 'profile'):
            task.tenant = self.user.profile.tenant
            task.created_by = self.user
        if commit:
            task.save()
        return task


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.user:
            comment.author = self.user
        if commit:
            comment.save()
        return comment


class TaskSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Task.TASK_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Task.TASK_PRIORITY,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 