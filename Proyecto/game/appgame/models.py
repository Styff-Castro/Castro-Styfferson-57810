from django.db import models
from django.contrib.auth.models import User

# Modelo de Negocio de la App.

class Consolas(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    precio = models.IntegerField()
    
    class Meta:
        verbose_name = "Consala"
        verbose_name_plural = "Consolas"
        ordering = ["-nombre"]

    def __str__(self):
        return f"{self.nombre}, {self.modelo}, {self.empresa}"

class Accsesorios(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    precio = models.IntegerField()

    class Meta:
        verbose_name = "Accesorio"
        verbose_name_plural = "Accesesorios"
        ordering = ["nombre"]


    def __str__(self):
        return f"{self.nombre}, {self.modelo}, {self.empresa}"

  

class Juegos(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    precio = models.IntegerField()

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

#--Carrito--#
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Consolas.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
