import pytest
from rest_framework import status
from django.urls import reverse
from cms_backend.models import Usuario, Rol, Permiso
from rest_framework.test import APIClient

@pytest.fixture(scope='module')
def test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield

@pytest.mark.django_db
class TestGestionDeUsuarios:
    client = APIClient()

    @pytest.fixture
    def crear_roles_y_permisos(self):
        # Crea permisos
        perm1 = Permiso.objects.create(nombre='puede_crear')
        perm2 = Permiso.objects.create(nombre='puede_editar')

        # Crea rol
        rol = Rol.objects.create(nombre='Editor')
        rol.permisos.set([perm1, perm2])
        return rol

    def test_registro_de_usuario(self, crear_roles_y_permisos):
        url = reverse('usuario-list-create')  # Ajustar según tu configuración de URL
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }
        
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Usuario.objects.count() == 1
        assert Usuario.objects.get().username == 'testuser'

    def test_roles_de_usuario(self, crear_roles_y_permisos):
        # Registra un usuario primero
        url = reverse('usuario-list-create')
        data = {
            "username": "roleuser",
            "email": "roleuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }

        self.client.post(url, data, format='json')

        usuario = Usuario.objects.get(username='roleuser')

        # Asigna roles al usuario
        usuario.roles.add(crear_roles_y_permisos)

        assert usuario.roles.count() == 1
        assert usuario.roles.first().nombre == 'Editor'

    def test_permisos_de_usuario(self, crear_roles_y_permisos):
        # Crea un nuevo usuario
        url = reverse('usuario-list-create')
        data = {
            "username": "permuser",
            "email": "permuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }
        response = self.client.post(url, data, format='json')

        usuario = Usuario.objects.get(username='permuser')

        # Asigna rol al usuario
        usuario.roles.add(crear_roles_y_permisos)

        # Verifica si el usuario tiene permisos
        assert usuario.roles.first().permisos.filter(nombre='puede_crear').exists()
        assert usuario.roles.first().permisos.filter(nombre='puede_editar').exists()

    def test_validacion_de_registro_de_usuario(self, crear_roles_y_permisos):
        url = reverse('usuario-list-create')
        data = {
            "username": "",  # Nombre de usuario inválido
            "email": "correo_invalido",
            "roles": [crear_roles_y_permisos.id]
        }

        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'email' in response.data

    def test_obtener_detalles_de_usuario(self, crear_roles_y_permisos):
        # Registra un nuevo usuario
        url = reverse('usuario-list-create')
        data = {
            "username": "detailuser",
            "email": "detailuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }
        self.client.post(url, data, format='json')

        usuario = Usuario.objects.get(username='detailuser')
        detalle_url = reverse('usuario-detail', kwargs={'pk': usuario.id})  # Ajustar según tu configuración de URL

        response = self.client.get(detalle_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'detailuser'
        assert response.data['email'] == 'detailuser@example.com'

    def test_actualizar_usuario(self, crear_roles_y_permisos):
        # Register a new user
        url = reverse('usuario-list-create')
        data = {
            "username": "updateuser",
            "email": "updateuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }
        self.client.post(url, data, format='json')

        user = Usuario.objects.get(username='updateuser')
        update_url = reverse('usuario-detail', kwargs={'pk': user.id})

        update_data = {
            "username": "updateduser2",
            "email": "updatedemail2@example.com",
            "roles": [crear_roles_y_permisos.id]
        }

        response = self.client.put(update_url, update_data, format='json')
        #print("\nerror codigo: ", response.status_code)
        #print("error data: ", response.data)

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.username == 'updateduser2'
        assert user.email == 'updatedemail2@example.com'
        assert user.roles.filter(id=crear_roles_y_permisos.id).exists()

    def test_borrar_usuario(self, crear_roles_y_permisos):
        # Register a new user
        url = reverse('usuario-list-create')
        data = {
            "username": "deleteuser",
            "email": "deleteuser@example.com",
            "roles": [crear_roles_y_permisos.id]
        }
        self.client.post(url, data, format='json')

        user = Usuario.objects.get(username='deleteuser')
        delete_url = reverse('usuario-detail', kwargs={'pk': user.id})

        response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Usuario.objects.count() == 0