import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from cms_backend.models import Parametro, Categoria, Subcategoria, Permiso, Rol, Usuario, Contenido, Comentario

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def crear_parametro(db):
    def make_parametro(nombre, valor):
        return Parametro.objects.create(nombre=nombre, valor=valor)
    return make_parametro

@pytest.fixture
def crear_permiso(db):
    def make_permiso(nombre):
        return Permiso.objects.create(nombre=nombre)
    return make_permiso

@pytest.fixture
def crear_contenidoo(db, crear_permiso, crear_rol, crear_usuario, crear_categoria, crear_subcategoria):
    def make_contenidoo(titulo, resumen, cuerpo, estado, subcategoria, autor):
        return Contenido.objects.create(titulo = titulo,
                                        resumen = resumen,
                                        cuerpo = cuerpo,
                                        estado = estado,
                                        subcategoria = subcategoria,
                                        autor = autor)
    return make_contenidoo

@pytest.fixture
def crear_rol(db, crear_permiso):
    def make_rol(nombre, permisos=None):
        rol = Rol.objects.create(nombre=nombre)
        if permisos:
            for permiso in permisos:
                rol.permisos.add(permiso)
        return rol
    return make_rol

@pytest.fixture
def crear_usuario(db, crear_rol):
    def make_usuario(username, email, roles=None):
        usuario = Usuario.objects.create(username=username, email=email)
        if roles:
            usuario.roles.set(roles)
        return usuario
    return make_usuario

@pytest.fixture
def crear_categoria(db):
    def make_categoria(codigo, nombre):
        return Categoria.objects.create(codigo=codigo, nombre=nombre)
    return make_categoria

@pytest.fixture
def crear_subcategoria(db, crear_categoria):
    def make_subcategoria(nombre, descripcion, categoria):
        return Subcategoria.objects.create(nombre=nombre, descripcion=descripcion, categoria=categoria)
    return make_subcategoria

@pytest.fixture(scope='module')
def test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield


