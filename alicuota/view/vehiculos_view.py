from email.message import Message

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation.template import context_re
from django.views.generic import ListView,CreateView,DeleteView, UpdateView
from requests.utils import super_len

from alicuota.forms import VehiculoForm
from alicuota.models import *
from django.urls import reverse_lazy


class VehiculoListView(LoginRequiredMixin, ListView):
    template_name = 'Vehiculo/listado_vehiculo.html'
    model = Vehiculo

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return self.model.objects.filter(placa__icontains=query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'
        context['buscar'] = 'Buscar por placa'
        context['btn_crear'] = 'Crear Vehiculos'
        context['url_crear'] = '/vehiculo_crear'
        context['btn_eliminar'] = '/vehiculo_eliminar'
        context['btn_actualizar'] = '/vehiculo_actualizar'
        return context


class VehiculoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Vehiculo/crear_vehiculo.html'
    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy('vehiculo_lista')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'NUEVO REGISTRO'
        context['action_save'] = '/vehiculo_crear/'
        context['listar_url'] = '/vehiculo_lista/'
        context['cancel_url'] = reverse_lazy('vehiculo_lista')
        return context

class VehiculoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'vehiculo/eliminar_vehiculo.html'
    model = Vehiculo
    success_url = reverse_lazy('vehiculo_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'ELIMINAR VEHICULO'
        context['action_save'] = self.request.path
        context['cancel_url'] = reverse_lazy('vehiculo_lista')
        return context


class VehiculoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'Vehiculo/crear_vehiculo.html'
    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy('vehiculo_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'ACTUALIZAR VEHÍCULO'
        context['action_save'] = self.request.path
        context['cancel_url'] = reverse_lazy('vehiculo_lista')
        return context