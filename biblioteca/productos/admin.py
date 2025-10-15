from django.contrib import admin
from .models import Libro, Autor, Categoria, LineaPedido, Pedido

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'precio', 'stock')
    search_fields = ('titulo', 'autor__nombre')
    list_filter = ('autor', 'precio')

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('precio_unitario', 'subtotal_inline')
    fields = ('libro', 'cantidad', 'precio_unitario', 'subtotal_inline') # Componentes que se muestran

    @admin.display(description='Subtotal')
    def subtotal_inline(self, obj):
        return obj.subtotal() if obj.pk else ''

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [LineaPedidoInline]
    list_display = ('id', 'nombre', 'email', 'creado_en', 'total_admin')
    readonly_fields = ('creado_en', 'total_admin')
    search_fields = ('nombre','email')
    date_hierarchy = 'creado_en'

    @admin.display(description='Total')
    def total_admin(self, obj):
        return obj.total()  