from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ConsolaForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    modelo = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.IntegerField()

class AccesorioForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    modelo = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.IntegerField()

class JuegoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    categoria = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.IntegerField()
    
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Contraseña a confirmar", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
       
class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido", max_length=50, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)