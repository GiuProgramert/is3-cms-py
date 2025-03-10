from django.db import IntegrityError
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from cms_backend.models import Categoria, Subcategoria, Permiso, Rol, Usuario, Contenido, Like

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def crear_permiso(db):
    def make_permiso(nombre):
        return Permiso.objects.create(nombre=nombre)
    return make_permiso

@pytest.mark.django_db
class TestHistorialListCreateView:

    def test_historial(self, api_client, crear_permiso):
        permiso1 = crear_permiso("publicar")
        data = {
            "nombre": "Publicador",
            "permisos": [permiso1.id]
        }
        rol_creado = api_client.post(reverse('rol-list-create'), data=data)

        data = {
            "username": "usuario_nuevo",
            "email": "usuario_nuevo@ejemplo.com",
            "roles": [rol_creado.data['id']]
        }
        usuario_creado = api_client.post(reverse('usuario-list-create'), data=data)

        data = {
            "codigo": "001",
            "nombre": "Categoria de Prueba"
        }
        categoria_creada = api_client.post(reverse('categoria-list-create'), data=data)

        data = {
            "nombre": "Subcategoria de Prueba",
            "descripcion": "Nueva descripcion de la subcategoria",
            "categoria": [categoria_creada.data['id']]
        }
        subcategoria_creada = api_client.post(reverse('subcategoria-list-create'), data=data)

        data = {
            "titulo": "Titulo 1",
            "resumen": "Resumen 1",
            "cuerpo": "Cuerpo 1 del contenido",
            "estado": "borrador",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado = api_client.post(reverse('contenido-list-create'), data=data)
        contenido_id = contenido_creado.data['id']

        data = {
            "estado": "aprobado",
            "titulo": "Titulo 1"
        }
        contenido_aprobado = api_client.put(reverse('aprobar-rechazar-contenido', kwargs={'pk': contenido_id}), data=data)

        historial_data = {
            "contenido": contenido_id,
            "usuario": usuario_creado.data['id'],
            "comentario": "Primera entrada de historial para el primer contenido.",
            "estado": "aprobado"
        }
        historial_creado = api_client.post(reverse('historial-list-create'), data=historial_data)

        historial_data_2 = {
            "contenido": contenido_id,
            "usuario": usuario_creado.data['id'],
            "comentario": "Segunda entrada de historial para el primer contenido.",
            "estado": "borrador"
        }
        historial_adicional_creado = api_client.post(reverse('historial-list-create'), data=historial_data_2)

        historial_data_3 = {
            "contenido": contenido_id,
            "usuario": usuario_creado.data['id'],
            "comentario": "Tercera entrada de historial para el primer contenido.",
            "estado": "borrador"
        }
        historial_adicional_creado = api_client.post(reverse('historial-list-create'), data=historial_data_3)

        data = {
            "titulo": "Titulo jeje",
            "resumen": "Resumen jeje",
            "cuerpo": "Cuerpo jeje del contenido",
            "estado": "borrador",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_2 = api_client.post(reverse('contenido-list-create'), data=data)
        contenido_2_id = contenido_creado_2.data['id']

        data = {
            "estado": "aprobado",
            "titulo": "Titulo jeje"
        }
        contenido_aprobado_2 = api_client.put(reverse('aprobar-rechazar-contenido', kwargs={'pk': contenido_2_id}), data=data)


        historial_data = {
            "contenido": contenido_2_id,
            "usuario": usuario_creado.data['id'],
            "comentario": "Primera entrada de historial para el segundo contenido..",
            "estado": "aprobado"
        }
        historial_creado_contenido_2 = api_client.post(reverse('historial-list-create'), data=historial_data)

        response_contenido_2 = api_client.get(reverse('contenido-detail', kwargs={'pk': contenido_id}))
        for historial in response_contenido_2.data['historiales']:
            print('\n\n', historial)