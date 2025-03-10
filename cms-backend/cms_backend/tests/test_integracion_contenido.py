import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from cms_backend.models import Contenido, Usuario, Subcategoria,Categoria,Permiso,Rol

@pytest.fixture(scope='module')
def test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield

@pytest.mark.django_db
def test_crear_aprobar_rechazar_contenido():
    client = APIClient()

    # 1. Crear una categoría
    categoria = Categoria.objects.create(codigo="001", nombre="Categoría Test")

    # 2. Crear una subcategoría asociada a la categoría
    subcategoria = Subcategoria.objects.create(nombre="Subcategoría Test", descripcion="Descripción de prueba", categoria=categoria)

    # 3. Crear permisos y roles para el usuario
    permiso = Permiso.objects.create(nombre="Permiso Test")
    rol = Rol.objects.create(nombre="Rol Test")
    rol.permisos.add(permiso)

    # 4. Crear un usuario con el rol asignado
    usuario = Usuario.objects.create(username="autor1", email="autor1@example.com")
    usuario.roles.add(rol)

    # 5. Crear un contenido con estado "en_revision"
    url = reverse('contenido-list-create')
    data = {
        "titulo": "Prueba de contenido",
        "resumen": "Resumen de prueba",
        "cuerpo": "Cuerpo de prueba",
        "estado": "en_revision",
        "subcategoria": subcategoria.id,  # Relacionar con la subcategoría creada
        "autor": usuario.id  # Relacionar con el usuario creado
    }
    response = client.post(url, data, format='json')

    # Verifica que el contenido fue creado correctamente con estado "en_revision"
    assert response.status_code == 201  # Created
    assert response.data['titulo'] == 'Prueba de contenido'
    assert response.data['estado'] == 'en_revision'

    # 6. Obtener el contenido recién creado
    contenido_id = response.data['id']
    get_url = reverse('contenido-detail', args=[contenido_id])
    get_response = client.get(get_url)
    
    assert get_response.status_code == 200
    assert get_response.data['estado'] == 'en_revision'
    
    # 7. Aprobar el contenido (simular llamada al método aprobar)
    contenido = Contenido.objects.get(id=contenido_id)
    contenido.aprobar()

    # Verifica que el contenido ahora esté aprobado
    contenido.refresh_from_db()  # Refresca el contenido desde la base de datos
    assert contenido.estado == 'aprobado'

    # 8. Rechazar el contenido (simular llamada al método rechazar)
    contenido.rechazar("No cumple con los requisitos")