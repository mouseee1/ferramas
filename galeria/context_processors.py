# galeria/context_processors.py

from .models import Carrito

def carrito_total(request):
    total = 0
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(cliente=request.user).first()
        if carrito:
            total = carrito.elementos.count()
    return {'carrito_total': total}