@pytest.mark.django_db
class TestParametroListCreate:
    
    def test_listar_parametros(self, api_client, crear_parametro):
        crear_parametro("parametro1", "valor1")
        crear_parametro("parametro2", "valor2")
        
        response = api_client.get(reverse('listar_crear_parametros'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['nombre'] == 'parametro1'
        assert response.data[0]['valor'] == 'valor1'

    def test_post_parametro(self, api_client):
        data = {
            "nombre": "parametro_nuevo",
            "valor": "valor_nuevo"
        }
        
        response = api_client.post(reverse('listar_crear_parametros'), data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Parametro.objects.count() == 1
        assert Parametro.objects.get().nombre == "parametro_nuevo"
        assert Parametro.objects.get().valor == "valor_nuevo"
        
    def test_crear_parametro_invalido(self, api_client):
        data = {
            "valor": "valor_sin_nombre"
        }
        
        response = api_client.post(reverse('listar_crear_parametros'), data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestCategoriaListCreate:

    def test_listar_categorias(self, api_client, crear_categoria):
        crear_categoria("001", "Categoria 1")
        crear_categoria("002", "Categoria 2")
        
        response = api_client.get(reverse('categoria-list-create'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['codigo'] == '001'
        assert response.data[0]['nombre'] == 'Categoria 1'

    def test_post_categoria(self, api_client):
        data = {
            "codigo": "003",
            "nombre": "Categoria Nueva"
        }
        
        response = api_client.post(reverse('categoria-list-create'), data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Categoria.objects.count() == 1
        assert Categoria.objects.get().codigo == "003"
        assert Categoria.objects.get().nombre == "Categoria Nueva"
        
    def test_crear_categoria_invalida(self, api_client):
        data = {
            "nombre": "Categoria sin codigo"
        }
        
        response = api_client.post(reverse('categoria-list-create'), data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestSubcategoriaListCreate:

    def test_listar_subcategorias(self, api_client, crear_subcategoria, crear_categoria):

        categoriaPrueba = crear_categoria("001", "Categoria 1")
        crear_subcategoria("Subcategoria1", "Descripcion1", categoriaPrueba)
        crear_subcategoria("Subcategoria2", "Descripcion2", categoriaPrueba)
        
        response = api_client.get(reverse('subcategoria-list-create'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['nombre'] == 'Subcategoria1'
        assert response.data[0]['descripcion'] == 'Descripcion1'
        assert response.data[1]['nombre'] == 'Subcategoria2'
        assert response.data[1]['descripcion'] == 'Descripcion2'

    def test_post_subcategoria(self, api_client, crear_categoria):
        categoriaPrueba = crear_categoria("001", "Categoria 1")
        data = {
            "nombre": "Subcategoria Nueva",
            "descripcion": "Nueva Descripcion",
            "categoria": categoriaPrueba.id
        }
        
        response = api_client.post(reverse('subcategoria-list-create'), data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Subcategoria.objects.count() == 1
        assert Subcategoria.objects.get().nombre == "Subcategoria Nueva"
        assert Subcategoria.objects.get().descripcion == "Nueva Descripcion"
        
    def test_crear_subcategoria_invalida(self, api_client):
        data = {
            "descripcion": "Descripcion sin nombre ni categoria",
        }
        
        response = api_client.post(reverse('subcategoria-list-create'), data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestPermisoListView:

    def test_listar_permisos(self, api_client, crear_permiso):
        crear_permiso("Permiso 1")
        crear_permiso("Permiso 2")
        
        response = api_client.get(reverse('permiso-list'))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['nombre'] == 'Permiso 1'
        assert response.data[1]['nombre'] == 'Permiso 2'

@pytest.mark.django_db
class TestRolListCreate:

    def test_listar_roles(self, api_client, crear_rol, crear_permiso):
        permiso1 = crear_permiso("Permiso 1")
        permiso2 = crear_permiso("Permiso 2")
        
        crear_rol("Rol 1", [permiso1])
        crear_rol("Rol 2", [permiso2])
        
        response = api_client.get(reverse('rol-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['nombre'] == 'Rol 1'
        assert response.data[1]['nombre'] == 'Rol 2'

    def test_post_rol(self, api_client, crear_permiso):
        permiso1 = crear_permiso("Permiso 1")
        data = {
            "nombre": "Rol Nuevo",
            "permisos": [permiso1.id]
        }
        
        response = api_client.post(reverse('rol-list-create'), data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Rol.objects.count() == 1
        assert Rol.objects.get().nombre == "Rol Nuevo"
        assert Rol.objects.get().permisos.count() == 1
        assert Rol.objects.get().permisos.first().nombre == "Permiso 1"

    def test_crear_rol_invalido(self, api_client):
        data = {
            "permisos": []  # Missing 'nombre'
        }
        
        response = api_client.post(reverse('rol-list-create'), data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestUsuarioListCreate:

    def test_listar_usuarios(self, api_client, crear_usuario, crear_rol, crear_permiso):
        permiso1 = crear_permiso("Permiso 1")
        rol_prueba = crear_rol("Rol 1", [permiso1])
        crear_usuario("usuario1", "usuario1@ejemplo.com", [rol_prueba])
        crear_usuario("usuario2", "usuario2@ejemplo.com", [rol_prueba])
        
        response = api_client.get(reverse('usuario-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['username'] == 'usuario1'
        assert response.data[0]['email'] == 'usuario1@ejemplo.com'

    def test_post_usuario(self, api_client, crear_rol, crear_permiso):
        permiso1 = crear_permiso("Permiso 1")
        rol_prueba = crear_rol("Rol 1", [permiso1])
        data = {
            "username": "usuario_nuevo",
            "email": "usuario_nuevo@ejemplo.com",
            "roles": [rol_prueba.id]
        }
        
        response = api_client.post(reverse('usuario-list-create'), data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Usuario.objects.count() == 1
        assert Usuario.objects.get().username == "usuario_nuevo"
        assert Usuario.objects.get().email == "usuario_nuevo@ejemplo.com"
        assert Usuario.objects.get().roles.count() == 1
        assert Usuario.objects.get().roles.first().nombre == "Rol 1"

    def test_crear_usuario_invalido(self, api_client):
        data = {
            "email": "usuario_sin_username@ejemplo.com"
        }
        
        response = api_client.post(reverse('usuario-list-create'), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestContenidoViews:
    def test_crear_listar_contenido(self, api_client, crear_permiso, crear_rol, crear_usuario, crear_categoria, crear_subcategoria, crear_contenidoo):
        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)

        response = api_client.get(reverse('contenido-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Titulo 1'
        assert response.data[0]['cuerpo'] == 'Cuerpo 1 del contenido'

    def test_crear_contenido(self, api_client, crear_permiso, crear_rol, crear_usuario, crear_categoria, crear_subcategoria, crear_contenidoo):
        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        # crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)

        data = {
            "titulo": "Titulo 1",
            "resumen": "Resumen 1",
            "cuerpo": "Cuerpo 1 del contenido",
            "estado": "borrador",
            "subcategoria": subcategoria1.id,
            "usuario": usuario1.id
        }

        response = api_client.post(reverse('contenido-list-create'), data=data)
        assert response.status_code == status.HTTP_201_CREATED


    def test_inactivar_contenido(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):
        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)

        api_client.force_authenticate(user=usuario1)
        response = api_client.patch(reverse('contenido-inactivar', args=[contenido1.id]))

        assert response.status_code == status.HTTP_200_OK
        contenido1.refresh_from_db()
        assert contenido1.estado == 'inactivo'

    def test_listar_contenidos_aprobados(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):

        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)
        crear_contenidoo("Titulo 2", "Resumen 2", "Cuerpo 2 del contenido", "aprobado", subcategoria1, usuario1)

        response = api_client.get(reverse('contenido-publicado'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Titulo 2'


    def test_buscar_contenidos(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):

        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido jeje", "aprobado", subcategoria1, usuario1)
        crear_contenidoo("Titulo 2", "Resumen 2", "Cuerpo 2 del contenido", "aprobado", subcategoria1, usuario1)

        response = api_client.get(reverse('contenido-busqueda'), {'titulo': 'Titulo 1'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Titulo 1'
        assert response.data[0]['cuerpo'] == 'Cuerpo 1 del contenido jeje'

@pytest.mark.django_db
class TestComentarioViews:

    def test_listar_comentarios(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):
        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)

        comentario1 = Comentario.objects.create(contenido = contenido1, texto ='este es un comentario jeje', usuario = usuario1)
        comentario2 = Comentario.objects.create(contenido = contenido1, texto ='este es un comentario segundo', usuario = usuario1)

        response = api_client.get(reverse('comentario-list-create', args=[contenido1.id]))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['text'] == 'este es un comentario jeje'
        assert response.data[1]['text'] == 'este es un comentario segundo'


    def test_crear_comentario(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):

        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)

        data = {
            "contenido": contenido1.id,
            "texto": "esta esss",
            "usuario": usuario1.id,
        }

        response = api_client.post(reverse('comentario-list-create', args=[contenido1.id]), data=data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Comentario.objects.count() == 1
        assert Comentario.objects.first().texto == "esta esss"

    def test_crear_comentario_con_respuesta(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):
        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)
        comentario1 = Comentario.objects.create(contenido = contenido1, texto ='este es un comentario jeje', usuario = usuario1)

        data = {
            "contenido": contenido1.id,
            "texto": "Respuesta al Comentarioo",
            "usuario": usuario1.id,
            "reply_to": comentario1.id
        }

        response = api_client.post(reverse('comentario-list-create', args=[contenido1.id]), data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comentario.objects.count() == 2
        assert Comentario.objects.last().texto == "Respuesta al Comentarioo"
        assert Comentario.objects.last().reply_to == comentario1

    def test_actualizar_comentario(self, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):

        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)
        comentario1 = Comentario.objects.create(contenido = contenido1, texto ='este es un comentario jeje', usuario = usuario1)

        data = {
            "texto": "Comentario Actualizado"
        }

        response = api_client.patch(reverse('comentario-detail', args=[contenido1.id, comentario1.id]), data=data)

        assert response.status_code == status.HTTP_200_OK
        comentario1.refresh_from_db()
        assert comentario1.texto == "Comentario Actualizado"

    def test_eliminar_comentario(sself, api_client, crear_subcategoria, crear_usuario, crear_contenidoo, crear_permiso, crear_categoria, crear_rol):

        permiso1 = crear_permiso("Permiso 1")
        rol1 = crear_rol("Rol 1", [permiso1])
        usuario1 = crear_usuario("hadi", "emailprueba@gmail.com", [rol1])
        categoria1 = crear_categoria("001", "Categoria 1")
        subcategoria1 = crear_subcategoria("Subcategoria 1", "Descripcion de subcategoria 1", categoria1)
        contenido1 = crear_contenidoo("Titulo 1", "Resumen 1", "Cuerpo 1 del contenido", "borrador", subcategoria1, usuario1)
        comentario1 = Comentario.objects.create(contenido = contenido1, texto ='este es un comentario jeje', usuario = usuario1)

        response = api_client.delete(reverse('comentario-detail', args=[contenido1.id, comentario1.id]))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comentario.objects.count() == 0