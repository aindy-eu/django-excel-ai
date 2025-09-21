# Implementation Instructions - Django Excel AI Validator

> Project-specific patterns and conventions to follow

## Code Organization

### App Structure Pattern (Enterprise)
```
apps/[app_name]/
├── __init__.py
├── admin.py          # Dev only (if settings.DEBUG)
├── apps.py           # App configuration
├── forms.py          # Forms with security validation
├── managers.py       # Custom managers with query optimization
├── migrations/       # Database migrations
├── models.py         # Data models with encrypted fields
├── permissions.py    # Custom permission classes
├── serializers.py    # API serializers (versioned)
├── signals.py        # Signal handlers + audit logging
├── templates/        # App-specific templates
│   └── [app_name]/   # Namespaced templates
├── templatetags/     # Custom template tags
├── tests/           # Enterprise test structure with pytest
│   ├── __init__.py
│   ├── factories.py  # Factory-boy test data
│   ├── test_models.py
│   ├── test_views.py
│   └── test_security.py
├── urls.py           # URL patterns with rate limiting
├── utils.py          # Helper functions
└── views.py          # View classes with permission mixins

libs/[library_name]/  # Shared code (2+ uses)
├── __init__.py
├── encryption.py     # Field encryption utilities
├── audit.py          # Audit trail logging
└── middleware.py     # Security middleware
```

### Import Order
```python
# Standard library
import os
from datetime import datetime

# Django imports
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView

# Third-party imports
from allauth.account.models import EmailAddress
import requests

# Local imports
from apps.users.models import User
from apps.dashboard.forms import DashboardForm
from libs.encryption import EncryptedField
from libs.audit import log_action
```

## Django Patterns

### Model Patterns
```python
class MyModel(models.Model):
    """One-line description.

    Longer description if needed.
    """
    # Constants
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    # Fields
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'My Model'
        verbose_name_plural = 'My Models'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('app_name:model_detail', kwargs={'pk': self.pk})
```

### View Patterns

#### Class-Based Views (Preferred)
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

class MyListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = 'app_name/mymodel_list.html'
    context_object_name = 'items'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Items'
        return context
```

#### Function-Based Views (When Simpler)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def my_view(request, pk):
    item = get_object_or_404(MyModel, pk=pk, user=request.user)
    return render(request, 'app_name/template.html', {
        'item': item,
    })
```

### URL Patterns
```python
from django.urls import path
from . import views

app_name = 'app_name'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
]
```

### Form Patterns
```python
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['name', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='w-full'),
            Field('description', css_class='w-full'),
            Field('status', css_class='w-full'),
            Submit('submit', 'Save', css_class='btn-primary')
        )
```

### Admin Configuration
```python
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'user', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
```

## Template Patterns

### Base Template Extension
```django
{% extends "base.html" %}
{% load static %}
{% load crispy_forms_tags %}

{% block title %}Page Title - {{ block.super }}{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">{{ page_title }}</h1>

    <!-- Content here -->
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
</script>
{% endblock %}
```

### Common Tailwind Classes
```html
<!-- Containers -->
<div class="container mx-auto px-4">

<!-- Cards -->
<div class="bg-white rounded-lg shadow-md p-6">

<!-- Buttons -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
<a href="#" class="text-blue-600 hover:text-blue-800 underline">

<!-- Forms -->
<form class="space-y-4">
<input class="shadow appearance-none border rounded w-full py-2 px-3">

<!-- Tables -->
<table class="min-w-full divide-y divide-gray-200">

<!-- Alerts -->
<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
```

### Template Components Pattern
Create reusable components in `templates/components/`:
```django
<!-- templates/components/card.html -->
<div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-xl font-semibold mb-2">{{ title }}</h3>
    {{ content }}
</div>

<!-- Usage -->
{% include "components/card.html" with title="My Card" content=item.description %}
```

## Security Patterns

### Permission Checks
```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class MyView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'app_name.view_mymodel'
    # or for multiple permissions
    permission_required = ('app_name.view_mymodel', 'app_name.change_mymodel')
```

### Object-Level Permissions
```python
def get_object(self):
    obj = super().get_object()
    if obj.user != self.request.user:
        raise PermissionDenied
    return obj
```

### Form Security
```python
def form_valid(self, form):
    form.instance.user = self.request.user  # Set user before saving
    return super().form_valid(form)
```

## Database Patterns

### Query Optimization
```python
# Use select_related for ForeignKey
items = MyModel.objects.select_related('user').all()

# Use prefetch_related for ManyToMany
items = MyModel.objects.prefetch_related('tags').all()

# Use only() for specific fields
items = MyModel.objects.only('name', 'status').all()
```

