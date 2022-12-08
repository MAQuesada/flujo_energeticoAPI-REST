
import datetime
from django.utils import timezone
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.core.exceptions import ValidationError
# paste in your models.py


def only_digit(value):
    if value.isdigit() is False:
        raise ValidationError('Solo se permiten números')


class Combustibles(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    precio = models.FloatField()
    subelemento_gastos = models.CharField(max_length=5, validators=[only_digit])

    def __str__(self):
        return ''+self.name


class Tarjetas(models.Model):
    numero = models.CharField(max_length=16, validators=[only_digit],  primary_key=True)
    c_control = models.CharField(max_length=100, blank=True)
    fecha = models.DateField(default=datetime.date.today)
    receptor = models.CharField(max_length=100, blank=True)
    ci = models.CharField(max_length=11, validators=[only_digit], blank=True)
    lit_inicio = models.FloatField(blank=True, null=True)
    cliente_pr = models.FloatField(blank=True, null=True)
    combos = models.CharField(max_length=100, blank=True,)
    activa = models.BooleanField(default=True)
    # falta restriccion de activa y estado.
    # falta en el serializer pasarle el carro asociado

    estado = models.IntegerField(
        choices=[(1, 'Asignada'),
                 (2, 'Existencia'),
                 (3, 'Vencida'),
                 (4, 'Cancelada'),
                 (5, 'Pérdida o Deterioro')],
        default=2)

    def __str__(self):
        return ''+self.numero


class Vehiculo(models.Model):
    matricula = models.CharField(max_length=10, primary_key=True)
    tipo = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    indice_consumo_real = models.FloatField()
    indice_consumo_fabricante = models.FloatField()
    f_act_indice = models.DateField()
    f_vencFICAV = models.DateField()
    f_venc_lic_operativa = models.DateField()
    apto = models.BooleanField(default=True)
    combustible = models.ForeignKey(
        Combustibles, on_delete=models.CASCADE, related_name='t_combustible')
    cap_tanque = models.PositiveIntegerField()
    prueba_litro = models.DateField(blank=True)
    num_motor = models.CharField(max_length=20)
    num_chasis = models.CharField(max_length=20)
    num_AFT = models.IntegerField()
    chofer = models.CharField(max_length=100, blank=True)
    tarjeta_asociada = models.ForeignKey(
        Tarjetas, on_delete=models.SET_NULL, related_name='t_tarjeta_asociada_a',
        null=True, default=None)

    def __str__(self):
        return ''+self.matricula


class MantenimientoAnual(models.Model):
    # id = models.AutoField(primary_key=True)
    meses = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')]

    mes = models.IntegerField(choices=meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    matricula = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='t_matricula')
    plan_consumo = models.FloatField()
    km_a_recorrer = models.FloatField()
    km_prox_mant = models.FloatField(blank=True, null=True)
    km_recorridos = models.FloatField(blank=True, null=True)
    fecha_mant = models.CharField(max_length=20, blank=True)
    actividad = models.CharField(max_length=200, default='Mantenimiento Anual', blank=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('mes', 'anno', 'matricula')
        ordering = ['anno', 'mes']

    def __str__(self):
        return ''+str(self.mes) + ' ' + str(self.anno)


class Resolucion (models.Model):
    nameResolucion = models.CharField(max_length=200)

    def __str__(self):
        return ''+self.nameResolucion


class Articulo (models.Model):
    nameArticulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    resolucion = models.ForeignKey(
        Resolucion, on_delete=models.CASCADE, related_name='t_resolucion')

    def __str__(self) -> str:
        return ''+self.nameArticulo


class Autocontrol (models.Model):
    mes = models.IntegerField(choices=MantenimientoAnual.meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='t_articulo')

    respuesta = models.IntegerField(
        choices=[(1, 'SI'),
                 (0, 'NO'),
                 (-1, 'NP'), ], default=None, blank=True, null=True)
    accion = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return ''+str(self.mes) + ' ' + str(self.anno) + ' ' + self.articulo.nameArticulo

    class Meta:
        unique_together = ('mes', 'anno', 'articulo')


class Tikets(models.Model):
    nro_chip = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    matricula = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,
                                  related_name='t_matricula_tiket')
    lugar = models.CharField(max_length=200)

    cantidad_entrada = models.FloatField()
    importe_entrada = models.FloatField()

    cantidad_salida = models.FloatField()
    importe_salida = models.FloatField()

    cantidad_saldo = models.FloatField()
    importe_saldo = models.FloatField()

    class Meta:

        unique_together = ('fecha', 'matricula')
        ordering = ['fecha']

    def __str__(self):
        return ''+str(self.nro_chip) + ' ' + str(self.fecha)


class EquipoEquipo(models.Model):
    mes = models.IntegerField(choices=MantenimientoAnual.meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    matricula_ee = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='t_matricula_ee')
    indice_consumo_fabricante = models.FloatField()
    actividad_real = models.FloatField()    # entrada de usuario
    comb_serviciado = models.PositiveIntegerField()  # calculable de tiket
    comb_inicio_mes = models.PositiveIntegerField()  # calculable del mes anterior
    comb_fin_mes = models.PositiveIntegerField()  # entrada de usuario
    comb_consumido = models.PositiveIntegerField()  # calculable

    comb_debio_consumir = models.FloatField()  # calculable
    indice_consumo_real = models.FloatField()   # calculable
    indice_comsumo_normado = models.FloatField()  # de vehiculo(5)

    dif_consumo = models.FloatField()  # formula
    desviacion_indice_normado = models.FloatField()  # formula
    desviacion_absoluta = models.FloatField()  # formula

    combustible = models.ForeignKey(
        Combustibles, on_delete=models.CASCADE, related_name='t_combustible_ee')  # de vehiculo

    def __str__(self):
        return 'Equipo a Equipo'+str(self.mes) + '/' + str(self.anno) + ' ' + self.matricula_ee.matricula

    class Meta:
        unique_together = ('mes', 'anno', 'matricula_ee')
        ordering = ['matricula_ee']


class MantenimientoReal(models.Model):
    mes = models.IntegerField(choices=MantenimientoAnual.meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    matricula_mr = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='t_matricula_mr')
    real_consumo_combustibles = models.FloatField()
    km_recorridos = models.FloatField()
    actividad_realizada = models.CharField(
        max_length=400, default='Mantenimiento mensual', blank=True)
    observaciones = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return 'Mantenimiento Real'+str(self.mes) + '/' + str(self.anno) + ' ' + self.matricula_mr.matricula

    class Meta:
        unique_together = ('mes', 'anno', 'matricula_mr')
        ordering = ['mes']


class EquiposIneficientes(models.Model):
    mes = models.IntegerField(choices=MantenimientoAnual.meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    matricula_ineficiente = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='t_matricula_ineficiente')
    servicio = models.CharField(max_length=200)
    comb_sin_respaldo = models.FloatField()
    medidas = models.CharField(max_length=200,  default='', blank=True)

    def __str__(self):
        return 'Equipos Ineficientes' + str(
            self.mes) + '/' + str(
            self.anno) + ' ' + self.matricula_ineficiente.matricula

    class Meta:
        unique_together = ('mes', 'anno', 'matricula_ineficiente')
        ordering = ['matricula_ineficiente']


class TarjetasDudosas(models.Model):
    mes = models.IntegerField(choices=MantenimientoAnual.meses)
    anno = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    matricula_tarjeta = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name='t_matricula_tarjeta')
    nro_tarjeta = models.CharField(max_length=20)
    servicio = models.CharField(max_length=200)
    causa = models.CharField(max_length=200, default='', blank=True)
    medidas = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return ('Tarjetas Dudosas'+str(self.mes) + '/' + str(self.anno) + ' '
                + self.matricula_tarjeta.tarjeta_asociada)

    class Meta:
        unique_together = ('mes', 'anno', 'matricula_tarjeta')
        ordering = ['matricula_tarjeta']
