from django.urls import path, include
from rest_framework import routers

from alicuota.apis import CrearFamiliaView, ValidacionesPersonaFamiliaView

urlpatterns = [
    path('crear_familia/', CrearFamiliaView.as_view(), name='crear_familia'),
    path('validar_persona_familia/', ValidacionesPersonaFamiliaView.as_view(), name='validar_persona_familia'),

]
