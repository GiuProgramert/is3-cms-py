from datetime import timedelta, timezone
from datetime import timedelta
from django.utils import timezone
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
class TestContarEstadosView:

    def test_cuenta_de_contenidos(self, api_client, crear_permiso):
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
            "estado": "en_revision",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_1 = api_client.post(reverse('contenido-list-create'), data=data)
        
        contenido_id = contenido_creado_1.data['id']
        data = {
            "estado": "aprobado",
            "titulo": "Titulo 1"
        }
        aprobar_contenido = api_client.put(reverse('aprobar-rechazar-contenido', kwargs={'pk': contenido_id}), data=data)


        data = {
            "titulo": "Titulo 2",
            "resumen": "Resumen 2",
            "cuerpo": "Cuerpo 2 del contenido",
            "estado": "en_revision",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_2 = api_client.post(reverse('contenido-list-create'), data=data)

        data = {
            "titulo": "Titulo 3",
            "resumen": "Resumen 3",
            "cuerpo": "Cuerpo 3 del contenido",
            "estado": "en_revision",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_3 = api_client.post(reverse('contenido-list-create'), data=data)

        data = {
            "titulo": "Titulo 4",
            "resumen": "Resumen 4",
            "cuerpo": "Cuerpo 4 del contenido",
            "estado": "en_revision",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_4 = api_client.post(reverse('contenido-list-create'), data=data)

        contenido_4_id = contenido_creado_4.data['id']
        data = {
            "estado": "rechazado",
            "titulo": "Titulo 4"
        }
        rechazar_contenido_4 = api_client.put(reverse('aprobar-rechazar-contenido', kwargs={'pk': contenido_4_id}), data=data)

        fecha_fin = timezone.now().date()
        fecha_inicio = fecha_fin - timedelta(days=1)

        lista_de_contenidos = api_client.get(reverse('contar-estados', kwargs={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}))

        print(lista_de_contenidos.data)
        assert lista_de_contenidos.data['inactivos'] == 0
        assert lista_de_contenidos.data['en_revision'] == 2