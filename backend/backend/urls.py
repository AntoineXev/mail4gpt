from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from accounts.urls import api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('health', lambda request: JsonResponse({'status': 'ok'})),  # Health check endpoint
]

urlpatterns += api_urlpatterns
