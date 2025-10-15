## Libreria — Proyecto Django

Aplicación web para una librería que comercializa libros. Permite listar y ver libros, gestionar un carrito, realizar checkout, y cuenta con autenticación/registro de usuarios, control de permisos por roles y un panel de ventas protegido. Incluye administración con Django Admin.

## Características

- Catálogo de libros (listado + detalle con imagen)
- Carrito de compras en sesión + Checkout
- Registro de usuarios, login y logout por POST
- Control de accesos:
@login_required en Checkout
Panel de ventas solo para usuarios con permiso productos.view_pedido
- Panel de administración: gestión de libros, autores, categorías, pedidos y líneas
- Bootstrap 5 para la UI

## Stack
- Python 3.12
- Django 5.2.x
- SQLite (desarrollo)
- Bootstrap 5.3 (CDN)

## Puesta en marcha
```bash
0) Clonar
git clone <URL-DEL-REPO>
cd biblioteca

1) Crear y activar entorno
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

2) Instalar dependencias
pip install -r requirements.txt   # si existe
# o al menos:
pip install django==5.2.7

3) Migraciones
python manage.py makemigrations
python manage.py migrate

4) Superusuario para admin
python manage.py createsuperuser

5) Correr servidor
python manage.py runserver

```
App en: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin

## Estructura (resumen)
```bash
biblioteca/
├─ biblioteca/              # settings/urls/wsgi/asgi
├─ productos/               # app principal
│  ├─ models.py             # Autor, Categoria, Libro, Pedido, LineaPedido
│  ├─ views.py              # home, list/detail, carrito, checkout, signup, panel_ventas
│  ├─ urls.py               # rutas de la app
│  ├─ forms.py              # CheckoutForm, SignUpForm
│  ├─ admin.py              # admin personalizado + inline de LineaPedido
├─ templates/
│  ├─ base.html             # layout + navbar + footer
│  ├─ login.html            # login con Django
│  ├─ signup.html           # registro de usuarios
│  └─ productos/
│     ├─ home.html
│     ├─ libro_list.html
│     ├─ libro_detail.html
│     ├─ carrito.html
│     └─ checkout.html
└─ manage.py
```
## Modelos
- Autor (nombre)
- Categoria (nombre)
- Libro (titulo, autor(FK), precio, imagen, stock)
- Pedido (usuario(FK opcional a User), nombre, email, direccion, creado_en)
- Método total() suma subtotales
- LineaPedido (pedido(FK), libro(FK), cantidad, precio_unitario)
- Método subtotal()

## Autenticación y Registro

- Login: django.contrib.auth.views.LoginView (/login/)
- Logout: botón en navbar via form POST → /logout/
- Registro: vista signup con SignUpForm (UserCreationForm extendido)
Al registrarse, el usuario queda logueado y redirige a home.

Settings útiles:
```bash
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```
## Autorización (roles y permisos)
Checkout protegido
```bash
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout(...):
    ...
```
##Panel de ventas por permiso

Solo usuarios con productos.view_pedido:
```bash
from django.contrib.auth.decorators import permission_required

@permission_required('productos.view_pedido', raise_exception=True)
def panel_ventas(request):
    ...
```
## Navbar sensible a permisos
```bash
{% if perms.productos.view_pedido %}
  <li class="nav-item"><a class="nav-link" href="{% url 'panel_ventas' %}">Panel</a></li>
{% endif %}
```

## Pruebas manuales sugeridas

- Crear usuario por /signup/ → queda logueado.
- Ver listado /libros/ → detalle de un libro.
- Agregar/quitar al carrito → ver totales.
- Ir a /checkout/ sin login → redirige a /login/.
- Con login → completar checkout → se crean Pedido + Líneas.
- Usuario sin permiso → /panel-ventas/ devuelve 403.
- Usuario en grupo Vendedores con view_pedido → accede a /panel-ventas/.

## Licencia

Uso académico/educativo (Bootcamp). Proyecto privado.

## Autoría

Desarrollado por Catalina (Bootcamp Python) — Módulo M6: Django.
Mentoría y guía pedagógica con enfoque en buenas prácticas y despliegue gradual.
