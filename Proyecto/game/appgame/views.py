from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *

from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from .models import Cart

# Create your views here.
def home(request):
    return render(request, "appgame/index.html")

@login_required
def consolas(request):
    contexto = {"consolas": Consolas.objects.all()}
    return render(request, "appgame/consolas.html", contexto)

@login_required
def accesorios(request):
    contexto = {"accesorios": Accsesorios.objects.all()}
    return render(request, "appgame/accesorios.html", contexto)

@login_required
def juegos(request):
    contexto = {"juegos": Juegos.objects.all()}
    return render(request, "appgame/juegos.html", contexto)

def acerca(request):
    return render(request, "appgame/acerca.html")

##---Formulario---##
@login_required
def consolaForm(request):
    if request.method == "POST":
        miForm = ConsolaForm(request.POST)
        if miForm.is_valid():
            consola_nombre = miForm.cleaned_data.get("nombre")
            consola_empresa = miForm.cleaned_data.get("empresa")
            consola_modelo = miForm.cleaned_data.get("modelo")
            consola_precio = miForm.cleaned_data.get("precio")
            consola = Consolas(nombre=consola_nombre, empresa=consola_empresa, modelo=consola_modelo, precio=consola_precio) 
            consola.save()
            contexto = {"consolas": Consolas.objects.all() }
            return render(request, "appgame/consolas.html", contexto)
        
    else:
        miForm =ConsolaForm()

    return render(request, "appgame/consolaForm.html", {"form":miForm})

@login_required
def accesorioForm(request):
    if request.method == "POST":
        miForm = AccesorioForm(request.POST)
        if miForm.is_valid():
            accesesorio_nombre = miForm.cleaned_data.get("nombre")
            accesorio_empresa = miForm.cleaned_data.get("empresa")
            accesorio_modelo = miForm.cleaned_data.get("modelo")
            accesorio_precio = miForm.cleaned_data.get("precio")
            accesorio = Accsesorios(nombre=accesesorio_nombre, empresa=accesorio_empresa, modelo=accesorio_modelo, precio=accesorio_precio) 
            accesorio.save()
            contexto = {"accesorios": Accsesorios.objects.all() }
            return render(request, "appgame/accesorios.html", contexto)
        
    else:
        miForm =AccesorioForm()

    return render(request, "appgame/accesorioForm.html", {"form":miForm})

@login_required
def juegoForm(request):
    if request.method == "POST":
        miForm = JuegoForm(request.POST)
        if miForm.is_valid():
            juego_nombre = miForm.cleaned_data.get("nombre")
            juego_empresa = miForm.cleaned_data.get("empresa")
            juego_categoria = miForm.cleaned_data.get("categoria")
            juego_precio = miForm.cleaned_data.get("precio")
            juego = Juegos(nombre=juego_nombre, empresa=juego_empresa, categoria=juego_categoria, precio=juego_precio) 
            juego.save()
            contexto = {"juegos": Juegos.objects.all() }
            return render(request, "appgame/juegos.html", contexto)
        
    else:
        miForm =JuegoForm()

    return render(request, "appgame/juegoForm.html", {"form":miForm})

#___ Buscarconsola
@login_required
def buscarConsolas(request):
    return render(request, "appgame/buscarconsola.html")

