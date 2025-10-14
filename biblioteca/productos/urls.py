from django.urls import path
from .views import home, LibroDetailView, LibroListView

urlpatterns = [
    path('', home, name='home'), #placeholder
    path('libros/', LibroListView.as_view(), name='libro_list'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
]