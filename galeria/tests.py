from django.test import TestCase
from .models import Cliente, Producto, Carrito, ElementoCarrito
from django.contrib.auth.models import User

class ProductoTestCase(TestCase):

    def setUp(self):
        # Configurar datos iniciales para las pruebas
        Producto.objects.create(nombre='Producto de prueba', precio=10.0, stock=5)

    def test_creacion_producto(self):
        producto = Producto.objects.get(nombre='Producto de prueba')
        self.assertEqual(producto.nombre, 'Producto de prueba')
        self.assertEqual(producto.precio, 10.0)
        self.assertEqual(producto.stock, 5)


class TestCarritoYPaypal(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.usuario = User.objects.create(username='usuario_prueba')
        self.producto = Producto.objects.create(nombre='Producto de prueba', precio=10.0, stock=5)

    def test_relacion_carrito_elementos(self):
        carrito = Carrito.objects.create(cliente=self.usuario)
        elemento = ElementoCarrito.objects.create(carrito=carrito, producto=self.producto, cantidad=2)

        # Verificar que el carrito tenga el elemento agregado
        self.assertEqual(carrito.elementos.count(), 1)
        self.assertEqual(carrito.elementos.first().producto.nombre, 'Producto de prueba')
        self.assertEqual(carrito.obtener_total(), 20.0)  # Precio del producto * cantidad

    def test_eliminar_del_carrito(self):
        # Crear un carrito para el usuario
        carrito = Carrito.objects.create(cliente=self.usuario)

        # Agregar un elemento al carrito
        elemento = ElementoCarrito.objects.create(carrito=carrito, producto=self.producto, cantidad=2)

        # Verificar que el carrito tenga el elemento agregado
        self.assertEqual(carrito.elementos.count(), 1)

        # Eliminar el elemento del carrito
        elemento.delete()

        # Verificar que el carrito esté vacío después de eliminar el elemento
        self.assertEqual(carrito.elementos.count(), 0)

        # Verificar que el total del carrito sea cero después de eliminar el elemento
        self.assertEqual(carrito.obtener_total(), 0.0)

        # Verificar que el elemento eliminado ya no esté en el carrito
        self.assertFalse(ElementoCarrito.objects.filter(carrito=carrito, producto=self.producto).exists())

        # Verificar que el producto tenga el stock original después de eliminarlo del carrito
        self.assertEqual(self.producto.stock, 5)
