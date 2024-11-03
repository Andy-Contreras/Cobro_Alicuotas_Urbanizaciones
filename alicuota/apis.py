from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from alicuota.models import FamiliaPropietario, MiembroFamilia
from django.db import connection
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from alicuota.util import validar_cedula_ecuatoriana_api


class ValidacionesPersonaFamiliaView(APIView):
    def post(self, request):
        try:
            persona = request.data.get('persona')
            cedula = persona['cedula']
            print(cedula)
            cedulaUnica= MiembroFamilia.objects.filter(cedula=cedula).exists()
            print(cedulaUnica)
            if cedulaUnica == False:
                print("La cédula es única.")
                estado_cedula = validar_cedula_ecuatoriana_api(cedula)
                if estado_cedula == True:
                    print('La cedula es ecuatoriana')
                    return Response({'mensaje': 'La cedula es ecuatoriana'}, status=status.HTTP_200_OK)
                else:
                    print('La cedula no ecuatoriana')
                    return Response({'mensaje': 'La cedula no ecuatoriana'}, status=status.HTTP_200_OK)
            else:
                print("La cédula ya está en uso.")
                return Response({'mensaje': 'La cédula ya está en uso.'}, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CrearFamiliaView(APIView):
    def post(self, request):
        try:
            residente = request.data.get('residente')
            listaFamilia = request.data.get('listaFamilia')
            print(f'Residente: {residente}')
            print(f'listaFamilia: {listaFamilia}')

            id_residente = int(residente['id'])
            with connection.cursor() as cursor:
                cursor.execute("insert into alicuota_familiapropietario(residente_id, descripcion) values(%s, %s)",
                               [id_residente, residente['descripcion']])
                print('Cabecera Creada')

            ultimoId = FamiliaPropietario.objects.latest('id').id

            for miembro in listaFamilia:
                fecha_str = miembro['fechaNacimiento']
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                with connection.cursor() as cursor:
                    cursor.execute("insert into alicuota_miembrofamilia(nombre, cedula, sexo, parentesco, "
                                   "fecha_nacimiento, familia_id) values (%s, %s,%s, %s,%s, %s)",
                                   [miembro['nombre'], miembro['cedula'], miembro['sexo'], miembro['parentesco'], fecha,
                                    ultimoId])
                print('Detalle Creado')

            return Response({'mensaje': 'Familia creada.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
