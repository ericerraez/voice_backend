from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.convert_api, name='convert_api'),
    path('convert_api/', views.convert_api, name='convert_api'),
    path('get_last_transcription/', views.get_last_transcription, name='get_last_transcription'),
]
