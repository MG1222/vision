# camera/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test-connection/', views.test_connection, name='test_connection'),
    path('capture-image/', views.capture_image, name='capture_image'),
    path('capture/', views.capture_image, name='capture_image'),
]
