import pytest
from cms_backend.models import Categoria, Subcategoria, Permiso, Rol, Usuario, Contenido, Comentario

@pytest.fixture(scope='module')
def test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield

@pytest.mark.django_db
class TestCategoriaModel:

    def test_crear_categoria(self):
        categoria = Categoria.objects.create(codigo='001', nombre='electronica')
        assert categoria.id is not None
        assert categoria.codigo == '001'
        assert categoria.nombre == 'electronica'

    def test_unique_codigo(self):
        Categoria.objects.create(codigo='002', nombre='libros')
        with pytest.raises(Exception):
            Categoria.objects.create(codigo='002', nombre='mas libros')

    def test_str(self):
        categoria = Categoria(codigo='003', nombre='ropa')
        assert str(categoria) == 'ropa'


@pytest.mark.django_db
class TestSubcategoriaModel:

    def test_crear_subcategoria(self):
        categoria = Categoria.objects.create(codigo='001', nombre='electronica')
        subcategoria = Subcategoria.objects.create(
            nombre='televisores',
            descripcion='Televisores de última generación',
            categoria=categoria
        )
        assert subcategoria.id is not None
        assert subcategoria.nombre == 'televisores'
        assert subcategoria.descripcion == 'Televisores de última generación'
        assert subcategoria.categoria == categoria
        assert str(subcategoria) == 'televisores'

    def test_crear_subcategoria_sin_categoria(self):
        with pytest.raises(Exception):
            Subcategoria.objects.create(nombre='audio', descripcion='Sistemas de audio')

@pytest.mark.django_db
class TestPermisoModel:

    def test_crear_permiso(self):
        permiso = Permiso.objects.create(nombre='editar')
        assert permiso.id is not None
        assert permiso.nombre == 'editar'
        assert str(permiso) == 'editar'


@pytest.mark.django_db
class TestRolModel:

    def test_crear_rol(self):
        rol = Rol.objects.create(nombre='administrador')
        permiso = Permiso.objects.create(nombre='publicar')
        rol.permisos.add(permiso)
        assert rol.id is not None
        assert rol.nombre == 'administrador'
        assert str(rol) == 'administrador'
        assert rol.permisos.count() == 1
        assert rol.permisos.first() == permiso


@pytest.mark.django_db
class TestUsuarioModel:

    def test_crear_usuario(self):
        rol = Rol.objects.create(nombre='administrador')
        usuario = Usuario.objects.create(username='usuarioprueba', email='email@ejemplo.com')
        usuario.roles.add(rol)

        assert usuario.id is not None
        assert usuario.username == 'usuarioprueba'
        assert usuario.email == 'email@ejemplo.com'
        assert usuario.roles.count() == 1
        assert rol in usuario.roles.all()
        assert str(usuario) == 'usuarioprueba'

    def test_unique_username(self):
        Usuario.objects.create(username='usuarioprueba', email='email1@ejemplo.com')
        with pytest.raises(Exception):
            Usuario.objects.create(username='usuarioprueba', email='email2@ejemplo.com')

    def test_unique_email(self):
        Usuario.objects.create(username='usuarioprueba1', email='email@ejemplo.com')
        with pytest.raises(Exception):
            Usuario.objects.create(username='usuarioprueba2', email='email@ejemplo.com')


@pytest.mark.django_db
class TestContenidoModel:

    def test_crear_contenido(self):
        categoria = Categoria.objects.create(codigo='001', nombre='electronica')
        subcategoria = Subcategoria.objects.create(nombre='televisores', descripcion='Televisores de última generación', categoria=categoria)
        autor = Usuario.objects.create(username='autorprueba', email='autor@ejemplo.com')

        contenido = Contenido.objects.create(
            titulo='Nuevo Televisor',
            resumen='Resumen del nuevo televisor',
            cuerpo='Cuerpo del contenido del nuevo televisor',
            multimedia='',
            estado='borrador',
            subcategoria=subcategoria,
            autor=autor
        )
        
        assert contenido.id is not None
        assert contenido.titulo == 'Nuevo Televisor'
        assert contenido.estado == 'borrador'
        assert contenido.subcategoria == subcategoria
        assert contenido.autor == autor
        assert str(contenido) == 'Nuevo Televisor'

        contenido.aprobar()
        assert contenido.estado == 'aprobado'

        contenido.rechazar(comentarios='No cumple con los requisitos.')
        assert contenido.estado == 'rechazado'


@pytest.mark.django_db
class TestComentarioModel:

    def test_crear_comentario(self):
        categoria = Categoria.objects.create(codigo='001', nombre='electronica')
        subcategoria = Subcategoria.objects.create(
            nombre='televisores',
            descripcion='Televisores de última generación',
            categoria=categoria
        )
        autor = Usuario.objects.create(username='autorprueba', email='autor@ejemplo.com')
        contenido = Contenido.objects.create(
            titulo='Nuevo Televisor',
            resumen='Resumen del nuevo televisor',
            cuerpo='Cuerpo del contenido del nuevo televisor',
            multimedia='',
            estado='borrador',
            subcategoria=subcategoria,
            autor=autor
        )
        
        comentario = Comentario.objects.create(
            contenido=contenido,
            texto='Probando comentario.',
            usuario=autor,
            avatarUrl='http://ejemplo.com/foto.png'
        )

        reply = Comentario.objects.create(
            contenido=contenido,
            texto='Esta es una respuesta.',
            usuario=autor,
            reply_to=comentario
        )
        
        assert comentario.id is not None
        assert comentario.texto == 'Probando comentario.'
        assert comentario.usuario == autor
        assert comentario.contenido == contenido
        assert comentario.avatarUrl == 'http://ejemplo.com/foto.png'
        assert str(comentario) == 'autorprueba: Probando comentario.'
        assert reply.id is not None
        assert reply.reply_to == comentario
        assert reply.texto == 'Esta es una respuesta.'
        assert comentario.replies.count() == 1
        assert reply in comentario.replies.all()