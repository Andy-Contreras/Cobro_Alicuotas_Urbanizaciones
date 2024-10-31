from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from alicuota.view.vivienda_view import ViviendaListView, ViviendaCreateView, ViviendaUpdateView
from alicuota.views import InicioTemplateView, LoginUserView, CustomPasswordResetView
# from alicuota.view.clientes_view import *
from alicuota.view.residentes_view import *
from alicuota.view.vehiculos_view import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([

# url de login___________________________________________________________________________________________________
    path('configuracion/', admin.site.urls, name="configuracion"),
    path('accounts/login/', LoginUserView.as_view(), name='custom_login'),
    path('', RedirectView.as_view(url="accounts/login")),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

# urls de inicio_________________________________________________________________________________________________
    path('inicio/', InicioTemplateView.as_view(), name='inicio'),

# urls de clientes_______________________________________________________________________________________________
#     path('cliente_lista/', ClienteListView.as_view(), name='cliente_lista'),
#     path('cliente_crear/', ClienteCreateView.as_view(), name='cliente_crear'),
#     path('cliente_eliminar/<int:pk>', ClienteDeleteView.as_view(), name='cliente_eliminar'),
#     path('cliente_actualizar/<int:pk>', ClienteUpdateView.as_view(), name='cliente_actualizar'),

# urls de Residente______________________________________________________________________________________________
    path('residente_lista/', ResidenteListView.as_view(), name='residente_lista'),
    path('residente_crear/', ResidenteCreateView.as_view(), name='residente_crear'),
    path('residente_eliminar/<int:pk>', ResidenteDeleteView.as_view(), name='residente_eliminar'),
    path('residente_actualizar/<int:pk>', ResidenteUpdateView.as_view(), name='residente_actualizar'),
# urls de Vehiculos______________________________________________________________________________________________
    path('vehiculos_lista/', VehiculoListView.as_view(), name='vehiculo_lista'),
    path('vehiculo_crear/', VehiculoCreateView.as_view(), name='vehiculo_crear'),
    path('vehiculo_eliminar/<int:pk>', VehiculoDeleteView.as_view(), name='vehiculo_eliminar'),
    path('vehiculo_actualizar/<int:pk>', VehiculoUpdateView.as_view(), name='vehiculo_actualizar'),

# urls de Vivienda_______________________________________________________________________________________________
    path('vivienda_lista/', ViviendaListView.as_view(), name='vivienda_lista'),
    path('vivienda_crear/', ViviendaCreateView.as_view(), name='vivienda_crear'),
    path('vivienda_actualizar/<int:pk>', ViviendaUpdateView.as_view(), name='vivienda_actualizar'),

# urls de Familia_______________________________________________________________________________________________
#     path('familia_lista/', FamiliaListView.as_view(), name='familia_lista'),
#     path('familia_crear/', FamiliaCreateView.as_view(), name='familia_crear'),

    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    ]

    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
