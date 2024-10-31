# from email.message import Message
#
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.translation.template import context_re
# from django.views.generic import ListView, CreateView, DeleteView, UpdateView
# from requests.utils import super_len
#
# from alicuota.forms import ClienteForm, ResidenteForm, FamiliaPropietarioForm
# from alicuota.models import *
# from django.urls import reverse_lazy
#
#
# class FamiliaListView(LoginRequiredMixin, ListView):
#     template_name = 'Familia_Residente/lista_familia.html'
#     model = FamiliaPropietario
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Listado de Familia'
#         context['btn_crear'] = 'Crear Familia'
#         context['buscar'] = 'Buscar Familia'
#         context['url_crear'] = '/familia_crear'
#         context['btn_actualizar'] = '/familia_actualizar'
#         return context
#
#
# class FamiliaCreateView(CreateView):
#     model = FamiliaPropietario
#     template_name = 'Familia_Residente/crear_familia.html'
#     success_url = reverse_lazy('familia_lista')
#     form_class = FamiliaPropietarioForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'NUEVO REGISTRO'
#         context['action_save'] = '/familia_crear/'
#         context['listar_url'] = '/familia_lista/'
#         context['cancel_url'] = reverse_lazy('familia_lista')
#         context['residentes'] = Residente.objects.all()  # Obtener la lista de residentes
#         return context
#
#     def form_valid(self, form):
#         # Guardar la familia primero
#         familia = form.save(commit=False)
#         familia.save()  # Guarda la familia, si hay un campo específico para el nombre de la familia
#
#         # Obtener datos de los miembros de la familia
#         nombres = self.request.POST.getlist('nombre[]')
#         cedulas = self.request.POST.getlist('cedula[]')
#         sexos = self.request.POST.getlist('sexo[]')
#         fechas_nacimiento = self.request.POST.getlist('fecha_nacimiento[]')
#         parentescos = self.request.POST.getlist('parentesco[]')
#         residente_id = self.request.POST.get('residente')  # Obtener el residente seleccionado
#
#         # Validar que se haya seleccionado un residente
#         if not residente_id:
#             form.add_error(None, 'Debes seleccionar un residente.')
#             return self.form_invalid(form)
#
#         # Guardar cada miembro de la familia
#         for i in range(len(nombres)):
#             FamiliaPropietario.objects.create(
#                 residente_id=residente_id,  # Asignar el residente
#                 nombre_familia=familia.nombre_familia,
#                 nombre=nombres[i],
#                 cedula=cedulas[i],
#                 sexo=sexos[i],
#                 fecha_nacimiento=fechas_nacimiento[i],
#                 parentesco=parentescos[i],
#             )
#
#         return super().form_valid(form)
