from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transporte_app.rest.views import *


# El name de una  URL permite referirse a ella de forma inequívoca desde otras partes de Django,
app_name = 'transporte_app'


# Create a router and register our viewsets with it.
router = DefaultRouter()

# The API URLs are now determined automatically by the router.
router.register('tip-comb', CombustibleViewSet, basename="tip-comb")
router.register('resolucion', ResolucionViewSet, basename="resolucion")
router.register('articulo', ArticuloViewSet, basename="articulo")
router.register('tarjetas', TarjetasViewSet, basename="tarjetas")


urlpatterns = [

    # URL de combustible 'tip-comb/<str:pk>'
    path('', include(router.urls)),

    path('vehiculo/', VehiculoListViewSet.as_view(), name='vehiculo-list'),

    path('vehiculo/<str:pk>', VehiculoDetailViewSet.as_view(), name='vehiculo-detail'),

    path('mant-anual/<str:matricula>/<int:anno>',
         MantenimientoAnualListAPIView.as_view(), name='mant-anual'),

    path('mant-anual/<int:pk>', MantenimientoAnualDetailAPIView.as_view(),
         name='mant-anual-detail'),

    path('mant-anual/<str:matricula>/<int:anno>/<int:mes>',
         redict_manteniento_anual, name='mant-anual-detailr-redic'),

    path('autocontrol/<int:anno>/<int:mes>', AutocontrolTotalListAPIView.as_view(),
         name='autocontrol-list'),

    path('autocontrol/<int:anno>/<int:mes>/NP', AutocontrolNPlListAPIView.as_view(),
         name='autocontrolNP-list'),

    path('autocontrol/<int:pk>', AutocontrolDetailAPIView.as_view(), name="autocontrol-detail"),

    path('tikets/<str:matricula>/<int:anno>/<int:mes>',
         TiketsListAPIView.as_view(), name='tikets-list'),

    path('tikets/<int:pk>', TiketsDetailsAPIView.as_view(), name='tikets-detail'),

    path('equipo/<int:anno>/<int:mes>', EquipoEquipoListAPIView.as_view(), name='equipo-list'),

    path('equipo/<int:pk>', EquipoEquipoDetailsAPIView.as_view(), name='equipo-detail'),

    path('mant-real/<str:matricula>/<int:anno>', MantenimientoRealListAPIView.as_view(),
         name='mant-real-list'),

    path('mant-real/<int:pk>', MantenimientoRealDetailsAPIView.as_view(), name='mant-real-detail'),

    path('equipo-ineficientes/<int:anno>',
         EquiposIneficientesListAPIView.as_view(), name='ineficientes-list'),

    path('equipo-ineficientes/detail/<int:pk>', EquiposIneficientesDetailsAPIView.as_view(),
         name='ineficientes-detail'),

    path('tarjetas-dudosas/<int:anno>', TarjetasDudosasListAPIView.as_view(),
         name='tarjetas-dudosas-list'),

    path('tarjetas-dudosas/detail/<int:pk>', TarjetasDudosasDetailsAPIView.as_view(),
         name='tarjetas-dudosas-detail'),


]
