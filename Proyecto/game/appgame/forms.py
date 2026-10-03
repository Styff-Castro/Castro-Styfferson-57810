import re
from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ConsolaForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    modelo = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    descuento = forms.IntegerField(label="Descuento (%)", min_value=0, max_value=90, initial=0, required=False)

class AccesorioForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    modelo = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    descuento = forms.IntegerField(label="Descuento (%)", min_value=0, max_value=90, initial=0, required=False)

class JuegoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    categoria = forms.CharField(max_length=50)
    empresa = forms.CharField(max_length=50)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    descuento = forms.IntegerField(label="Descuento (%)", min_value=0, max_value=90, initial=0, required=False)
    
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


#-- Checkout --#
ANIO_MIN = 2020
ANIO_MAX = date.today().year + 10   # rango realista: ninguna tarjeta dura más de ~10 años

SOLO_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$")
ALFANUM = re.compile(r"^[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ#º°.,'\- ]+$")  # letras, números y signos de dirección


def luhn_valido(numero):
    """Algoritmo de Luhn: detecta números de tarjeta mal tipeados."""
    total, alterno = 0, False
    for d in reversed(numero):
        n = int(d)
        if alterno:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        alterno = not alterno
    return total % 10 == 0


def solo_digitos(valor):
    return re.sub(r"[\s-]", "", valor or "")


class CheckoutForm(forms.Form):
    MESES = [("", "Mes")] + [(f"{m:02d}", f"{m:02d}") for m in range(1, 13)]
    ANIOS = [("", "Año")] + [(str(a), str(a)) for a in range(ANIO_MIN, ANIO_MAX + 1)]

    # Tarjeta
    marca = forms.ChoiceField(label="Tipo de tarjeta", choices=[("visa", "Visa"), ("mastercard", "Mastercard")],
                              widget=forms.RadioSelect)
    titular = forms.CharField(label="Nombre del titular", min_length=3, max_length=50)
    numero_tarjeta = forms.CharField(label="Número de tarjeta", max_length=23)  # 19 dígitos + espacios
    mes = forms.ChoiceField(label="Mes", choices=MESES)
    anio = forms.ChoiceField(label="Año", choices=ANIOS)
    cvv = forms.CharField(label="Código de seguridad (CVV)", min_length=3, max_length=3)

    # Dirección
    pais = forms.CharField(label="País", min_length=2, max_length=56)
    ciudad = forms.CharField(label="Ciudad", min_length=2, max_length=60)
    calle = forms.CharField(label="Calle", min_length=3, max_length=100)
    casa_apto = forms.CharField(label="Casa / Apto", max_length=20)
    codigo_postal = forms.CharField(label="Código postal", min_length=3, max_length=10)

    # Contacto e identificación
    cod_area = forms.CharField(label="Código de país", min_length=1, max_length=4)
    telefono = forms.CharField(label="Teléfono", min_length=6, max_length=12)
    tipo_documento = forms.ChoiceField(label="Tipo de identificación",
                                       choices=[("dni", "DNI"), ("pasaporte", "Pasaporte")])
    numero_documento = forms.CharField(label="Número de identificación", min_length=6, max_length=9)

    # --- Validaciones por campo ---
    def clean_titular(self):
        v = " ".join(self.cleaned_data["titular"].split())
        if not SOLO_LETRAS.match(v):
            raise forms.ValidationError("Solo letras y espacios.")
        return v.upper()

    def clean_numero_tarjeta(self):
        v = solo_digitos(self.cleaned_data["numero_tarjeta"])
        if not v.isdigit():
            raise forms.ValidationError("Solo se permiten números.")
        if not 13 <= len(v) <= 19:
            raise forms.ValidationError("Debe tener entre 13 y 19 dígitos.")
        if not luhn_valido(v):
            raise forms.ValidationError("El número de tarjeta no es válido.")
        return v

    def clean_cvv(self):
        v = self.cleaned_data["cvv"]
        if not (v.isdigit() and len(v) == 3):
            raise forms.ValidationError("Debe tener exactamente 3 números.")
        return v

    def _texto(self, campo, patron=ALFANUM):
        v = " ".join(self.cleaned_data[campo].split())
        if not patron.match(v):
            raise forms.ValidationError("Contiene caracteres no permitidos.")
        return v

    def clean_pais(self):
        return self._texto("pais", SOLO_LETRAS)

    def clean_ciudad(self):
        return self._texto("ciudad")

    def clean_calle(self):
        return self._texto("calle")

    def clean_casa_apto(self):
        return self._texto("casa_apto")

    def clean_codigo_postal(self):
        v = self.cleaned_data["codigo_postal"].strip().upper()
        if not re.fullmatch(r"[0-9A-Z]{3,10}", v):
            raise forms.ValidationError("Solo letras y números, sin espacios.")
        return v

    def clean_cod_area(self):
        v = self.cleaned_data["cod_area"].lstrip("+")
        if not re.fullmatch(r"\d{1,3}", v):
            raise forms.ValidationError("De 1 a 3 números (ej. 54, 58).")
        return v

    def clean_telefono(self):
        v = solo_digitos(self.cleaned_data["telefono"])
        if not re.fullmatch(r"\d{6,12}", v):
            raise forms.ValidationError("Solo números, entre 6 y 12 dígitos.")
        return v

    # --- Validaciones que combinan campos ---
    def clean(self):
        data = super().clean()
        numero, marca = data.get("numero_tarjeta"), data.get("marca")

        if numero and marca:
            es_visa = numero.startswith("4") and len(numero) in (13, 16, 19)
            prefijo = int(numero[:4])
            es_master = (51 <= int(numero[:2]) <= 55 or 2221 <= prefijo <= 2720) and len(numero) == 16
            if marca == "visa" and not es_visa:
                self.add_error("numero_tarjeta", "No corresponde a una Visa (empieza con 4; 13, 16 o 19 dígitos).")
            if marca == "mastercard" and not es_master:
                self.add_error("numero_tarjeta", "No corresponde a una Mastercard (empieza con 51-55 o 2221-2720; 16 dígitos).")

        mes, anio = data.get("mes"), data.get("anio")
        if mes and anio:
            hoy = date.today()
            if (int(anio), int(mes)) < (hoy.year, hoy.month):
                self.add_error("anio", "La tarjeta está vencida.")

        tipo, doc = data.get("tipo_documento"), (data.get("numero_documento") or "").strip().upper()
        if tipo and doc:
            if tipo == "dni" and not re.fullmatch(r"\d{7,8}", doc):
                self.add_error("numero_documento", "El DNI lleva solo números (7 u 8 dígitos).")
            elif tipo == "pasaporte" and not re.fullmatch(r"[A-Z0-9]{6,9}", doc):
                self.add_error("numero_documento", "El pasaporte lleva letras y/o números (6 a 9 caracteres).")
            data["numero_documento"] = doc
        return data

