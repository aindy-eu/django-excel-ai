"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import HomeView, AboutView

urlpatterns = [
    # Authentication URLs (must be before admin)
    path('auth/', include('apps.authentication.urls')),

    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),

    # Excel Manager
    path('excel/', include('apps.excel_manager.urls')),

    # Users
    path('', include('apps.users.urls')),

    # Development tools
    path('__reload__/', include('django_browser_reload.urls')),

    # Static pages
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
]

# Admin only in development
if settings.DEBUG or getattr(settings, 'ADMIN_ENABLED', False):
    urlpatterns.insert(0, path('admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)