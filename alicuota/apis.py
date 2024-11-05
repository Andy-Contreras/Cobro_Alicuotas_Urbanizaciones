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
            cedulaUnica = MiembroFamilia.objects.filter(cedula=cedula).exists()
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

class BuscarMiembrosFamilia(APIView):
    def get(self, request, id_familia):
        try:
            print(id_familia)
            miembros = MiembroFamilia.objects.filter(familia_id=id_familia)
            print(miembros)
            return Response(miembros.values(), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Familia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ModificarFamiliaView(APIView):
    def put(self, request, id_familia):
        try:
            # Cabecera: Actualizar la familia
            familia = FamiliaPropietario.objects.get(id=id_familia)
            familia.descripcion = request.data.get('descripcion')
            familia.save()

            # Detalles: Obtener la lista enviada desde el front
            listaFamilia = request.data.get('listaFamilia')  # Datos enviados desde el front
            miembros = MiembroFamilia.objects.filter(familia_id=id_familia)  # Miembros existentes en la DB

            # Convertir los miembros existentes a un diccionario para fácil acceso usando cédula
            miembros_existentes_dict = {miembro.cedula: miembro for miembro in miembros}

            # Eliminar miembros que no están en la lista del front
            for cedula in list(miembros_existentes_dict.keys()):
                if not any(miembro['cedula'] == cedula for miembro in listaFamilia):
                    # Si el miembro no está en la lista del front, lo eliminamos
                    miembros_existentes_dict[cedula].delete()
                    print(f'Miembro con cédula {cedula} eliminado.')

            # Agregar o actualizar miembros desde la lista del front
            for miembro_front in listaFamilia:
                cedula = miembro_front['cedula']
                # Si el miembro ya existe, lo actualizamos
                if cedula in miembros_existentes_dict:
                    miembro = miembros_existentes_dict[cedula]
                    miembro.nombre = miembro_front['nombre']
                    miembro.sexo = miembro_front['sexo']
                    miembro.parentesco = miembro_front['parentesco']
                    miembro.fecha_nacimiento = datetime.strptime(miembro_front['fecha_nacimiento'], "%Y-%m-%d")
                    miembro.save()
                    print(f'Miembro con cédula {cedula} actualizado.')
                else:
                    # Si el miembro no existe, lo creamos
                    fecha = datetime.strptime(miembro_front['fecha_nacimiento'], "%Y-%m-%d")
                    MiembroFamilia.objects.create(
                        nombre=miembro_front['nombre'],
                        cedula=cedula,
                        sexo=miembro_front['sexo'],
                        parentesco=miembro_front['parentesco'],
                        fecha_nacimiento=fecha,
                        familia_id=id_familia
                    )
                    print(f'Miembro creado con cédula {cedula}.')

            return Response({'mensaje': 'Familia modificada.'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Familia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Error en ModificarFamiliaView: {type(e).__name__} - {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class BuscarInfoViviendaView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT av.id, av.descripcion, av.valor, ar.nombre, ar.cedula, ar.email 
                    FROM alicuota_vivienda av 
                    JOIN alicuota_residente ar ON av.residente_id = ar.id
                """)

                # Obtener los resultados de la consulta
                resultados = cursor.fetchall()
                # Crear una lista de diccionarios para retornar los resultados
                data = [
                    {
                        'id': resultado[0],
                        'descripcion': resultado[1],
                        'valor': resultado[2],
                        'nombre': resultado[3],
                        'cedula': resultado[4],
                        'email': resultado[5]
                    } for resultado in resultados
                ]

            print('Consulta realizada con éxito')
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)