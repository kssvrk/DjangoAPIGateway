from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<path:path>/', views.proxy, name='proxy'),
    
    
]