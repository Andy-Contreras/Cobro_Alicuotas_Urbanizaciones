from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from alicuota import views
# Importación de vistas
from alicuota.view.familia_view import FamiliaListView, FamiliaCreateView, FamiliaUpdateView
from alicuota.view.vivienda_view import ViviendaListView, ViviendaCreateView, ViviendaUpdateView
from alicuota.views import InicioTemplateView, LoginUserView, CustomPasswordResetView, PDFReporteResidenteView
from alicuota.view.clientes_view import *
from alicuota.view.residentes_view import ResidenteListView, ResidenteCreateView, ResidenteDeleteView, \
    ResidenteUpdateView
from alicuota.view.vehiculos_view import VehiculoListView, VehiculoCreateView, VehiculoDeleteView, VehiculoUpdateView
from alicuota.view.alicuota_view import *

urlpatterns = [
                  # URL de login
                  path('configuracion/', admin.site.urls, name="configuracion"),
                  path('api/', include('alicuota.urls')),
                  path('accounts/login/', LoginUserView.as_view(), name='custom_login'),
                  path('', RedirectView.as_view(url="accounts/login")),
                  path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

                  # URLs de inicio
                  path('inicio/', InicioTemplateView.as_view(), name='inicio'),

                  # URLs de residentes
                  path('residente_lista/', ResidenteListView.as_view(), name='residente_lista'),
                  path('residente_crear/', ResidenteCreateView.as_view(), name='residente_crear'),
                  path('residente_eliminar/<int:pk>/', ResidenteDeleteView.as_view(), name='residente_eliminar'),
                  path('residente_actualizar/<int:pk>/', ResidenteUpdateView.as_view(), name='residente_actualizar'),
                  path('inicio/generar/<int:pk>/', PDFReporteResidenteView.as_view(), name='generar'),

                  # URLs de vehículos
                  path('vehiculos_lista/', VehiculoListView.as_view(), name='vehiculo_lista'),
                  path('vehiculo_crear/', VehiculoCreateView.as_view(), name='vehiculo_crear'),
                  path('vehiculo_eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='vehiculo_eliminar'),
                  path('vehiculo_actualizar/<int:pk>/', VehiculoUpdateView.as_view(), name='vehiculo_actualizar'),

                  # URLs de viviendas
                  path('vivienda_lista/', ViviendaListView.as_view(), name='vivienda_lista'),
                  path('vivienda_crear/', ViviendaCreateView.as_view(), name='vivienda_crear'),
                  path('vivienda_actualizar/<int:pk>/', ViviendaUpdateView.as_view(), name='vivienda_actualizar'),

                  # URLs de familias
                  path('familia_lista/', FamiliaListView.as_view(), name='familia_lista'),
                  path('familia_crear/', FamiliaCreateView.as_view(), name='familia_crear'),
                  path('familia_actualizar/<int:pk>/', FamiliaUpdateView.as_view(), name='familia_actualizar'),

                  path('alicuota_lista/', AlicuotaListView.as_view(), name='alicuota_lista'),
                  path('alicuota_crear/', AlicuotaCreateView.as_view(), name='alicuota_lista'),

                  path("__reload__/", include("django_browser_reload.urls")),
                  path("accounts/", include("django.contrib.auth.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
