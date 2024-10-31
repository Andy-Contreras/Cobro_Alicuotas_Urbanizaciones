from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from alicuota.mixins import RetornarInicioMixin
from alicuota.models import *


# Create your views_system here.

class LoginUserView(RetornarInicioMixin, LoginView):
    extra_context = {'titulo': 'ACA - Inicio de sesión'}


class InicioTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel Administrativo'
        context['residentes'] = Residente.objects.count()
        context['viviendas'] = Vivienda.objects.count()
        return context


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    extra_context = {'titulo': 'ACA - Recuperar Contraseña'}

    def post(self, request, *args, **kwargs):
        # Obtener el correo ingresado desde el formulario
        email = request.POST.get('email')

        # Verificar si el correo está registrado
        if not User.objects.filter(email=email).exists():
            # Si el correo no existe, mostrar un mensaje de error
            messages.error(request, "El correo ingresado no está registrado.")
            return render(request, self.template_name, {
                'form': self.get_form(),
                'titulo': 'ACA - Recuperar Contraseña'
            })

        # Si el correo es válido, continuar con el proceso normal de restablecimiento
        messages.success(request, "Si el correo es correcto, recibirás un enlace para restablecer tu contraseña.")
        return super().post(request, *args, **kwargs)
