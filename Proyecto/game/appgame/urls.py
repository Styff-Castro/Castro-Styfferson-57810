from django.urls import path, include
from .views import *
from . import views

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name="home"),
    path('consolas/', consolas, name="consolas"),
    path('accesorios/', accesorios, name="accesorios"),
    path('juegos/', juegos, name="juegos"),

    path('acerca/', acerca, name="acerca"),

    ##---Formulario---#
    path('consolaForm/', consolaForm, name="consolaForm"),
    path('accesorioForm/', accesorioForm, name="accesorioForm"), 
    path('juegoForm/', juegoForm, name="juegoForm"),

    ##---Buscar---##
    path('buscarConsolas/', buscarConsolas, name="buscarConsolas"),
    path('buscarAccesorios/', buscarAccesorios, name="buscarAccesorios"),
    path('buscarJuegos/', buscarJuegos, name="buscarJuegos"),
    path('encontrarConsolas/', encontrarConsolas, name="encontrarConsolas"),
    path('encontrarAccesorios/', encontrarAccesorios, name="encontrarAccesorios"),
    path('encontrarJuegos/', encontrarJuegos, name="encontrarJuegos"),

    ##--Update--##
     path('consolaUpdate/<id_consolas>/', consolaUpdate, name="consolaUpdate"),
     path('juegoUpdate/<id_juegos>/', juegoUpdate, name="juegoUpdate"),
     path('accesorioUpdate/<id_accesorios>/', accesorioUpdate, name="accesorioUpdate"),

    ##--Delete--##
     path('consolaDelete/<id_consolas>/', consolaDelete, name="consolaDelete"),
     path('juegoDelete/<id_juegos>/', juegoDelete, name="juegoDelete"),
     path('accesorioDelete/<id_accesorios>/', accesorioDelete, name="accesorioDelete"),
    
    #___ Login / Logout / Registration
    path('login/', loginRequest, name="login"),
    path('logout/', LogoutView.as_view(template_name="appgame/logout.html"), name="logout"),
    path('registro/', register, name="registro"),

    #___ Edición de Perfil / Avatar
    path('perfil/', editProfile, name="perfil"),
    path('<int:pk>/password/', CambiarClave.as_view(), name="cambiarClave"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),

    #-- Carrito --#
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('carrito/', views.carrito, name='carrito'),
]