@login_required
def encontrarConsolas(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        consolas = Consolas.objects.filter(nombre__icontains=patron)
        contexto = {'consolas': consolas}    
    else:
        contexto = {'consolas': Consolas.objects.all()}
        
    return render(request, "appgame/consolas.html", contexto)

##___BuscarAccesorio
@login_required
def buscarAccesorios(request):
    return render(request, "appgame/buscaraccesorios.html")

@login_required
def encontrarAccesorios(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        accesorios = Accsesorios.objects.filter(nombre__icontains=patron)
        contexto = {'accesorios': accesorios}    
    else:
        contexto = {'accesorios': Accsesorios.objects.all()}
        
    return render(request, "appgame/accesorios.html", contexto)

#___BuscarJuego
@login_required
def buscarJuegos(request):
    return render(request, "appgame/buscarjuego.html")

@login_required
def encontrarJuegos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        juegos = Juegos.objects.filter(nombre__icontains=patron)
        contexto = {'juegos': juegos}    
    else:
        contexto = {'juegos': Juegos.objects.all()}
        
    return render(request, "appgame/juegos.html", contexto)

##--Encontrar Consolas, Accesorios, Juegos--#
@login_required
def encontrarConsolas(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        consolas = Consolas.objects.filter(nombre__icontains=patron)
        contexto = {'consolas': consolas}    
    else:
        contexto = {'consolas': Consolas.objects.all()}
        
    return render(request, "appgame/consolas.html", contexto)

@login_required
def encontrarAccesorios(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        accesorios = Accsesorios.objects.filter(nombre__icontains=patron)
        contexto = {'accesorios': accesorios}    
    else:
        contexto = {'accesorios': Accsesorios.objects.all()}
        
    return render(request, "appgame/accesorios.html", contexto)

@login_required
def encontrarJuegos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        juegos = Juegos.objects.filter(nombre__icontains=patron)
        contexto = {'juegos': juegos}    
    else:
        contexto = {'juegos': Juegos.objects.all()}
        
    return render(request, "appgame/juegos.html", contexto)

#--Update--#
@login_required
def consolaUpdate(request, id_consolas):
    consolas = Consolas.objects.get(id=id_consolas)
    if request.method == "POST":
        miForm = ConsolaForm(request.POST)
        if miForm.is_valid():
            consolas.nombre = miForm.cleaned_data.get("nombre")
            consolas.empresa = miForm.cleaned_data.get("empresa")
            consolas.modelo = miForm.cleaned_data.get("modelo")
            consolas.save()
            contexto = {"consolas": Consolas.objects.all() }
            return render(request, "appgame/consolas.html", contexto)       
    else:
        miForm = ConsolaForm(initial={"nombre": consolas.nombre, "empresa": consolas.empresa, "modelo": consolas.modelo}) 
    
    return render(request, "appgame/consolaForm.html", {"form": miForm})

@login_required
def juegoUpdate(request, id_juegos):
    juegos = Juegos.objects.get(id=id_juegos)
    if request.method == "POST":
        miForm = JuegoForm(request.POST)
        if miForm.is_valid():
            juegos.nombre = miForm.cleaned_data.get("nombre")
            juegos.empresa = miForm.cleaned_data.get("empresa")
            juegos.categoria = miForm.cleaned_data.get("categoria")
            juegos.save()
            contexto = {"juegos": Juegos.objects.all() }
            return render(request, "appgame/juegos.html", contexto)       
    else:
        miForm = JuegoForm(initial={"nombre": juegos.nombre, "empresa": juegos.empresa, "categoria": juegos.categoria}) 
    
    return render(request, "appgame/juegoForm.html", {"form": miForm})

@login_required
def accesorioUpdate(request, id_accesorios):
    accesorios = Accsesorios.objects.get(id=id_accesorios)
    if request.method == "POST":
        miForm = AccesorioForm(request.POST)
        if miForm.is_valid():
            accesorios.nombre = miForm.cleaned_data.get("nombre")
            accesorios.empresa = miForm.cleaned_data.get("empresa")
            accesorios.modelo = miForm.cleaned_data.get("modelo")
            accesorios.save()
            contexto = {"accesorios": Accsesorios.objects.all() }
            return render(request, "appgame/accesorios.html", contexto)       
    else:
        miForm = JuegoForm(initial={"nombre": accesorios.nombre, "empresa": accesorios.empresa, "modelo": accesorios.modelo}) 
    
    return render(request, "appgame/accesorioForm.html", {"form": miForm})

#--Delete--#
@login_required
def consolaDelete(request, id_consolas):
    consolas = Consolas.objects.get(id=id_consolas)
    consolas.delete()
    contexto = {"consolas": Consolas.objects.all() }
    return render(request, "appgame/consolas.html", contexto) 

@login_required
def juegoDelete(request, id_juegos):
    juegos = Juegos.objects.get(id=id_juegos)
    juegos.delete()
    contexto = {"juegos": Juegos.objects.all() }
    return render(request, "appgame/juegos.html", contexto)

@login_required
def accesorioDelete(request, id_accesorios):
    accesorios = Accsesorios.objects.get(id=id_accesorios)
    accesorios.delete()
    contexto = {"accesorios": Accsesorios.objects.all() }
    return render(request, "appgame/accesorios.html", contexto)

# ___ Login / Logout / Registration

def loginRequest(request):
    if request.method == "POST":
        player = request.POST["username"]
        clave = request.POST["password"]
        user = authenticate(request, username=player, password=clave)
        if user is not None:
            login(request, user)

              #_______ Buscar Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            #______________________________________________________________
            return render(request, "appgame/index.html")
        else:
            return redirect(reverse_lazy('login'))

    else:
        miForm = AuthenticationForm()

    return render(request, "appgame/login.html", {"form": miForm})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirige a la página de inicio después de cerrar sesión
    return render(request, 'appgame/logout.html')

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            #usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))
    else:
        miForm = RegistroForm()

    return render(request, "appgame/registro.html", {"form": miForm})    

# ____ Edición de Perfil / Avatar

@login_required
def editProfile(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy("home"))
    else:
        miForm = UserEditForm(instance=usuario)
    return render(request, "appgame/editarPerfil.html", {"form": miForm})
    
class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "appgame/cambiar_clave.html"
    success_url = reverse_lazy("home")

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)
        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            imagen = miForm.cleaned_data["imagen"]
            #_________ Borrar avatares viejos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #__________________________________________
            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()

            #_________ Enviar la imagen al home
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            #____________________________________________________
            return redirect(reverse_lazy("home"))
    else:
        miForm = AvatarForm()
    return render(request, "appgame/agregarAvatar.html", {"form": miForm})  

#-- Carrito --#

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = Consolas.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('carrito')

def carrito(request):
    cart = Cart(request)
    return render(request, 'appgame/carrito.html', {'cart': cart})

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        # Maneja el caso donde no se proporciona un ID de producto
        return redirect('home')  # Redirigir a una página relevante si no hay ID de producto

    # Convertir el product_id a un número entero
    try:
        product_id = int(product_id)
    except ValueError:
        return redirect('home')  # Redirigir si el ID no es válido

    # Obtener el producto y añadirlo al carrito
    product = get_object_or_404(Consolas, id=product_id)
    cart = Cart(request)
    cart.add(product)

    return redirect('carrito')