### Custom Managers
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class MyModel(models.Model):
    # ... fields ...

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager
```

## Testing Patterns (pytest)
```python
import pytest
from django.urls import reverse
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestMyModel:
    def test_list_view(self, client, user):
        """Test that authenticated users can view list."""
        client.force_login(user)
        response = client.get(reverse('app_name:mymodel_list'))
        assert response.status_code == 200

    @pytest.mark.integration
    def test_create_flow(self, authenticated_client):
        """Test complete creation flow."""
        response = authenticated_client.post(
            reverse('app_name:mymodel_create'),
            data={'name': 'Test Item'}
        )
        assert response.status_code == 302

# Run with: pytest apps/app_name/tests/
# Coverage: pytest --cov=apps --cov-report=html
```

## Common Commands

### Development
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Tailwind watch mode
python manage.py tailwind start

# Tailwind build
python manage.py tailwind build

# Run tests
pytest                           # All tests
pytest apps/users/               # Specific app
pytest -m unit                   # Unit tests only
pytest --cov=apps                # With coverage
pytest -n auto                   # Parallel execution
```

### Database
```bash
# Access PostgreSQL
python manage.py dbshell

# Reset database (careful!)
python manage.py flush

# Load fixtures
python manage.py loaddata fixture_name
```

## Environment Variables
Always use environment variables for sensitive data:
```python
# In settings.py
import environ

env = environ.Env()

SECRET_KEY = env('SECRET_KEY')
DATABASE_URL = env('DATABASE_URL')
```

## Git Commit Messages
Follow this pattern:
```
type: subject

body (optional)

footer (optional)
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Tests
- chore: Maintenance

## Implementation Workflow

### Pre-Implementation
- [ ] Review existing patterns in codebase
- [ ] Identify reusable components
- [ ] Check for similar features to follow
- [ ] Review security implications
- [ ] Confirm technical approach with documentation

### During Implementation
- [ ] Follow existing HTMX/Alpine patterns
- [ ] Maintain consistent file structure
- [ ] Add both unit and integration tests
- [ ] Ensure dark mode support
- [ ] Check responsive design on each UI change
- [ ] Run linters frequently (not just at end)

### Post-Implementation
- [ ] Run all quality tools (lint, type-check, tests)
- [ ] Manual testing of happy path
- [ ] Manual testing of error cases
- [ ] Cross-browser verification
- [ ] Create comprehensive handover document
- [ ] Update documentation if patterns changed

## Common Patterns

### HTMX Modal/Partial Pattern
1. Button triggers hx-get to load form/content
2. Form/content targets specific container for updates
3. Success triggers event for coordinating updates
4. Use HX-Trigger header in response for events
5. Return different templates for HTMX vs regular requests

Example:
```python
# View
if hasattr(request, 'htmx') and request.htmx:
    response = render(request, 'partial.html', context)
    response['HX-Trigger'] = 'event-name'
    return response
```

### File Upload Pattern
1. Validate client-side with Alpine.js
2. Show preview before upload (for images)
3. Validate server-side (size, type, content)
4. Clean up old files with Django signals
5. Return updated partial on success

Example:
```python
# Form validation
def clean_avatar(self):
    file = self.cleaned_data.get('avatar')
    if file:
        if file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("File too large")
        # Check actual image validity
        try:
            get_image_dimensions(file)
        except:
            raise forms.ValidationError("Invalid image file")
    return file
```

### Alpine.js Component Pattern
1. Create component in `static/js/alpine/components/`
2. Follow existing component structure
3. Register in base.html
4. Initialize with `x-data` in template

Example:
```javascript
// static/js/alpine/components/myComponent.js
document.addEventListener('alpine:init', () => {
    Alpine.data('myComponent', (initialParam = false) => ({
        // State
        property: initialParam,

        // Methods
        doSomething() {
            // Implementation
        },

        // Lifecycle
        init() {
            // Initialization
        }
    }));
});
```

### Django Signal Pattern for Cleanup
```python
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=MyModel)
def cleanup_old_files(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = MyModel.objects.get(pk=instance.pk)
            if old_instance.file != instance.file:
                # Delete old file
                if os.path.isfile(old_instance.file.path):
                    os.remove(old_instance.file.path)
        except MyModel.DoesNotExist:
            pass
```

## Remember

1. **Check existing patterns first** - Look at similar code in the project
2. **Use Django's built-in features** - Don't reinvent the wheel
3. **Keep it simple** - Complexity should be justified
4. **Think about maintenance** - Code is read more than written
5. **Test edge cases** - Even if just manually for now
6. **Document unusual decisions** - Help future developers understand why
7. **Pattern reuse saves time** - Don't create new patterns unnecessarily
8. **UI details matter** - Consider all states (loading, error, success, empty)