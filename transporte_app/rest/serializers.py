from rest_framework import serializers
from django.shortcuts import get_object_or_404

from transporte_app import models


class CombustibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Combustibles
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    # t_combustible = serializers.StringRelatedField()  # es de solo lectura por defalut

    class Meta:
        model = models.Vehiculo
        fields = '__all__'
        # exclude = ('combustible',)


class MantenimientoAnualSerializer (serializers.ModelSerializer):
    # matricula = serializers.StringRelatedField(read_only=True, default=None)

    matricula = VehiculoSerializer(read_only=True, default=None)

    anno = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = models.MantenimientoAnual
        fields = '__all__'
        read_only_fields = ['matricula', 'anno']


class ResolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resolucion
        fields = '__all__'


class ArticuloSerializer(serializers.ModelSerializer):

    # resolucion = ResolucionSerializer(read_only=True)

    class Meta:
        model = models.Articulo
        fields = '__all__'
        # depth = 1


class AutocontrolSerializer(serializers.ModelSerializer):
    id_articulo = serializers.IntegerField(write_only=True)
    # t_articulo = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    class Meta:
        model = models.Autocontrol
        fields = '__all__'
        read_only_fields = ['mes', 'anno']
        depth = 2
        extra_kwargs = {'id_articulo': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('id_articulo')
        return super().create(validated_data)


class AutocontrolDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Autocontrol
        fields = '__all__'


class TarjetasSerializer(serializers.ModelSerializer):
    t_tarjeta_asociada_a = VehiculoSerializer(read_only=True, many=True)

    class Meta:
        model = models.Tarjetas
        fields = '__all__'

    # validación a nivel de Objeto

    def validate(self, data):
        """ `data` is a dictionary of the fields values of serializer
        """
        if data['activa'] & (data['estado'] in (3, 4, 5)):
            raise serializers.ValidationError(
                'Una tarjeta activa solo puede estar Asignada o en Existencia')
        if data['estado'] in (1, 2) and not data['activa']:
            raise serializers.ValidationError(
                'Una tarjeta no activa no puede estar  Asignada o en Existencia')
        return data


class TiketSerializer (serializers.ModelSerializer):
    matricula = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    # matricula = VehiculoSerializer(read_only=True, default=None)

    class Meta:
        model = models.Tikets
        fields = '__all__'
        read_only_fields = ['matricula', 'cantidad_entrada', 'importe_salida',
                            'cantidad_saldo', 'importe_saldo']


class TiketDetailSerializer (serializers.ModelSerializer):
    matricula = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    # matricula = VehiculoSerializer(read_only=True, default=None)

    class Meta:
        model = models.Tikets
        fields = '__all__'
        read_only_fields = ['fecha']


class EquipoEquipoSerializer (serializers.ModelSerializer):
    # matricula_ee = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    class Meta:
        model = models.EquipoEquipo
        fields = '__all__'
        read_only_fields = [
            'mes', 'anno', 'indice_consumo_fabricante', 'comb_serviciado', 'comb_inicio_mes',
            'comb_consumido', 'comb_debio_consumir', 'indice_consumo_real',
            'indice_comsumo_normado', 'dif_consumo', 'desviacion_indice_normado',
            'desviacion_absoluta', 'combustible']


class EquipoEquipoDetailSerializer (serializers.ModelSerializer):

    class Meta:
        model = models.EquipoEquipo
        fields = '__all__'
        read_only_fields = [
            'mes', 'anno', 'matricula_ee', 'indice_consumo_fabricante', 'comb_serviciado',
            'comb_consumido', 'dif_consumo', 'indice_consumo_real', 'comb_debio_consumir',
            'desviacion_indice_normado', 'desviacion_absoluta', 'combustible']


class MantenimientoRealSerializer (serializers.ModelSerializer):
    # matricula = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    class Meta:
        model = models.MantenimientoReal
        fields = '__all__'
        read_only_fields = ['matricula_mr', 'anno', 'real_consumo_combustibles', 'km_recorridos']


class MantenimientoRealDetailSerializer (serializers.ModelSerializer):
    # matricula = serializers.PrimaryKeyRelatedField(read_only=True, default=None)

    class Meta:
        model = models.MantenimientoReal
        fields = '__all__'
        read_only_fields = ['matricula_mr', 'anno']


class EquiposIneficinetesSerializer (serializers.ModelSerializer):

    class Meta:
        model = models.EquiposIneficientes
        fields = '__all__'
        read_only_fields = ['matricula_ineficiente', 'anno', 'mes', ]
        write_only_fields = ('medidas', 'comb_sin_respaldo', 'servicio')


class TarjetasDudosasSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.TarjetasDudosas
        fields = '__all__'
        read_only_fields = ['matricula_tarjeta', 'anno', 'mes',  'servicio', 'nro_tarjeta']