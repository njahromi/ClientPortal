from django import forms
from .models import Document
from clients.models import Client


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['client', 'title', 'document_type', 'file', 'description']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter clients by tenant
        if self.user and hasattr(self.user, 'profile'):
            tenant = self.user.profile.tenant
            self.fields['client'].queryset = Client.objects.filter(tenant=tenant)
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB.")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError("File type not allowed. Please upload PDF, DOC, DOCX, TXT, JPG, JPEG, or PNG files.")
        
        return file
    
    def save(self, commit=True):
        document = super().save(commit=False)
        if self.user and hasattr(self.user, 'profile'):
            document.tenant = self.user.profile.tenant
            document.uploaded_by = self.user
        if commit:
            document.save()
        return document


class DocumentSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search documents...'
        })
    )
    document_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Document.DOCUMENT_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 