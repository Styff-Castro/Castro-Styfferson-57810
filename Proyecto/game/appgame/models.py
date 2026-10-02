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
