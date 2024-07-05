from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transcriptor.urls')),  # Incluye las URLs de la aplicación transcriptor
]
