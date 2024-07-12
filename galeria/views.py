from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Carrito, ElementoCarrito  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework import viewsets
from .serializers import ProductoSerializer
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect
import paypalrestsdk
from django.contrib.auth.decorators import login_required
from paypalrestsdk import Payment
from django.contrib.auth.views import LoginView, LogoutView






# Create your views here.
def index(requets):
    return render(requets, 'index.html')

def galeria(requets):
    return render(requets, 'galeria.html')



def galeria1(requets):
    return render(requets, 'galeria-1.html')
    
    

def galeria2(requets):
    return render(requets, 'galeria-2.html')

def artistai(requets):
    return render(requets,'artista-i.html' )

def artistal(requets):
    return render(requets,'artista-l.html' )

def pinturaslocales(request):
    # Obtener todos los productos
    productos = Producto.objects.all()

    # Pasar los productos a la plantilla
    return render(request, 'pinturas-locales.html', {'productos': productos})


def pi(requets):
    return render(requets, 'p-i.html')



def prueba(requets):
    return render(requets, 'prueba.html')



def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    carrito, creado = Carrito.objects.get_or_create(cliente=request.user)
    
    elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    if not creado:
        elemento.cantidad += 1
        elemento.save()
    
    return JsonResponse({'status': 'success',})
    
    

def eliminar_del_carrito(request, producto_id):
    carrito = get_object_or_404(Carrito, cliente=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    elemento = get_object_or_404(ElementoCarrito, carrito=carrito, producto=producto)
    
    elemento.delete()

    # Verificar si quedan elementos en el carrito
    elementos_en_carrito = carrito.elementos.all()
    if not elementos_en_carrito.exists():
        messages.info(request, 'No hay productos en tu carrito.')

    # Redirigir de vuelta a la página desde donde se hizo la solicitud
    return redirect('detalle_carrito')


def detalle_carrito(request):
    carrito = get_object_or_404(Carrito, cliente=request.user)
    return render(request, 'detalle_carrito.html', {'carrito': carrito})



def carrito_total(request):
    total = 0
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(cliente=request.user).first()
        if carrito:
            total = carrito.elementos.count()
    return {'carrito_total': total}




class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer



def pago_paypal(request):
    carrito = get_object_or_404(Carrito, cliente=request.user)  # Ajusta según tu modelo de carrito
    items = []
    total = 0

    for elemento in carrito.elementos.all():
        items.append({
            "name": elemento.producto.nombre,
            "sku": str(elemento.producto.id),
            "price": str(elemento.producto.precio),
            "currency": "USD",
            "quantity": elemento.cantidad
        })
        total += elemento.producto.precio * elemento.cantidad

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8000/pago/paypal/ejecutar",
            "cancel_url": "http://localhost:8000/pago/cancelar"},
        "transactions": [{
            "item_list": {
                "items": items},
            "amount": {
                "total": str(total),
                "currency": "USD"},
            "description": "Compra de productos en tu tienda"}]})

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        return render(request, 'error.html', {'error': payment.error})
    return render(request, 'pago/paypal.html')



@login_required
def ejecutar_pago(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        try:
            carrito = Carrito.objects.get(cliente=request.user)
            carrito.elementos.all().delete()
            return render(request, 'exito.html', {'payment': payment})
        except Carrito.DoesNotExist:
            return render(request, 'error.html', {'error': 'Carrito no encontrado.'})
