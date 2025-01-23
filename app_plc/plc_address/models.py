from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Sector(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) 
    sector = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.sector} - {self.ubicacion} "

class Tag(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    TIPOS_IO = [
        ('DI', 'Digital Input'),
        ('DO', 'Digital Output'),
        ('AI', 'Analog Input'),
        ('AO', 'Analog Output'),
        ('RTD_IN', 'RTD Input'),
        ('RTD_OUT', 'RTD Output'),
    ]

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='direcciones')
    tipo_io = models.CharField(max_length=10, choices=TIPOS_IO)
    direccion_plc = models.CharField(max_length=50)
    slot = models.IntegerField()
    bastidor = models.IntegerField()
    direccion = models.CharField(max_length=50)
    numero_modulo = models.IntegerField()
    numero_entrada = models.IntegerField()   
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tag.nombre} - {self.tipo_io} - Módulo {self.numero_modulo}"