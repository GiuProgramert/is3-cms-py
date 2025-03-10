"""
**URL configuration for cms_backend project.**

This file contains the URL mappings for the Django project. It defines which views should be called based on the URL path.

Examples:
- Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
- Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
- Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

**URLs de Historial**

Estas rutas manejan las operaciones de creación, listado, actualización, y eliminación de instancias del modelo `Historial`.

Rutas:
- 'historial/': 
    - Vista asociada: `HistorialListCreateView`.
    - Descripción: Permite listar todos los registros de `Historial` y crear nuevos registros.
    - Métodos HTTP soportados:
        - GET: Devuelve la lista de todos los registros en `Historial`.
        - POST: Crea un nuevo registro en `Historial`.

- 'historial/<int:pk>/': 
    - Vista asociada: `HistorialRetrieveUpdateDestroyView`.
    - Descripción: Permite obtener, actualizar o eliminar un registro de `Historial` específico.
    - Parámetro:
        - pk (int): Identificador único del registro de `Historial`.
    - Métodos HTTP soportados:
        - GET: Devuelve los detalles de un registro específico.
        - PUT/PATCH: Actualiza el registro de `Historial` correspondiente al `pk` dado.
        - DELETE: Elimina el registro de `Historial` correspondiente al `pk` dado.
        
**URLs de Likes**

Estas rutas manejan las operaciones de creación, listado y eliminación de instancias del modelo `Like`.

Rutas:
- 'likes/':
    - Vista asociada: `LikeCreateView`.
    - Descripción: Permite crear un nuevo `Like` en un contenido específico por un usuario.
    - Métodos HTTP soportados:
        - POST: Crea un nuevo registro de `Like`.

- 'likes/contenido/<int:contenido_id>/':
    - Vista asociada: `LikeListView`.
    - Descripción: Permite listar todos los `Likes` asociados a un contenido específico.
    - Parámetro:
        - contenido_id (int): Identificador único del contenido al cual están asociados los `Likes`.
    - Métodos HTTP soportados:
        - GET: Devuelve la lista de `Likes` asociados al contenido especificado.

- 'likes/delete/<int:contenido_id>/<int:usuario_id>/':
    - Vista asociada: `LikeDeleteView`.
    - Descripción: Permite eliminar un `Like` específico de un contenido por un usuario específico.
    - Parámetros:
        - contenido_id (int): Identificador único del contenido al cual está asociado el `Like`.
        - usuario_id (int): Identificador único del usuario que dio el `Like`.
    - Métodos HTTP soportados:
        - DELETE: Elimina el `Like` correspondiente al `contenido_id` y `usuario_id` especificados. Devuelve 
        un mensaje de error si no existe.

**URLs Articulo**

Endpoint: /articulos/aprobados/<str:fecha_inicio>/<str:fecha_fin>/

Método HTTP: GET

Descripción: Este endpoint permite contar la cantidad de artículos que han sido aprobados en un rango de fechas 
especificado. Utiliza las fechas de inicio y fin proporcionadas para filtrar los artículos aprobados.

Parámetros de la URL:

    fecha_inicio (str): Fecha de inicio del rango en formato AAAA-MM-DD.
    fecha_fin (str): Fecha de fin del rango en formato AAAA-MM-DD.

Respuesta:

    200 OK: Devuelve la cantidad de artículos aprobados en el rango de fechas especificado.
    400 Bad Request: Si el formato de las fechas es inválido.

** Comentarios **
Configuración de rutas y documentación para la API del proyecto CMS-24.

Este módulo define las rutas para acceder a las vistas de comentarios y 
la documentación generada automáticamente mediante Swagger.

Clases y Funciones:
    schema_view: Configura la vista de la documentación de la API utilizando 
                 drf_yasg con opciones de contacto, licencia, y términos de uso.
    urlpatterns: Lista de rutas definidas para la API, incluyendo el esquema de 
                 documentación.

Ejemplo de Uso:
    Este archivo puede usarse como parte de las configuraciones de rutas en un
    proyecto Django, permitiendo la generación automática de documentación.

Importaciones:
    ComentarioListCreateView: Vista para listar y crear comentarios.
    ComentarioDetailView: Vista para ver el detalle de un comentario.
    permissions: Módulo de permisos de Django REST Framework.
    get_schema_view: Función de drf_yasg para configurar la vista del esquema.
    openapi: Módulo de drf_yasg para definir la estructura de la documentación.

**Permisos**
URLs de Permiso
Estas rutas manejan la operación de listado de permisos en el sistema.
Rutas:
    'permisos/':
        Vista asociada: PermisoListView.
        Descripción: Permite listar todos los permisos existentes en el sistema.
        Método HTTP soportado:
            GET: Devuelve la lista de todos los permisos registrados en el sistema.
    'swagger(?P<format>.json|.yaml)$':
        Vista asociada: schema_view.without_ui().
        Descripción: Permite obtener el esquema de la API en formato JSON o YAML, usado para generar la documentación 
        interactiva de la API.
        Parámetro:
            format (string): El formato del esquema que se solicita, puede ser .json o .yaml.
        Método HTTP soportado:
            GET: Devuelve el esquema de la API en el formato especificado (JSON o YAML).
Ejemplo de uso de las URLs
    GET /permisos/:
        Devuelve todos los permisos existentes en el sistema.
    GET /swagger.json o GET /swagger.yaml:
        Devuelve el esquema de la API en formato JSON o YAML respectivamente, utilizado para documentar las rutas 
        y operaciones disponibles en la API.

**Roles**
Rutas:
    'roles/':
        Vista asociada: RolListCreateView.
        Descripción: Permite listar todos los roles existentes y crear un nuevo rol.
        Métodos HTTP soportados:
            GET: Devuelve la lista de todos los roles registrados en el sistema.
            POST: Crea un nuevo rol con los datos proporcionados en la solicitud.
    'roles/int:pk/':
        Vista asociada: RolDetailView.
        Descripción: Permite obtener los detalles de un rol específico mediante su identificador único pk.
        Parámetro:
            pk (int): Identificador único del rol que se desea obtener.
        Métodos HTTP soportados:
            GET: Devuelve la información detallada del rol con el identificador pk especificado.
            PUT: Actualiza los detalles del rol con el identificador pk especificado.
            DELETE: Elimina el rol con el identificador pk especificado.
Ejemplo de uso de las URLs
    POST /roles/:
        Crea un nuevo rol proporcionando los datos necesarios en el cuerpo de la solicitud.
    GET /roles/{pk}/:

        Obtiene los detalles del rol con el id (pk) especificado.

**Usuarios**
Rutas:
    'usuarios/':
        Vista asociada: UsuarioListCreateView.
        Descripción: Permite listar todos los usuarios y crear un nuevo usuario.
        Métodos HTTP soportados:
            GET: Devuelve la lista de todos los usuarios registrados en el sistema.
            POST: Crea un nuevo usuario con los datos proporcionados en la solicitud.
    'usuarios/int:pk/':
        Vista asociada: UsuarioDetailView.
        Descripción: Permite obtener los detalles de un usuario específico mediante su identificador único pk.
        Parámetro:
            pk (int): Identificador único del usuario que se desea obtener.
        Métodos HTTP soportados:
            GET: Devuelve la información detallada del usuario con el identificador pk especificado.
            PUT: Actualiza los detalles del usuario con el identificador pk especificado.
            DELETE: Elimina el usuario con el identificador pk especificado.
    'usuarios/email/str:email/':
        Vista asociada: ObtenerUsuarioPorEmailView.
        Descripción: Permite obtener un usuario específico mediante su dirección de correo electrónico.
        Parámetro:
            email (str): Dirección de correo electrónico del usuario que se desea obtener.
        Métodos HTTP soportados:
            GET: Devuelve la información del usuario correspondiente a la dirección de correo electrónico especificada.
Ejemplo de uso de las URLs
    POST /usuarios/:
        Crea un nuevo usuario proporcionando los datos necesarios en el cuerpo de la solicitud.
    GET /usuarios/{pk}/:
        Obtiene los detalles del usuario con el id (pk) especificado.
    GET /usuarios/email/{email}/:

        Obtiene el usuario que tiene la dirección de correo electrónico especificada.

**Vistas**
URLs de Registro de Vista

Estas rutas manejan la operación de registrar una vista de un usuario en un contenido específico.
Rutas:

    'registrar_vista/':
        Vista asociada: registrar_vista.
        Descripción: Registra una vista de un usuario en un contenido específico. Si el usuario ya ha visto el contenido,
        se devuelve un mensaje indicando esto.
        Métodos HTTP soportados:
            POST: Permite registrar una vista de un contenido por un usuario. Si el usuario ya ha visto este contenido, 
            se devuelve un mensaje indicando que ya lo ha visto.
        Cuerpo de la solicitud (Request body):
            contenido_id (int): ID del contenido que se está viendo.
            usuario_id (int): ID del usuario que está viendo el contenido.
Ejemplo de uso de la URL

    POST /registrar_vista/:
        Descripción: Registra la vista de un contenido por parte de un usuario. Si el usuario no ha visto el contenido 
        antes, se crea un nuevo registro de vista. Si ya lo ha visto, se devuelve un mensaje indicando que ya ha registrado 
        la vista.
"""
from django.contrib import admin
from django.urls import path, re_path
from .views import ContarArticulosAprobadosView, ParametroListCreate, ParametroRetrieveUpdate, CategoriaListCreate, CategoriaRetrieveUpdateDestroy
from .views import SubcategoriaListCreate, SubcategoriaRetrieveUpdateDestroy, SendEmailView
from .views import HistorialListCreateView, HistorialRetrieveUpdateDestroyView, LikeCreateView, LikeDeleteView, LikeListView, ParametroListCreate, ParametroRetrieveUpdate, CategoriaListCreate, CategoriaRetrieveUpdateDestroy
from .views import SubcategoriaListCreate, SubcategoriaRetrieveUpdateDestroy
from .views import ContenidoListCreate, ContenidoRetrieveUpdate, ContenidoInactivar, ContenidoPublicadoList, ContenidoSearch
from .views import ContenidoAprobarRechazar,ObtenerUsuarioPorEmailView,CategoriaListCreate, CambiarEstadoView,ContarArticulosInactivosView,ContenidoMasLikesView,ContarEstadosView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    UsuarioListCreateView, UsuarioDetailView, RolListCreateView, 
    RolDetailView, PermisoListView, UsuarioByEmailView,ContenidosMasVistosAPIView
)
# TODO: implementar comentarios
from .views import ComentarioListCreateView, ComentarioDetailView,TopContenidosMasVistosAPIView
from .views import registrar_vista
# Configuración de la vista para la documentación de la API
schema_view = get_schema_view(
    openapi.Info(
        title="CMS-24 API",# Título de la API para la documentación
        default_version='v1', # Versión actual de la API
        description="Documentación de la API del proyecto CMS-24", # Breve descripción de la API
        terms_of_service="https://www.cms.com/terms/", # URL a los términos y condiciones
        contact=openapi.Contact(email="contact@cms.com"), # Información de contacto
        license=openapi.License(name="MIT License"), # Tipo de licencia de la API
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Permitir acceso público a la documentación
)

urlpatterns = [
    # Ruta para la documentación en formato JSON o YAML
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Ruta para ver la documentación en Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Ruta para ver la documentación en Redoc
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Otros endpoints de tu API...
]

# Mapeo de URLs a vistas específicas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('parametros/', ParametroListCreate.as_view(), name='listar_crear_parametros'),
    path('parametros/<int:id>/', ParametroRetrieveUpdate.as_view(), name='modificar_parametro'),
    path('categorias/', CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', CategoriaRetrieveUpdateDestroy.as_view(), name='categoria-detail'),
    path('subcategorias/', SubcategoriaListCreate.as_view(), name='subcategoria-list-create'),
    path('subcategorias/<int:pk>/', SubcategoriaRetrieveUpdateDestroy.as_view(), name='subcategoria-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('contenido/', ContenidoListCreate.as_view(), name='contenido-list-create'),
    path('contenido/<int:pk>/', ContenidoRetrieveUpdate.as_view(), name='contenido-detail'),
    path('contenido/<int:pk>/inactivar/', ContenidoInactivar.as_view(), name='contenido-inactivar'),
    path('contenido/publicado/', ContenidoPublicadoList.as_view(), name='contenido-publicado'),
    path('contenido/busqueda/', ContenidoSearch.as_view(), name='contenido-busqueda'),
    path('contenido/<int:pk>/aprobar_rechazar/', ContenidoAprobarRechazar.as_view(), name='aprobar-rechazar-contenido'),
    path('contenido/<int:contenido_id>/cambiar-estado/', CambiarEstadoView.as_view(), name='cambiar-estado'),
    # Usuario URLs
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('usuarios/email/<str:email>/', ObtenerUsuarioPorEmailView.as_view(), name='usuario_por_email'),
    
    # Rol URLs
    path('roles/', RolListCreateView.as_view(), name='rol-list-create'),
    path('roles/<int:pk>/', RolDetailView.as_view(), name='rol-detail'),
    
    # Permiso URLs
    path('permisos/', PermisoListView.as_view(), name='permiso-list'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Comentarios URLs
    #path('contenidos/<int:contenido_id>/comentarios/', ComentarioListCreateView.as_view(), name='comentarios-list-create'),
    #path('comentarios/<int:contenido_id>/', ComentarioListCreateView.as_view(), name='comentarios-list-create'),
    #path('contenidos/<int:contenido_id>/comentarios/<int:pk>/', ComentarioDetailView.as_view(), name='comentario-detail'),  # Ruta para detalles
# URL para listar y crear comentarios asociados a un contenido específico
    path('contenido/<int:contenido_id>/comentarios/', ComentarioListCreateView.as_view(), name='comentario-list-create'),
    
    # URL para obtener, actualizar o eliminar un comentario específico
    path('contenido/<int:contenido_id>/comentarios/<int:pk>/', ComentarioDetailView.as_view(), name='comentario-detail'),
  # Historial URLs
    path('historial/', HistorialListCreateView.as_view(), name='historial-list-create'),
    path('historial/<int:pk>/', HistorialRetrieveUpdateDestroyView.as_view(), name='historial-detail'),
    #path para enviar emails
    path('send-email/', SendEmailView.as_view(), name='send_email'),

    # Likes URLs
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('likes/contenido/<int:contenido_id>/', LikeListView.as_view(), name='like-list'),
    path('likes/delete/<int:contenido_id>/<int:usuario_id>/', LikeDeleteView.as_view(), name='like-delete'),  # Cambiado  # Cambia esta línea

    # articulos redactados
    path('articulos/aprobados/<str:fecha_inicio>/<str:fecha_fin>/', ContarArticulosAprobadosView.as_view(),name='contar_articulos_aprobados'),
    path('articulos/inactivos/<str:fecha_inicio>/<str:fecha_fin>/', ContarArticulosInactivosView.as_view(), name='articulos-inactivos'),
    path('articulos/mas-likes/', ContenidoMasLikesView.as_view(), name='contenido-mas-likes'),
    path('articulos/contar-estados/<str:fecha_inicio>/<str:fecha_fin>/', ContarEstadosView.as_view(), name='contar-estados'),

    #vistas
    path('registrar_vista/', registrar_vista, name='registrar_vista'),
    path('vistas/top-5/', TopContenidosMasVistosAPIView.as_view(), name='contenidos_mas_vistos'),
    path('contenidos_mas_vistos/<str:fecha_inicio>/<str:fecha_fin>/', ContenidosMasVistosAPIView.as_view(), name='contenidos_mas_vistos'),]

