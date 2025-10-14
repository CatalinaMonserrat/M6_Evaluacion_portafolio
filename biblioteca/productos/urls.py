from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('libros/', views.LibroListView.as_view(), name='libro_list'),
    path('libros/<int:pk>/', views.LibroDetailView.as_view(), name='libro_detail'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/quitar/<int:pk>/', views.quitar_carrito, name='quitar_carrito'),
]