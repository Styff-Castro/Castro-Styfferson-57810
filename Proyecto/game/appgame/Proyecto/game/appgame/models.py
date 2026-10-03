from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class ConDescuento(models.Model):
    """Campos y cálculos comunes de precio/descuento para los productos."""
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(90)], help_text="Porcentaje de descuento (0-90)"
    )

    class Meta:
        abstract = True

    @property
    def precio_final(self):
        if not self.descuento:
            return self.precio
        factor = (Decimal(100) - self.descuento) / Decimal(100)
        return (self.precio * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# Modelo de Negocio de la App.

class Consolas(ConDescuento):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Consala"
        verbose_name_plural = "Consolas"
        ordering = ["-nombre"]

    def __str__(self):
        return f"{self.nombre}, {self.modelo}, {self.empresa}"

class Accsesorios(ConDescuento):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Accesorio"
        verbose_name_plural = "Accesesorios"
        ordering = ["nombre"]


    def __str__(self):
        return f"{self.nombre}, {self.modelo}, {self.empresa}"

  

class Juegos(ConDescuento):
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ["nombre"]
   
    def __str__(self):
        return f"{self.nombre}, {self.categoria}, {self.empresa}"
    
class Avatar(models.Model):   
    imagen = models.ImageField(upload_to="avatares") 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"


#-- Compras --#
class Pedido(models.Model):
    ESTADOS = [
        ("pagado", "Pagado"),
        ("preparacion", "En preparación"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    MARCAS = [("visa", "Visa"), ("mastercard", "Mastercard")]
    DOCUMENTOS = [("dni", "DNI"), ("pasaporte", "Pasaporte")]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="pedidos")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="pagado")

    # Montos
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)   # sin descuento
    descuento = models.DecimalField(max_digits=12, decimal_places=2)  # ahorro total
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Pago: NUNCA se guarda el número completo ni el CVV, solo la marca y los últimos 4
    titular = models.CharField(max_length=50)
    marca_tarjeta = models.CharField(max_length=10, choices=MARCAS)
    ultimos4 = models.CharField(max_length=4)
    vencimiento = models.CharField(max_length=7)  # MM/AAAA

    # Envío y contacto
    pais = models.CharField(max_length=56)
    ciudad = models.CharField(max_length=60)
    calle = models.CharField(max_length=100)
    casa_apto = models.CharField(max_length=20)
    codigo_postal = models.CharField(max_length=10)
    cod_area = models.CharField(max_length=4)
    telefono = models.CharField(max_length=12)
    tipo_documento = models.CharField(max_length=10, choices=DOCUMENTOS)
    numero_documento = models.CharField(max_length=9)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    @property
    def numero(self):
        return f"ZA-{self.id:06d}"

    @property
    def porcentaje_descuento(self):
        if not self.subtotal:
            return 0
        return round(self.descuento * 100 / self.subtotal)

    @property
    def paso_estado(self):
        """Índice del estado para la barra de seguimiento (cancelado = -1)."""
        orden = ["pagado", "preparacion", "enviado", "entregado"]
        return orden.index(self.estado) if self.estado in orden else -1

    def __str__(self):
        return f"{self.numero} - {self.user} - {self.get_estado_display()}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    tipo = models.CharField(max_length=10)
    producto_id = models.PositiveIntegerField()
    nombre = models.CharField(max_length=160)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.PositiveSmallIntegerField(default=0)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.precio_final * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.nombre}"

