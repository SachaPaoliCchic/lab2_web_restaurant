from django.db import models

# Create your models here.
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Table(models.Model):
    numero = models.IntegerField(unique=True)
    capacite = models.IntegerField()

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    nombre_personnes = models.IntegerField()
