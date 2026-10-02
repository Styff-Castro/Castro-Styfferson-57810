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
from django.db.models import Q
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .cart import Cart, MODELOS

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
    patron = request.GET.get("buscar", "").strip()
    if patron:
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
    patron = request.GET.get("buscar", "").strip()
    if patron:
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
    patron = request.GET.get("buscar", "").strip()
    if patron:
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
            consolas.precio = miForm.cleaned_data.get("precio")
            consolas.save()
            contexto = {"consolas": Consolas.objects.all() }
            return render(request, "appgame/consolas.html", contexto)       
    else:
        miForm = ConsolaForm(initial={"nombre": consolas.nombre, "empresa": consolas.empresa, "modelo": consolas.modelo, "precio": consolas.precio}) 
    
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
            juegos.precio = miForm.cleaned_data.get("precio")
            juegos.save()
            contexto = {"juegos": Juegos.objects.all() }
            return render(request, "appgame/juegos.html", contexto)       
    else:
        miForm = JuegoForm(initial={"nombre": juegos.nombre, "empresa": juegos.empresa, "categoria": juegos.categoria, "precio": juegos.precio}) 
    
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
            accesorios.precio = miForm.cleaned_data.get("precio")
            accesorios.save()
            contexto = {"accesorios": Accsesorios.objects.all() }
            return render(request, "appgame/accesorios.html", contexto)       
    else:
        miForm = AccesorioForm(initial={"nombre": accesorios.nombre, "empresa": accesorios.empresa, "modelo": accesorios.modelo, "precio": accesorios.precio}) 
    
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
def _volver(request, default="carrito"):
    """Regresa a la página desde donde se hizo el POST (si es del mismo sitio)."""
    siguiente = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
        return redirect(siguiente)
    return redirect(default)


@require_POST
def add_to_cart(request):
    tipo = request.POST.get("tipo")
    modelo = MODELOS.get(tipo)
    if modelo is None:
        messages.error(request, "Tipo de producto inválido.")
        return _volver(request)
    product = get_object_or_404(modelo, id=request.POST.get("product_id") or 0)
    Cart(request).add(tipo, product)
    messages.success(request, f"«{product.nombre}» agregado al carrito.")
    return _volver(request)


@require_POST
def decrease_from_cart(request):
    Cart(request).decrease(request.POST.get("tipo"), request.POST.get("product_id"))
    return redirect("carrito")


@require_POST
def remove_from_cart(request):
    Cart(request).remove(request.POST.get("tipo"), request.POST.get("product_id"))
    return redirect("carrito")


@require_POST
def clear_cart(request):
    Cart(request).clear()
    return redirect("carrito")


def carrito(request):
    return render(request, "appgame/carrito.html", {"cart": Cart(request)})


#-- Búsqueda global (barra del navbar) --#
def buscar(request):
    q = request.GET.get("q", "").strip()
    resultados = {"consolas": [], "accesorios": [], "juegos": []}
    if q:
        filtro = Q(nombre__icontains=q) | Q(empresa__icontains=q)
        resultados = {
            "consolas": Consolas.objects.filter(filtro | Q(modelo__icontains=q)),
            "accesorios": Accsesorios.objects.filter(filtro | Q(modelo__icontains=q)),
            "juegos": Juegos.objects.filter(filtro | Q(categoria__icontains=q)),
        }
    total = sum(len(r) for r in resultados.values())
    return render(request, "appgame/buscar.html", {"q": q, "total": total, **resultados})
