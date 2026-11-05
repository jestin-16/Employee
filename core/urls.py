from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy', 'app': 'Employee Management System'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/health/', health_check, name='api_health'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
