from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView, LogoutView

router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet),



urlpatterns =[
    path('', LoginView.as_view(template_name='index.html'), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('galeria',views.galeria, name='galeria'),
    path('galeria1',views.galeria1, name='galeria-1'),
    path('galeria2',views.galeria2, name='galeria-2'),
    path('artistal',views.artistal, name='artista-l'),
    path('artistai',views.artistai, name='artista-i'),
    path('pinturaslocales',views.pinturaslocales, name='pinturas-locales'),
    path('pi',views.pi, name='p-i'),
    path('prueba',views.prueba, name='prueba'),
    path('detalle_carrito', views.detalle_carrito, name='detalle_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Ferremas API')),
     path('pago/paypal/', views.pago_paypal, name='pago_paypal'),
    path('pago/paypal/ejecutar/', views.ejecutar_pago, name='ejecutar_pago'),
    

]