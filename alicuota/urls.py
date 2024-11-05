from django.urls import path, include
from rest_framework import routers

from alicuota.apis import CrearFamiliaView, ValidacionesPersonaFamiliaView,BuscarMiembrosFamilia,ModificarFamiliaView, BuscarInfoViviendaView

urlpatterns = [
    path('crear_familia/', CrearFamiliaView.as_view(), name='crear_familia'),
    path('validar_persona_familia/', ValidacionesPersonaFamiliaView.as_view(), name='validar_persona_familia'),
    path('buscar_miembros_familia/<int:id_familia>/', BuscarMiembrosFamilia.as_view(), name='buscar_miembros_familia'),
    path('modificar_familia/<int:id_familia>/', ModificarFamiliaView.as_view(), name='modificar_familia'),
    path('buscar_vivienda/', BuscarInfoViviendaView.as_view(), name='buscar_vivienda'),

]
