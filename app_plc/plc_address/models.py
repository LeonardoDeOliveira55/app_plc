from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
    
#################################################################################################3


class KVARValue(models.Model):
    """Valores predeterminados de KVAR y sus características"""
    kvar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="KVAR")
    voltage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Voltaje")
    amperage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amperaje nominal (A)")

    def __str__(self):
        return f"{self.kvar} KVAR - {self.voltage}V - {self.amperage}A"

    class Meta:
        verbose_name = "Valor KVAR"
        verbose_name_plural = "Valores KVAR"

class Location(models.Model):
    """Ubicación del banco de capacitores"""
    name = models.CharField(max_length=200, verbose_name="Nombre de ubicación")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_configured = models.BooleanField(default=False, verbose_name="Configuración completada")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contactor(models.Model):
    """Contactor y su configuración"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='contactors')
    number = models.IntegerField(verbose_name="Número de contactor")
    is_configured = models.BooleanField(default=False, verbose_name="Configuración completada")

    def __str__(self):
        return f"Contactor {self.number} - {self.location.name}"

class Capacitor(models.Model):
    """Capacitor individual con su valor KVAR"""
    contactor = models.ForeignKey(Contactor, on_delete=models.CASCADE, related_name='capacitors')
    number = models.IntegerField(verbose_name="Número de capacitor")
    kvar_value = models.ForeignKey(KVARValue, on_delete=models.PROTECT, verbose_name="Valor KVAR")

    def __str__(self):
        return f"Capacitor {self.number} - {self.contactor}"

class Measurement(models.Model):
    """Medición de corriente para cada contactor"""
    contactor = models.ForeignKey(Contactor, on_delete=models.CASCADE, related_name='measurements')
    current_r = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Corriente R (A)"
    )
    current_s = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Corriente S (A)"
    )
    current_t = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Corriente T (A)"
    )
    measurement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    @property
    def expected_current(self):
        """Calcula la corriente esperada sumando las corrientes nominales de todos los capacitores"""
        return sum(capacitor.kvar_value.amperage for capacitor in self.contactor.capacitors.all())

    @property
    def current_deviation_r(self):
        """Calcula la desviación en la fase R"""
        return ((self.current_r - self.expected_current) / self.expected_current) * 100

    @property
    def current_deviation_s(self):
        """Calcula la desviación en la fase S"""
        return ((self.current_s - self.expected_current) / self.expected_current) * 100

    @property
    def current_deviation_t(self):
        """Calcula la desviación en la fase T"""
        return ((self.current_t - self.expected_current) / self.expected_current) * 100

    def __str__(self):
        return f"Medición Contactor {self.contactor.number} - {self.measurement_date}"