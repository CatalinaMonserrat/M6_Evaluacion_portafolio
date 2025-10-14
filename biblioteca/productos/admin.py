from django.contrib import admin
from .models import Libro, Autor

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'precio', 'stock')
    search_fields = ('titulo', 'autor__nombre')
    list_filter = ('autor', 'precio')

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)