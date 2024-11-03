from email.message import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation.template import context_re
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from requests.utils import super_len
from django.shortcuts import render, redirect
from alicuota.forms import FamiliaPropietarioForm, MiembroFamiliaForm
from alicuota.models import *
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

class FamiliaListView(LoginRequiredMixin, ListView):
    template_name = 'Familia_Residente/lista_familia.html'
    model = FamiliaPropietario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Familia'
        context['btn_crear'] = 'Crear Familia'
        context['buscar'] = 'Buscar Familia'
        context['url_crear'] = '/familia_crear'
        context['btn_actualizar'] = '/familia_actualizar'
        return context

class FamiliaCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'Familia_Residente/crear_familia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Familia'
        context['residentes'] = Residente.objects.all()
        return context


class FamiliaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'Familia_Residente/crear_familia.html'
    model = FamiliaPropietario
    form_class = FamiliaPropietarioForm
    success_url = reverse_lazy('familia_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Configura el formset para cargar los datos de los miembros de la familia
        MiembroFamiliaFormSet = inlineformset_factory(
            FamiliaPropietario, MiembroFamilia, form=MiembroFamiliaForm, extra=0, can_delete=True
        )

        # Carga el formset con los datos existentes o con los datos POST si se está enviando el formulario
        if self.request.POST:
            context['miembros_formset'] = MiembroFamiliaFormSet(self.request.POST, instance=self.object)
        else:
            context['miembros_formset'] = MiembroFamiliaFormSet(instance=self.object)

        # Campos adicionales para la plantilla
        context.update({
            'titulo': 'ACTUALIZAR FAMILIA',
            'action_save': self.request.path,
            'cancel_url': reverse_lazy('familia_lista'),
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        miembros_formset = context['miembros_formset']

        # Validar ambos formularios (FamiliaPropietario y MiembroFamilia)
        if form.is_valid() and miembros_formset.is_valid():
            # Guardar el formulario de FamiliaPropietario y asignar a instance
            self.object = form.save()

            # Asignar la familia actual al formset y guardar los cambios en los miembros
            miembros_formset.instance = self.object
            miembros_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['miembros_formset'] = inlineformset_factory(
            FamiliaPropietario, MiembroFamilia, form=MiembroFamiliaForm, extra=0, can_delete=True
        )(self.request.POST, instance=self.object)

        return self.render_to_response(context)

