# import datetime
from datetime import datetime


from django.db.utils import IntegrityError
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from transporte_app.models import *
from transporte_app.rest.serializers import *


class CombustibleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Cobustible.
    """
    queryset = Combustibles.objects.all()
    serializer_class = CombustibleSerializer


class VehiculoListViewSet(generics.ListCreateAPIView):
    """
    A simple ViewSet for viewing and editing Vehiculo.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def post(self, request, *args, **kwargs):
        numero = request.POST['tarjeta_asociada']
        try:
            tarjeta = Tarjetas.objects.get(numero=numero)
        except Tarjetas.DoesNotExist:
            tarjeta = None
        else:  # tarjeta existe
            if(tarjeta.estado == 1):
                return Response(
                    {'detail': f'Ya la Tarjeta {tarjeta.numero} esta asociada a un vehiculo'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                tarjeta.estado = 1
                tarjeta.activa = True
                tarjeta.receptor = request.POST['chofer']
                tarjeta.fecha = datetime.date.today()
                tarjeta.save()
        return super().post(request, *args, **kwargs)


class VehiculoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple ViewSet for viewing and editing Vehiculo.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def put(self, request, *args, **kwargs):

        vehiculo = get_object_or_404(Vehiculo, matricula=self.kwargs['pk'])

        try:
            tarjeta_antigua = Tarjetas.objects.get(numero=vehiculo.tarjeta_asociada)
        except Tarjetas.DoesNotExist:
            tarjeta_antigua = None
        try:
            tarjeta_nueva = Tarjetas.objects.get(numero=request.data['tarjeta_asociada'])
        except Tarjetas.DoesNotExist:
            tarjeta_nueva = None

        if tarjeta_antigua is not None:
            if tarjeta_nueva is not None:
                if tarjeta_antigua.numero != tarjeta_nueva.numero:
                    if tarjeta_nueva.estado == 1:
                        return Response(
                            {'detail': f'Ya la Tarjeta {tarjeta_nueva.numero} esta asociada a un vehiculo'},
                            status=status.HTTP_400_BAD_REQUEST)
                    else:  # ambas tarjetas existen y son diferentes
                        tarjeta_antigua.estado = 2
                        tarjeta_antigua.receptor = ''
                        tarjeta_antigua.fecha = datetime.date.today()
                        tarjeta_antigua.save()

                        tarjeta_nueva.activa = True
                        tarjeta_nueva.estado = 1
                        tarjeta_nueva.receptor = request.data['chofer']
                        tarjeta_nueva.fecha = datetime.date.today()
                        tarjeta_nueva.save()

            else:  # tarjeta nueva no existe
                tarjeta_antigua.estado = 2
                tarjeta_antigua.receptor = ''
                tarjeta_antigua.fecha = datetime.date.today()
                tarjeta_antigua.save()

        else:   # tarjeta antigua no existe
            if tarjeta_nueva is not None:
                if tarjeta_nueva.estado == 1:
                    return Response(
                        {'detail':
                         f'Ya la Tarjeta {tarjeta_nueva.numero} esta asociada a un vehiculo'},
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    tarjeta_nueva.activa = True
                    tarjeta_nueva.estado = 1
                    tarjeta_nueva.receptor = request.data['chofer']
                    tarjeta_nueva.fecha = datetime.date.today()
                    tarjeta_nueva.save()

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        vehiculo = get_object_or_404(Vehiculo, matricula=self.kwargs['pk'])

        try:
            tarjeta = Tarjetas.objects.get(numero=vehiculo.tarjeta_asociada)
        except Tarjetas.DoesNotExist:
            tarjeta = None
        else:
            tarjeta.estado = 2
            tarjeta.receptor = ''
            tarjeta.fecha = datetime.date.today()
            tarjeta.save()
        return super().delete(request, *args, **kwargs)


class MantenimientoAnualListAPIView(generics.ListCreateAPIView):
    """Obtene los `MantenimientoAnual` de acuerdo a un año y un Vehiculo
    especificado y ademas podemos insertar"""

    serializer_class = MantenimientoAnualSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        matricula = self.kwargs['matricula']
        get_object_or_404(Vehiculo, matricula=matricula)
        return MantenimientoAnual.objects.filter(anno=anno, matricula=matricula)

    def perform_create(self, serializer):
        """asignar al nuevo MantenimientoAnual el  anno y matricula al q
        pertenece el MantenimientoAnual en actual """

        anno = self.kwargs['anno']
        matricula = self.kwargs['matricula']
        vehi = get_object_or_404(Vehiculo, matricula=matricula)
        serializer.save(anno=anno, matricula=vehi)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except IntegrityError:
            return Response(
                {'detail': 'Ya existe el MantenimientoAnual para ese Vehiculo con igual mes y año'},
                status=status.HTTP_400_BAD_REQUEST)


class MantenimientoAnualDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Obtene una mes del MantenimientoAnual que ademas podemos actualizar o eliminar"""

    serializer_class = MantenimientoAnualSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return MantenimientoAnual.objects.filter(id=pk)

    def perform_update(self, serializer):
        """asignar el anno y matricula al q pertenece el MantenimientoAnual en actual """

        mant = get_object_or_404(MantenimientoAnual, id=self.kwargs['pk'])
        anno = mant.anno
        matricula = mant.matricula
        serializer.save(anno=anno, matricula=matricula)


@api_view()  # solo GET sin parametros
def redict_manteniento_anual(request, mes, matricula, anno):

    mant = get_object_or_404(MantenimientoAnual, matricula=matricula, anno=anno, mes=mes)
    return HttpResponseRedirect(
        reverse('transporte_app:mant-anual-detail', args=(mant.id,)))


class ArticuloViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Articulo.
    """
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer


class ResolucionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Resolucion.
    """
    queryset = Resolucion.objects.all()
    serializer_class = ResolucionSerializer


class AutocontrolTotalListAPIView(generics.ListCreateAPIView):
    """Obtene los `Autocontrols` de acuerdo a un año y un Vehiculo
    especificado y ademas podemos insertar"""

    serializer_class = AutocontrolSerializer
    # queryset = Resolucion.objects.select_related('articulo__resolucion').all()

    def get_queryset(self):
        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        return Autocontrol.objects.filter(anno=anno, mes=mes)

    def perform_create(self, serializer):
        """asignar al nuevo Autocontrol el  anno y mes en que estamos filtrando actualmente"""

        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        arti = get_object_or_404(Articulo, id=self.request.POST['id_articulo'])
        serializer.save(anno=anno, mes=mes, articulo=arti)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {'detail': 'Ya existe el Autocontrol para ese Articulo con igual mes y año'},
                status=status.HTTP_400_BAD_REQUEST)


class AutocontrolDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Obtene un Autocontrol que ademas podemos actualizar o eliminar"""

    serializer_class = AutocontrolDetailSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Autocontrol.objects.filter(id=pk)


class AutocontrolNPlListAPIView(generics.ListAPIView):
    """Obtene los `Autocontrols` de acuerdo a un año y un Vehiculo
    especificado y ademas podemos insertar"""

    serializer_class = AutocontrolSerializer
    # queryset = Resolucion.objects.select_related('articulo__resolucion').all()

    def get_queryset(self):
        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        return Autocontrol.objects.filter(anno=anno, mes=mes, respuesta=-1)


class TarjetasViewSet(viewsets.ModelViewSet):

    """
    A simple ViewSet for viewing and editing Tarjetas.
    """
    queryset = Tarjetas.objects.all()
    serializer_class = TarjetasSerializer

    def create(self, request, *args, **kwargs):
        if int(request.POST['estado']) in (1,):
            return Response(
                {'detail': 'Solo se puede Asignar una Tarjeta desde Vehiculo'},
                status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if int(request.POST['estado']) in (1,):
            return Response(
                {'detail': 'Solo se puede Asignar una Tarjeta desde Vehiculo'},
                status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class TiketsListAPIView(generics.ListCreateAPIView):
    """Obtene los Tikets de acuerdo a la fecha(mes/año) y un Vehiculo
    especificado y ademas podemos insertar"""
    serializer_class = TiketSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        matricula = self.kwargs['matricula']
        get_object_or_404(Vehiculo, matricula=matricula)
        return Tikets.objects.filter(matricula=matricula, fecha__year=anno, fecha__month=mes)

    def perform_create(self, serializer):
        """asignar los valores calculables al nuevo Tiket y el Vehiculo al que pertenece"""

        matricula = self.kwargs['matricula']
        vehi = get_object_or_404(Vehiculo, matricula=matricula)
        precio = round(float(vehi.combustible.precio), 2)

        if self.request.POST['importe_entrada'] == 0:
            cantidad_entrada = 0
        else:
            cantidad_entrada = round(float(self.request.POST['importe_entrada'])/precio, 2)

        importe_salida = round(float(self.request.POST['cantidad_salida'])*precio, 2)
        fecha = datetime.datetime.strptime(self.request.POST['fecha'], '%Y-%m-%dT%H:%M')

        query = Tikets.objects.filter(matricula=matricula, fecha__year=fecha.year,
                                      fecha__month=fecha.month)
        cantidad_saldo = 0.0
        importe_saldo = 0.0
        if query.exists():
            importe_saldo = round(
                query[query[:].__len__() - 1].importe_saldo +
                float(self.request.POST['importe_entrada']) - importe_salida, 2)
            cantidad_saldo = round(
                query[query[:].__len__() - 1].cantidad_saldo -
                float(self.request.POST['cantidad_salida']) + cantidad_entrada, 2)
        else:
            mes = fecha.month
            anno = fecha.year
            mes_anterior = mes - 1
            anno_anterior = anno
            if mes == 1:
                mes_anterior = 12
                anno_anterior = anno - 1
            query_anterior = Tikets.objects.filter(matricula=matricula, fecha__year=anno_anterior,
                                                   fecha__month=mes_anterior)
            if query_anterior.exists():
                importe_saldo = round(
                    query_anterior[query_anterior[:].__len__() - 1].importe_saldo +
                    float(self.request.POST['importe_entrada']) - importe_salida, 2)
            cantidad_saldo = round(
                query_anterior[query_anterior[:].__len__() - 1].cantidad_saldo -
                float(self.request.POST['cantidad_salida']) + cantidad_entrada, 2)

            # Restriccion de saldo

        if abs(round((cantidad_saldo * precio - importe_saldo), 2)) >= 0.1:
            return Response(
                {'detail': f'La cantidad de saldo no coincide con importe '},
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save(matricula=vehi, cantidad_entrada=cantidad_entrada,
                        importe_salida=importe_salida, cantidad_saldo=cantidad_saldo,
                        importe_saldo=importe_saldo)

    def post(self, request, *args, **kwargs):
        try:
            fecha = datetime.datetime.strptime(request.POST['fecha'], '%Y-%m-%dT%H:%M')
            if((Tikets.objects.filter(fecha__gte=fecha).exists())):
                return Response(
                    {'detail': 'No se puede insertar un Tiket con fecha anterior al ultimo'},
                    status=status.HTTP_400_BAD_REQUEST)

            respone = super().post(request, *args, **kwargs)

            # insertar tatjetas dudosas
            if respone.status_code == status.HTTP_201_CREATED:
                vehi = get_object_or_404(Vehiculo, matricula=self.kwargs['matricula'])
                if len(Tikets.objects.filter(fecha__gte=fecha - datetime.timedelta(days=1))[:]) >= 3 and not TarjetasDudosas.objects.filter(matricula_tarjeta=vehi,  anno=self.kwargs['anno'], mes=self.kwargs['mes']).exists():

                    TarjetasDudosas.objects.create(
                        matricula_tarjeta=vehi, anno=self.kwargs['anno'],
                        mes=self.kwargs['mes'],
                        nro_tarjeta=vehi.tarjeta_asociada, servicio=vehi.combustible,
                        causa='Mas de tres tickets de combustible en 24hs', medidas='')

            return respone

        except IntegrityError:
            return Response(
                {'detail': f'Ya existe un tiket asociado al vehiculo con la fecha seleccionada'},
                status=status.HTTP_400_BAD_REQUEST)


class TiketsDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TiketDetailSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Tikets.objects.filter(id=pk)

    # def perform_update(self, serializer):
    #     tiket = get_object_or_404(models.Tikets,self.kwargs['pk'])
    #     serializer.save(matricula= tiket.matricula)

    def update(self, request, *args, **kwargs):
        tiket = get_object_or_404(Tikets, id=self.kwargs['pk'])
        if((Tikets.objects.filter(fecha__gt=tiket.fecha).exists())):
            return Response(
                {'detail': 'No se puede modificar un Tiket con fecha anterior al ultimo'},
                status=status.HTTP_400_BAD_REQUEST)

        vehi = get_object_or_404(models.Vehiculo, matricula=tiket.matricula)
        if (round(float(request.data['cantidad_entrada']) * vehi.combustible.precio, 2) !=
                round(float(request.data['importe_entrada']), 2)):
            return Response(
                {'detail': 'Cantidad de Entrada no se corresponde con Importe de Entrada'},
                status=status.HTTP_400_BAD_REQUEST)

        if (round(float(request.data['cantidad_salida']) * vehi.combustible.precio, 2) !=
                round(float(request.data['importe_salida']), 2)):
            return Response(
                {'detail': 'Cantidad de Salida no se corresponde con Importe de Salida'},
                status=status.HTTP_400_BAD_REQUEST)

        if (round(float(request.data['cantidad_saldo']) * vehi.combustible.precio, 2) !=
                round(float(request.data['importe_saldo']), 2)):
            return Response(
                {'detail': 'Cantidad de Saldo no se corresponde con Importe de Saldo'},
                status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        tiket = get_object_or_404(Tikets, id=self.kwargs['pk'])
        if((Tikets.objects.filter(fecha__gt=tiket.fecha).exists())):
            return Response(
                {'detail': 'No se puede eliminar un Tiket con fecha anterior al ultimo'},
                status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)


class EquipoEquipoListAPIView(generics.ListCreateAPIView):
    """Obtene el Reporte de Vheiculos de acuerdo a (mes/año)"""
    serializer_class = EquipoEquipoSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        return EquipoEquipo.objects.filter(anno=anno, mes=mes)

    def perform_create(self, serializer):
        """asignar los valores calculables a EquipoEquipo"""

        anno = self.kwargs['anno']
        mes = self.kwargs['mes']
        vehi = get_object_or_404(Vehiculo, matricula=serializer.validated_data.get('matricula_ee'))
        indice_consumo_fabricante = vehi.indice_consumo_fabricante
        indice_comsumo_normado = vehi.indice_consumo_real

        # calcularlo de tikets
        comb_serviciado = 0
        query_tiket = Tikets.objects.filter(matricula=vehi.matricula, fecha__year=anno,
                                            fecha__month=mes)
        if query_tiket.exists():
            comb_serviciado = query_tiket[query_tiket[:].__len__() - 1].cantidad_saldo

        mes_anterior = mes - 1
        anno_anterior = anno
        if mes == 1:
            mes_anterior = 12
            anno_anterior = anno - 1

        equipo_query = EquipoEquipo.objects.filter(
            anno=anno_anterior, mes=mes_anterior, matricula_ee=vehi.matricula)

        comb_inicio_mes = 0
        if equipo_query.exists():
            comb_inicio_mes = equipo_query[0].comb_fin_mes

        comb_consumido = comb_serviciado + comb_inicio_mes - \
            float(serializer.validated_data.get('comb_fin_mes'))
        if (comb_consumido < 0):
            comb_consumido = 0

        comb_debio_consumir = 0
        if(indice_comsumo_normado > 0):
            comb_debio_consumir = round(float(serializer.validated_data.get(
                'actividad_real'))/indice_comsumo_normado, 2)

        indice_consumo_real = 0
        if(comb_consumido > 0):
            indice_consumo_real = round(
                float(serializer.validated_data.get('actividad_real'))/comb_consumido, 2)

        dif_consumo = 0  # formula
        desviacion_indice_normado = 0  # formula
        desviacion_absoluta = 5  # formula# formula y si el equipo no esta activo ponerlo > que 5

        combustible = get_object_or_404(Combustibles, name=vehi.combustible.name)

        # 13 campos para guardar en el serializer
        serializer.save(mes=mes, anno=anno,
                        indice_consumo_fabricante=indice_consumo_fabricante,
                        comb_serviciado=comb_serviciado,
                        comb_inicio_mes=comb_inicio_mes,
                        comb_consumido=comb_consumido,
                        comb_debio_consumir=comb_debio_consumir,
                        indice_consumo_real=indice_consumo_real,
                        indice_comsumo_normado=indice_comsumo_normado,
                        dif_consumo=dif_consumo,
                        desviacion_indice_normado=desviacion_indice_normado,
                        desviacion_absoluta=desviacion_absoluta,
                        combustible=combustible)

    def post(self, request, *args, **kwargs):

        try:
            response = super().post(request, *args, **kwargs)

            equipo = get_object_or_404(
                EquipoEquipo, mes=response.data['mes'],
                anno=response.data['anno'],
                matricula_ee=response.data['matricula_ee'])

            if response.status_code == status.HTTP_201_CREATED and float(
                    response.data['desviacion_absoluta']) >= 5 and not EquiposIneficientes.objects.filter(anno=equipo.anno, mes=equipo.mes,                                                          matricula_ineficiente=equipo.matricula_ee):

                EquiposIneficientes.objects.create(
                    anno=equipo.anno,
                    mes=equipo.mes,
                    matricula_ineficiente=equipo.matricula_ee,
                    servicio=equipo.combustible,
                    comb_sin_respaldo=equipo.desviacion_absoluta,
                    medidas='Ninguna')

            return response

        except IntegrityError:
            return Response(
                {'detail': f'Ya existe un vehicculo en EquipoEquipo con matricula {request.data["matricula_ee"]} y mes {self.kwargs["mes"]} y año {self.kwargs["anno"]} '},
                status=status.HTTP_400_BAD_REQUEST)


class EquipoEquipoDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EquipoEquipoDetailSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return EquipoEquipo.objects.filter(id=pk)

    def perform_update(self, serializer):
        equipo = get_object_or_404(models.EquipoEquipo,  id=self.kwargs['pk'])

        comb_consumido = equipo.comb_serviciado + float(serializer.validated_data.get(
            'comb_inicio_mes')) - float(serializer.validated_data.get('comb_fin_mes'))
        if comb_consumido < 0:
            comb_consumido = equipo.comb_consumido

        comb_debio_consumir = 0
        if(float(serializer.validated_data.get('indice_comsumo_normado')) > 0):
            comb_debio_consumir = round(
                float(serializer.validated_data.get('actividad_real')) /
                float(serializer.validated_data.get('indice_comsumo_normado')),
                2)

        indice_consumo_real = 0
        if(comb_consumido > 0):
            indice_consumo_real = round(
                float(serializer.validated_data.get('actividad_real'))/comb_consumido, 2)

        dif_consumo = 0  # formula
        desviacion_indice_normado = 0  # formula
        desviacion_absoluta = 6  # formula y si el equipo no esta activo ponerlo > que 5

        serializer.save(comb_consumido=comb_consumido,
                        comb_debio_consumir=comb_debio_consumir,
                        indice_consumo_real=indice_consumo_real,
                        dif_consumo=dif_consumo,
                        desviacion_indice_normado=desviacion_indice_normado,
                        desviacion_absoluta=desviacion_absoluta)

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)

        equipo = get_object_or_404(EquipoEquipo, id=kwargs['pk'])
        if response.status_code == status.HTTP_200_OK and equipo.desviacion_absoluta >= 5:
            if (not EquiposIneficientes.objects.filter(anno=equipo.anno, mes=equipo.mes,
                                                       matricula_ineficiente=equipo.matricula_ee).
                    exists()):

                EquiposIneficientes.objects.create(
                    anno=equipo.anno,
                    mes=equipo.mes,
                    matricula_ineficiente=equipo.matricula_ee,
                    servicio=equipo.combustible,
                    comb_sin_respaldo=equipo.desviacion_absoluta,
                    medidas='Ninguna')
            else:
                equipo_ineficiente = EquiposIneficientes.objects.get(
                    anno=equipo.anno, mes=equipo.mes, matricula_ineficiente=equipo.matricula_ee)
                equipo_ineficiente.comb_sin_respaldo = equipo.desviacion_absoluta
                equipo_ineficiente.save()
        else:
            query = EquiposIneficientes.objects.filter(anno=equipo.anno, mes=equipo.mes,
                                                       matricula_ineficiente=equipo.matricula_ee)
            if (response.status_code == status.HTTP_200_OK and query.exists()):
                query[0].delete()
        return response


class MantenimientoRealListAPIView(generics.ListCreateAPIView):
    serializer_class = MantenimientoRealSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        matricula = self.kwargs['matricula']
        return MantenimientoReal.objects.filter(anno=anno, matricula_mr=matricula)

    def perform_create(self, serializer):
        """asignar los valores calculables a MantenimientoReal"""

        anno = self.kwargs['anno']
        matricula = self.kwargs['matricula']
        vehi = get_object_or_404(Vehiculo, matricula=matricula)
        real_consumo_combustibles = 0
        km_recorridos = 0
        equipo_query = EquipoEquipo.objects.filter(
            anno=anno, matricula_ee=matricula, mes=serializer.validated_data.get('mes'))

        if equipo_query.exists():
            real_consumo_combustibles = float(equipo_query[0].comb_consumido)
            km_recorridos = (equipo_query[0].actividad_real)
        serializer.save(real_consumo_combustibles=real_consumo_combustibles,
                        km_recorridos=km_recorridos, anno=anno, matricula_mr=vehi)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except IntegrityError:
            return Response(
                {'detail': f'Ya ese Vehiculo tiene un MantenimientoReal  en ese mes y año'},
                status=status.HTTP_400_BAD_REQUEST)


class MantenimientoRealDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MantenimientoRealDetailSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return MantenimientoReal.objects.filter(id=pk)


class EquiposIneficientesListAPIView(generics.ListAPIView):
    serializer_class = EquiposIneficinetesSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        return EquiposIneficientes.objects.filter(anno=anno)


class EquiposIneficientesDetailsAPIView (generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EquiposIneficinetesSerializer

    def get_queryset(self):
        return EquiposIneficientes.objects.filter(id=self.kwargs['pk'])


class TarjetasDudosasListAPIView(generics.ListAPIView):
    serializer_class = TarjetasDudosasSerializer

    def get_queryset(self):
        anno = self.kwargs['anno']
        return TarjetasDudosas.objects.filter(anno=anno)


class TarjetasDudosasDetailsAPIView (generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TarjetasDudosasSerializer

    def get_queryset(self):
        return TarjetasDudosas.objects.filter(id=self.kwargs['pk'])
