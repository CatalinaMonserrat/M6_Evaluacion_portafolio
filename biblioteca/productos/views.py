from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Libro, Pedido, LineaPedido
from .forms import CheckoutForm

def home(request):
    return render(request, 'productos/home.html')

def ver_carrito(request):
    return render(request, 'productos/carrito.html', {'items': [], 'total': 0})

class LibroListView(ListView):
    model = Libro
    template_name = 'productos/libro_list.html'
    context_object_name = 'libros'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'productos/libro_detail.html'

def _get_cart(session):
    return session.setdefault('cart', {})  # {libro_id: cantidad}

def agregar_carrito(request, pk):
    libro = get_object_or_404(Libro, pk=pk) #Manejo de erro en caso de no encontrar el libro
    cart = _get_cart(request.session)
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session.modified = True
    messages.success(request, f"{libro} agregado al carrito.")
    return redirect('libro_list')

def quitar_carrito(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    cart = _get_cart(request.session)
    if str(pk) in cart:
        del cart[str(pk)]
        request.session.modified = True
        messages.success(request, f"{libro} quitado del carrito.")
    return redirect('libro_list')

def ver_carrito(request):
    cart = _get_cart(request.session)
    items, total = [], 0
    for sid, qty in cart.items(): # sid = libro_id y qty = cantidad
        libro = get_object_or_404(Libro, pk=int(sid))
        subtotal = libro.precio * qty
        total += subtotal
        items.append({'libro': libro, 'cantidad': qty, 'subtotal': subtotal})
    return render(request, 'productos/carrito.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        messages.warning(request, "El carrito está vacío.")
        return redirect('libro_list')

    # Construimos el form según método
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedido = Pedido.objects.create(
                usuario=request.user,
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                direccion=form.cleaned_data['direccion'],
            )

            # Validación de stock y creación de líneas
            for sid, qty in cart.items():
                libro = get_object_or_404(Libro, pk=int(sid))
                qty = int(qty)
                if libro.stock < qty:
                    messages.error(request, f"No hay suficiente stock de {libro}.")
                    pedido.delete()
                    return redirect('libro_list')

                LineaPedido.objects.create(
                    pedido=pedido,
                    libro=libro,
                    cantidad=qty,
                    precio_unitario=libro.precio,
                )
                libro.stock -= qty
                libro.save()

            # Vaciar carrito y salir
            request.session['cart'] = {}
            messages.success(request, "Pedido creado con éxito.")
            return redirect('home')
    else:
        form = CheckoutForm(initial={
            'nombre': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        })

    # Si es GET o POST inválido, armamos items y total para render
    items, total = [], Decimal('0')
    for sid, qty in cart.items():
        libro = get_object_or_404(Libro, pk=int(sid))
        qty = int(qty)
        subtotal = libro.precio * qty  # Decimal * int
        total += subtotal
        items.append({'libro': libro, 'cantidad': qty, 'subtotal': subtotal})

    return render(request, 'productos/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })