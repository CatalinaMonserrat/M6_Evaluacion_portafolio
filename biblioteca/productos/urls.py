from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #placeholder
    path('libros/', views.libro_list, name='libro_list'),
    path('libros/<int:pk>', views.libro_detail, name='libro_detail'),
]