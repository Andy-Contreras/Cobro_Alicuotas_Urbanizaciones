from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator



def validar_cedula_ecuatoriana(cedula):
    if len(cedula) != 10 or not cedula.isdigit():
        raise ValidationError("La cédula debe tener 10 dígitos numéricos.")

    provincia = int(cedula[0:2])
    if provincia < 1 or provincia > 24:
        raise ValidationError("Los dos primeros dígitos de la cédula no corresponden a una provincia válida.")

    digito_verificador = int(cedula[-1])
    suma = 0

    for i in range(9):
        digito = int(cedula[i])
        if i % 2 == 0:  # Posición par
            digito *= 2
            if digito > 9:
                digito -= 9
        suma += digito

    suma = suma % 10
    if suma != 0:
        suma = 10 - suma

    if suma != digito_verificador:
        raise ValidationError("La cédula no es válida.")


# Validacion para solo numero
solo_numeros_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='El número debe tener exactamente 10 dígitos numéricos.'
)

#Validaciones para las apis
def validar_cedula_ecuatoriana_api(cedula):
    try:
        if len(cedula) != 10 or not cedula.isdigit():
            print('La cédula debe tener 10 dígitos numéricos.')
            return False  # La cédula debe tener 10 dígitos numéricos.

        provincia = int(cedula[0:2])
        if provincia < 1 or provincia > 24:
            print('Los dos primeros dígitos de la cédula no corresponden a una provincia válida.')
            return False  # Los dos primeros dígitos de la cédula no corresponden a una provincia válida.

        digito_verificador = int(cedula[-1])
        suma = 0

        for i in range(9):
            digito = int(cedula[i])
            if i % 2 == 0:  # Posición par
                digito *= 2
                if digito > 9:
                    digito -= 9
            suma += digito

        suma = suma % 10
        if suma != 0:
            suma = 10 - suma

        if suma != digito_verificador:
            print('La cédula no es válida.')

            return False  # La cédula no es válida.
        print('La cédula es válida.')
        return True  # La cédula es válida.
    except (ValueError, IndexError):
        print('Captura errores de conversión y de acceso a índices.')
        return False  # Captura errores de conversión y de acceso a índices.



