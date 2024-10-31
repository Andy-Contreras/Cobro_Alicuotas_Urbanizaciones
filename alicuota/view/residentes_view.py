from email.message import Message

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation.template import context_re
from django.views.generic import ListView,CreateView,DeleteView, UpdateView
from requests.utils import super_len

from alicuota.forms import ResidenteForm
from alicuota.models import *
from django.urls import reverse_lazy

class ResidenteListView(LoginRequiredMixin, ListView):
    template_name = 'Residente/lista_residente.html'
    model = Residente

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return self.model.objects.filter(nombre__icontains=query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Residente'
        context['btn_crear'] = 'Crear Residente'
        context['buscar'] = 'Buscar Residente'
        context['url_crear'] = '/residente_crear'
        context['btn_eliminar'] = '/residente_eliminar'
        context['btn_actualizar'] = '/residente_actualizar'
        return context

class ResidenteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'Residente/crear_residente.html'
    model = Residente
    form_class =ResidenteForm
    success_url = reverse_lazy('residente_lista')
    context_object_name = 'residentes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'NUEVO REGISTRO'
        context['action_save'] = '/residente_crear/'
        context['listar_url'] = '/residente_lista/'
        context['cancel_url'] = reverse_lazy('residente_lista')
        return context


class ResidenteDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'Residente/eliminar_residente.html'
    model = Residente
    success_url = reverse_lazy('residente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'ELIMINAR RESIDENTE'
        context['action_save'] = self.request.path
        context['cancel_url'] = reverse_lazy('residente_lista')
        return context


class ResidenteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'Residente/crear_residente.html'
    model = Residente
    form_class = ResidenteForm
    success_url = reverse_lazy('residente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'ACTUALZIAR RESIDENTE'
        context['action_save'] = self.request.path
        context['cancel_url'] = reverse_lazy('residente_lista')
        return context