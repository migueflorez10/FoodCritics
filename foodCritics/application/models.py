from django.db import models

# Create your models here.

class Categorias(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

class Restaurantes(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    place_id = models.CharField(primary_key=True, max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places= 1)
    location = models.JSONField(null=False)
    type = models.ForeignKey(Categorias, on_delete=models.CASCADE,null=True, blank=True)

class Comentarios(models.Model):
    place_id = models.CharField(primary_key=True, max_length=100)
    reviews = models.JSONField()

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length =200)
    email = models.CharField(max_length =200)
    password = models.CharField(max_length =50)
    points = models.IntegerField()

class plato(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length =200)
    price = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places= 1)
    reviews = models.JSONField()
    photo = models.ImageField(upload_to='FotoPlato/', default=None, blank=True)
    restaurante = models.ForeignKey(Restaurantes, on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(Categorias, on_delete=models.CASCADE,null=True, blank=True)
