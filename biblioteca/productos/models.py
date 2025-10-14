from django.db import models
from django.conf import settings  

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self): return self.titulo

class Pedido(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    creado_en = models.DateTimeField(auto_now_add=True) 

    def total(self):  # calcula total
        return sum(item.subtotal() for item in self.items.all())  
    
    def __str__(self):
        # si usuario es None, muestra el nombre de envío
        return f"Pedido #{self.id} - {self.nombre}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name='items', on_delete=models.CASCADE  
    )
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.libro} x{self.cantidad}"