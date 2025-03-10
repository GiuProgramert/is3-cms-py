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
class TestContenidoMasLikesView:

    def test_generar_reporte(self, api_client, crear_permiso):
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

        data = {
            "username": "usuario_nuevo_2",
            "email": "usuario_nuevo_2@ejemplo.com",
            "roles": [rol_creado.data['id']]
        }
        usuario_creado_2 = api_client.post(reverse('usuario-list-create'), data=data)

        data = {
            "titulo": "Titulo 222",
            "resumen": "Resumen 222",
            "cuerpo": "Cuerpo 222 del contenido",
            "estado": "borrador",
            "subcategoria": [subcategoria_creada.data['id']],
            "usuario": [usuario_creado.data['id']]
        }
        contenido_creado_2 = api_client.post(reverse('contenido-list-create'), data=data)
        contenido_2_id = contenido_creado_2.data['id']

        data = {
            "estado": "aprobado",
            "titulo": "Titulo 222"
        }
        contenido_2_aprobado = api_client.put(reverse('aprobar-rechazar-contenido', kwargs={'pk': contenido_2_id}), data=data)

        like_creado = Like.objects.create(
            contenido=Contenido.objects.get(id=contenido_2_aprobado.data['id']),
            usuario=Usuario.objects.get(id=usuario_creado.data['id'])
        )

        like_creado_2 = Like.objects.create(
            contenido=Contenido.objects.get(id=contenido_2_aprobado.data['id']),
            usuario=Usuario.objects.get(id=usuario_creado_2.data['id'])
        )

        data = {
            "username": "usuario_nuevo_3",
            "email": "usuario_nuevo_3@ejemplo.com",
            "roles": [rol_creado.data['id']]
        }
        usuario_creado_3 = api_client.post(reverse('usuario-list-create'), data=data)

        like_creado_3 = Like.objects.create(
            contenido=Contenido.objects.get(id=contenido_2_aprobado.data['id']),
            usuario=Usuario.objects.get(id=usuario_creado_3.data['id'])
        )


        reporte_de_contenidos = api_client.get(reverse('contenido-mas-likes'))
        contador = 1
        for contenido in reporte_de_contenidos.data:
            print('\n\nID del contenido: ', contenido['id'])
            print('Posicion del contenido: ', contador)
            print('Cantidad de likes: ', contenido['num_likes'])
            print('---')
            contador = contador + 1
