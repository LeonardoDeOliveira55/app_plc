from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Tag(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    TIPOS_IO = [
        ('DI', 'Digital Input'),
        ('DO', 'Digital Output'),
        ('AI', 'Analog Input'),
        ('AO', 'Analog Output'),
        ('RTD', 'RTD'),
    ]

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='direcciones')
    tipo_io = models.CharField(max_length=3, choices=TIPOS_IO)
    direccion_et = models.CharField(max_length=50)
    numero_modulo = models.IntegerField()
    numero_entrada = models.IntegerField()
    slot = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tag.nombre} - {self.tipo_io} - Módulo {self.numero_modulo}"