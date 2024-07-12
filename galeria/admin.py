from django.contrib import admin
from .models import Cliente, Producto, Carrito, ElementoCarrito


class ElementoCarritoAdmin(admin.ModelAdmin):
    list_display = ('get_producto_nombre', 'cantidad', 'carrito')

    def get_producto_nombre(self, obj):
        return obj.producto.nombre  # Asumiendo que 'nombre' es el campo en el modelo Producto que deseas mostrar

    get_producto_nombre.short_description = 'Producto'

# Register your models here.
admin.site.register(Producto)  # Registrar Producto con la clase ProductoAdmin
admin.site.register(Carrito)
admin.site.register(ElementoCarrito,ElementoCarritoAdmin)


