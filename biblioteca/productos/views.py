from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Libro

def home(request):
    return render(request, 'home.html')

class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'
    context_object_name = 'libros'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libro_detail.html'

