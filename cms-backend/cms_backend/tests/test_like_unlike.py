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
class TestLikeViews:

    def test_like_unlike(self, api_client, crear_permiso):
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

        like_creado = Like.objects.create(
            contenido=Contenido.objects.get(id=contenido_aprobado.data['id']),
            usuario=Usuario.objects.get(id=usuario_creado.data['id'])
        )

        # assert like_creado is not None
        # assert like_creado.contenido.id == contenido_aprobado.data['id']
        # print('\n', like_creado)
        assert Like.objects.filter(contenido=contenido_aprobado.data['id']).count() == 1

        data = {
            "username": "usuario_nuevo_2",
            "email": "usuario_nuevo_2@ejemplo.com",
            "roles": [rol_creado.data['id']]
        }
        
        usuario_creado_2 = api_client.post(reverse('usuario-list-create'), data=data)

        like_creado_2 = Like.objects.create(
            contenido=Contenido.objects.get(id=contenido_aprobado.data['id']),
            usuario=Usuario.objects.get(id=usuario_creado_2.data['id'])
        )

        assert Like.objects.filter(contenido=contenido_aprobado.data['id']).count() == 2
        
        like_borrado = api_client.delete(reverse('like-delete', kwargs={
            'contenido_id': contenido_aprobado.data['id'],
            'usuario_id': usuario_creado_2.data['id']
        }))
        assert like_borrado.status_code == status.HTTP_204_NO_CONTENT
        assert Like.objects.filter(contenido=contenido_aprobado.data['id']).count() == 1

        with pytest.raises(IntegrityError):
            Like.objects.create(
                contenido=Contenido.objects.get(id=contenido_aprobado.data['id']),
                usuario=Usuario.objects.get(id=usuario_creado.data['id'])
        )