import pytest
from rest_framework.exceptions import ValidationError
from cms_backend.models import Parametro, Categoria, Subcategoria, Rol, Permiso, Usuario, Contenido, Comentario
from cms_backend.serializers import (
    ParametroSerializer,
    CategoriaSerializer,
    SubcategoriaSerializer,
    ComentarioSerializer,
    ContenidoSerializer,
    UsuarioSerializer,
    RolSerializer,
    RolCreateUpdateSerializer,
    RolConPermisosSerializer,
    UsuarioConRolesYPermisosSerializer
)

@pytest.fixture(scope='module')
def test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield

@pytest.mark.django_db
def test_parametro_serializer(test_db):
    parametro = Parametro.objects.create(nombre='Test Parametro', valor='Test Valor')
    serializer = ParametroSerializer(parametro)
    assert serializer.data == {'id': parametro.id, 'nombre': 'Test Parametro', 'valor': 'Test Valor'}

@pytest.mark.django_db
def test_categoria_serializer(test_db):
    categoria = Categoria.objects.create(codigo='CAT001', nombre='Test Categoria')
    serializer = CategoriaSerializer(categoria)
    assert serializer.data == {'id': categoria.id, 'codigo': 'CAT001', 'nombre': 'Test Categoria'}

@pytest.mark.django_db
def test_subcategoria_serializer_unique_nombre(test_db):
    categoria = Categoria.objects.create(codigo='CAT001', nombre='Test Categoria')
    Subcategoria.objects.create(nombre='Test Subcategoria', descripcion='Desc', categoria=categoria)

    serializer = SubcategoriaSerializer(data={'nombre': 'Test Subcategoria', 'descripcion': 'Desc', 'categoria': categoria.id})
    
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)

    assert 'El nombre de la subcategoría debe ser único dentro de la categoría.' in str(excinfo.value)

@pytest.mark.django_db
def test_comentario_serializer(test_db):
    usuario = Usuario.objects.create(username='testuser', email='test@ejemplo.com')
    contenido = Contenido.objects.create(titulo='Test Contenido', resumen='Resumen', cuerpo='Cuerpo', autor=usuario)
    comentario = Comentario.objects.create(texto='Test Comentario', usuario=usuario, contenido=contenido)

    serializer = ComentarioSerializer(comentario)
    assert 'userId' in serializer.data
    assert serializer.data['text'] == 'Test Comentario'

@pytest.mark.django_db
def test_contenido_serializer(test_db):
    usuario = Usuario.objects.create(username='testuser', email='test@ejemplo.com')
    subcategoria = Subcategoria.objects.create(nombre='Subcat', descripcion='Desc', categoria=Categoria.objects.create(codigo='CAT001', nombre='Test Categoria'))
    contenido = Contenido.objects.create(titulo='Test Contenido', resumen='Resumen', cuerpo='Cuerpo', subcategoria=subcategoria, autor=usuario)
    
    serializer = ContenidoSerializer(contenido)
    assert serializer.data['titulo'] == 'Test Contenido'

@pytest.mark.django_db
def test_usuario_serializer_create(test_db):
    rol = Rol.objects.create(nombre='Test Rol')
    serializer = UsuarioSerializer(data={'username': 'testuser', 'email': 'test@ejemplo.com', 'roles': [rol.id]})
    assert serializer.is_valid()
    usuario = serializer.save()
    assert usuario.username == 'testuser'
    assert usuario.roles.count() == 1

@pytest.mark.django_db
def test_rol_serializer(test_db):
    permiso = Permiso.objects.create(nombre='Test Permiso')
    rol = Rol.objects.create(nombre='Test Rol')
    rol.permisos.add(permiso)
    
    serializer = RolSerializer(rol)
    assert serializer.data['nombre'] == 'Test Rol'

@pytest.mark.django_db
def test_rol_create_update_serializer(test_db):
    permiso = Permiso.objects.create(nombre='Test Permiso')
    rol = Rol.objects.create(nombre='Test Rol')
    data = {'nombre': 'Rol Actualizado', 'permisos': [permiso.id]}
    
    serializer = RolCreateUpdateSerializer(rol, data=data)
    assert serializer.is_valid()
    updated_rol = serializer.save()
    assert updated_rol.nombre == 'Rol Actualizado'

@pytest.mark.django_db
def test_usuario_con_roles_y_permisos_serializer(test_db):
    rol = Rol.objects.create(nombre='Test Roll')
    permiso = Permiso.objects.create(nombre='Test Permiso')
    rol.permisos.add(permiso)
    usuario = Usuario.objects.create(username='testuser', email='test@ejemplo.com')
    usuario.roles.add(rol)

    serializer = UsuarioConRolesYPermisosSerializer(usuario)
    assert serializer.data['username'] == 'testuser'
    assert len(serializer.data['roles']) == 1
    assert serializer.data['roles'][0]['nombre'] == 'Test Roll'