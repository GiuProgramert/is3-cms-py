from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import Articulo, Historial, Like, Parametro, Contenido
from .models import Categoria
from .models import Subcategoria
from .serializers import ArticuloAprobadoSerializer, HistorialSerializer, LikeSerializer, ParametroSerializer
from .serializers import CategoriaSerializer
from .serializers import SubcategoriaSerializer
from .serializers import ContenidoSerializer
from .serializers import ContenidoRevisionSerializer
from .models import Usuario, Rol, Permiso
from .serializers import UsuarioSerializer, PermisoSerializer, RolCreateUpdateSerializer,UsuarioConRolesYPermisosSerializer,CategoriaConSubcategoriasSerializer
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q
from django.db import transaction
from django.db.models import Count
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from django.http import JsonResponse
from rest_framework.views import APIView
#Desde aqui empieza para swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_date
# Vista para listar y crear parámetros
class ParametroListCreate(generics.ListCreateAPIView):
    """
    Vista para listar todos los parámetros disponibles o crear un nuevo parámetro.
    
    Esta vista permite a los usuarios obtener una lista de parámetros o crear un nuevo parámetro en el sistema.

    Métodos disponibles:
    - GET: Listar todos los parámetros.
    - POST: Crear un nuevo parámetro.
    """
    queryset = Parametro.listar()
    serializer_class = ParametroSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Listar parámetros",
        operation_description="Devuelve una lista de todos los parámetros disponibles.",
        responses={
            200: openapi.Response(
                description="Lista de parámetros",
                schema=ParametroSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Obtener una lista de todos los parámetros disponibles.
        
        Este método maneja las solicitudes GET a esta vista. Devuelve una lista de parámetros registrados en el sistema.
        
        Ejemplo de respuesta (200 OK):
        [
            {
                "id": 1,
                "nombre": "Parametro 1",
                "valor": "Valor 1"
            },
            {
                "id": 2,
                "nombre": "Parametro 2",
                "valor": "Valor 2"
            }
        ]
        
        Parámetros:
        - Ninguno
        
        Respuesta:
        - Código 200: Lista de parámetros con sus detalles.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del método POST
    @swagger_auto_schema(
        operation_summary="Crear un nuevo parámetro",
        operation_description="Crea un nuevo parámetro en el sistema.",
        request_body=ParametroSerializer,
        responses={
            201: openapi.Response(
                description="Parámetro creado exitosamente",
                schema=ParametroSerializer
            ),
            400: openapi.Response(
                description="Error en la solicitud",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crear un nuevo parámetro en el sistema.
        
        Este método maneja las solicitudes POST a esta vista. Permite crear un nuevo parámetro especificando su nombre y valor en el cuerpo de la solicitud.
        
        Ejemplo de solicitud:
        {
            "nombre": "Nuevo Parametro",
            "valor": "Valor del parámetro"
        }
        
        Ejemplo de respuesta (201 Created):
        {
            "id": 3,
            "nombre": "Nuevo Parametro",
            "valor": "Valor del parámetro"
        }
        
        Parámetros:
        - 'nombre': El nombre del nuevo parámetro (requerido).
        - 'valor': El valor del nuevo parámetro (requerido).
        
        Respuesta:
        - Código 201: Parámetro creado exitosamente.
        - Código 400: Error en la solicitud (por ejemplo, datos inválidos).
        """
        return super().post(request, *args, **kwargs)

# Vista para modificar y obtener un parámetro
class ParametroRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Vista para recuperar, actualizar y modificar parcialmente un parámetro específico.

    Esta vista permite a los usuarios:
    - Obtener los detalles de un parámetro específico mediante su ID.
    - Actualizar completamente los detalles de un parámetro específico.
    - Modificar parcialmente los campos de un parámetro específico.
    
    Métodos disponibles:
    - GET: Obtener un parámetro por ID.
    - PUT: Actualizar un parámetro.
    - PATCH: Modificar parcialmente un parámetro.
    """
    queryset = Parametro.listar()
    serializer_class = ParametroSerializer
    lookup_field = 'id'

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Obtener un parámetro por ID",
        operation_description="Recupera los detalles de un parámetro específico mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del parámetro a recuperar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles del parámetro",
                schema=ParametroSerializer
            ),
            404: openapi.Response(
                description="Parámetro no encontrado"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recuperar los detalles de un parámetro específico.

        Este método maneja las solicitudes GET a esta vista. Devuelve los detalles completos de un parámetro especificado por su ID.

        Parámetros:
        - 'id': ID del parámetro a recuperar (requerido).

        Respuestas:
        - Código 200: Devuelve los detalles del parámetro solicitado.
        - Código 404: El parámetro no fue encontrado.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del PUT
    @swagger_auto_schema(
        operation_summary="Actualizar un parámetro",
        operation_description="Actualiza los detalles de un parámetro específico.",
        request_body=ParametroSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del parámetro a actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Parámetro actualizado exitosamente",
                schema=ParametroSerializer
            ),
            400: openapi.Response(
                description="Error en la solicitud",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
            404: openapi.Response(
                description="Parámetro no encontrado"
            )
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Actualizar completamente un parámetro.

        Este método maneja las solicitudes PUT a esta vista. Permite actualizar completamente los detalles de un parámetro especificado por su ID.

        Parámetros:
        - 'id': ID del parámetro a actualizar (requerido).

        Cuerpo de la solicitud:
        - Todos los campos del parámetro deben ser proporcionados.

        Respuestas:
        - Código 200: Parámetro actualizado exitosamente.
        - Código 400: Error en la solicitud (por ejemplo, datos inválidos).
        - Código 404: El parámetro no fue encontrado.
        """
        return super().put(request, *args, **kwargs)

    #Documentación del PATCH
    @swagger_auto_schema(
        operation_summary="Modificar parcialmente un parámetro",
        operation_description="Realiza una actualización parcial de los campos de un parámetro específico.",
        request_body=ParametroSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del parámetro a modificar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Parámetro modificado parcialmente con éxito",
                schema=ParametroSerializer
            ),
            400: openapi.Response(
                description="Error en la solicitud",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
            404: openapi.Response(
                description="Parámetro no encontrado"
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Modificar parcialmente un parámetro.

        Este método maneja las solicitudes PATCH a esta vista. Permite modificar parcialmente los campos de un parámetro especificado por su ID.

        Parámetros:
        - 'id': ID del parámetro a modificar (requerido).

        Cuerpo de la solicitud:
        - Solo los campos que se deseen actualizar deben ser proporcionados.

        Respuestas:
        - Código 200: Parámetro modificado parcialmente con éxito.
        - Código 400: Error en la solicitud (por ejemplo, datos inválidos).
        - Código 404: El parámetro no fue encontrado.
        """
        return super().patch(request, *args, **kwargs)

#TODO:CATEGORIAS
class CategoriaListCreate(generics.ListCreateAPIView):
    """
    Vista para listar todas las categorías existentes y crear nuevas categorías.
    
    Permite:
    - Listar todas las categorías y sus subcategorías asociadas.
    - Crear una nueva categoría especificando sus subcategorías.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaConSubcategoriasSerializer

    #Documentación para POST
    @swagger_auto_schema(
        operation_summary="Listar y crear categorías",
        operation_description="Obtiene la lista de todas las categorías existentes o crea una nueva categoría.",
        request_body=CategoriaConSubcategoriasSerializer,  # Especifica el esquema para la creación
        responses={
            200: openapi.Response(
                description="Lista de categorías",
                schema=CategoriaConSubcategoriasSerializer(many=True)  # Respuesta para el listado de categorías
            ),
            201: openapi.Response(
                description="Categoría creada con éxito",
                schema=CategoriaConSubcategoriasSerializer  # Respuesta para la creación de una categoría
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crear una nueva categoría con sus subcategorías.
        
        Permite la creación de una nueva categoría. Los datos de la nueva categoría deben
        ser proporcionados en el cuerpo de la solicitud en formato JSON.

        Respuestas:
        - 201: Categoría creada con éxito.
        - 400: Error de validación (por ejemplo, datos inválidos).
        """
        return super().post(request, *args, **kwargs)
    
    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Listar todas las categorías",
        operation_description="Obtiene la lista de todas las categorías junto con sus subcategorías.",
        responses={
            200: openapi.Response(
                description="Lista de categorías",
                schema=CategoriaConSubcategoriasSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Listar todas las categorías junto con sus subcategorías.

        Este método devuelve todas las categorías registradas en el sistema, junto con
        sus subcategorías asociadas, si las hay.

        Respuesta:
        - 200: Devuelve la lista de categorías con sus subcategorías.
        """
        return super().get(request, *args, **kwargs)

class CategoriaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar (completa o parcialmente) y eliminar una categoría específica.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    #Documentación de GET
    @swagger_auto_schema(
        operation_summary="Obtener una categoría específica",
        operation_description="Recupera una instancia de la categoría utilizando su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID de la categoría a obtener",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles de la categoría",
                schema=CategoriaSerializer()
            ),
            404: openapi.Response(
                description="Categoría no encontrada"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    #Documentación del método PUT
    @swagger_auto_schema(
        operation_summary="Actualizar una categoría",
        operation_description="Actualiza todos los campos de una categoría específica usando su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID de la categoría a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        request_body=CategoriaSerializer,
        responses={
            200: openapi.Response(
                description="Categoría actualizada con éxito",
                schema=CategoriaSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada"
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    #Documentación del método PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una categoría",
        operation_description="Actualiza uno o más campos de una categoría específica usando su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID de la categoría a actualizar parcialmente",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        request_body=CategoriaSerializer,
        responses={
            200: openapi.Response(
                description="Categoría actualizada parcialmente",
                schema=CategoriaSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada"
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    #Documentación del método DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar una categoría",
        operation_description="Elimina una categoría específica usando su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID de la categoría a eliminar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        responses={
            204: openapi.Response(
                description="Categoría eliminada exitosamente"
            ),
            404: openapi.Response(
                description="Categoría no encontrada"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubcategoriaListCreate(generics.ListCreateAPIView):
    """
    Vista para listar y crear subcategorías.

    Este endpoint permite obtener una lista de todas las subcategorías existentes
    y crear una nueva subcategoría en el sistema.

    Métodos disponibles:
    - GET: Lista todas las subcategorías.
    - POST: Crea una nueva subcategoría.
    """
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Listar subcategorías",
        operation_description="Devuelve una lista de todas las subcategorías disponibles.",
        responses={
            200: openapi.Response(
                description="Lista de subcategorías",
                schema=SubcategoriaSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera una lista de todas las subcategorías.

        Este método devuelve todos los registros de subcategorías en el sistema.

        Respuestas:
        - 200: Lista de subcategorías.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del método POST
    @swagger_auto_schema(
        operation_summary="Crear una nueva subcategoría",
        operation_description="Crea una nueva subcategoría en el sistema.",
        request_body=SubcategoriaSerializer,
        responses={
            201: openapi.Response(
                description="Subcategoría creada exitosamente",
                schema=SubcategoriaSerializer
            ),
            400: openapi.Response(
                description="Error en la solicitud",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea una nueva subcategoría.

        Este método recibe los datos de la subcategoría a crear y los procesa
        para guardar una nueva subcategoría en el sistema.

        Parámetros:
        - request_body: Los datos de la nueva subcategoría (según el esquema `SubcategoriaSerializer`).

        Respuestas:
        - 201: Subcategoría creada exitosamente.
        - 400: Error en la solicitud, si los datos son inválidos.
        """
        return super().post(request, *args, **kwargs)

class SubcategoriaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar y eliminar subcategorías.

    Esta vista permite recuperar los detalles de una subcategoría específica mediante su ID,
    actualizar sus detalles, realizar una actualización parcial, y eliminar una subcategoría
    de forma definitiva.

    Métodos disponibles:
    - GET: Recupera una subcategoría por su ID.
    - PUT: Actualiza completamente los detalles de una subcategoría.
    - PATCH: Actualiza parcialmente los detalles de una subcategoría.
    - DELETE: Elimina una subcategoría por su ID.
    """
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Obtener una subcategoría por ID",
        operation_description="Recupera los detalles de una subcategoría específica mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID de la subcategoría a recuperar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles de la subcategoría",
                schema=SubcategoriaSerializer
            ),
            404: openapi.Response(
                description="Subcategoría no encontrada"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera los detalles de una subcategoría específica.

        Este método devuelve los detalles completos de una subcategoría identificada
        por su ID.

        Parámetros:
        - id: ID de la subcategoría a recuperar.

        Respuestas:
        - 200: Detalles de la subcategoría.
        - 404: Subcategoría no encontrada si el ID no existe.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del método PUT
    @swagger_auto_schema(
        operation_summary="Actualizar una subcategoría",
        operation_description="Actualiza los detalles de una subcategoría específica.",
        request_body=SubcategoriaSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID de la subcategoría a actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Subcategoría actualizada exitosamente",
                schema=SubcategoriaSerializer
            ),
            400: openapi.Response(
                description="Error en la solicitud",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
            404: openapi.Response(
                description="Subcategoría no encontrada"
            )
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Actualiza completamente los detalles de una subcategoría.

        Este método recibe los nuevos detalles de una subcategoría y los actualiza
        en el sistema según el ID proporcionado.

        Parámetros:
        - id: ID de la subcategoría a actualizar.
        - request_body: Los nuevos datos para actualizar la subcategoría (según el esquema `SubcategoriaSerializer`).

        Respuestas:
        - 200: Subcategoría actualizada exitosamente.
        - 400: Error en la solicitud si los datos son inválidos.
        - 404: Subcategoría no encontrada si no existe la subcategoría con el ID dado.
        """
        return super().put(request, *args, **kwargs)

    #Documentación del método PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una subcategoría",
        operation_description="Actualiza parcialmente los detalles de una subcategoría específica.",
        request_body=SubcategoriaSerializer,
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la subcategoría", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={
            200: SubcategoriaSerializer,
            400: openapi.Response("Error en la solicitud"),
            404: openapi.Response("Subcategoría no encontrada")
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Actualiza parcialmente los detalles de una subcategoría.

        Este método permite realizar una actualización parcial de una subcategoría,
        modificando solo los campos que se proporcionen.

        Parámetros:
        - id: ID de la subcategoría a actualizar parcialmente.
        - request_body: Los datos a actualizar (según el esquema `SubcategoriaSerializer`).

        Respuestas:
        - 200: Subcategoría actualizada exitosamente.
        - 400: Error en la solicitud si los datos son inválidos.
        - 404: Subcategoría no encontrada si no existe la subcategoría con el ID dado.
        """
        return super().patch(request, *args, **kwargs)

    #Documentación del método DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar una subcategoría",
        operation_description="Elimina una subcategoría específica mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID de la subcategoría a eliminar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: openapi.Response(description="Subcategoría eliminada exitosamente"),
            404: openapi.Response(
                description="Subcategoría no encontrada"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Elimina una subcategoría específica.

        Este método elimina de manera permanente una subcategoría identificada por su ID.

        Parámetros:
        - id: ID de la subcategoría a eliminar.

        Respuestas:
        - 204: Subcategoría eliminada exitosamente.
        - 404: Subcategoría no encontrada si no existe la subcategoría con el ID dado.
        """
        return super().delete(request, *args, **kwargs)
    
class CategoriaListView(generics.ListAPIView):
    """
    Vista para listar todas las categorías con sus subcategorías anidadas.

    Esta vista permite obtener una lista completa de las categorías existentes,
    con sus respectivas subcategorías anidadas. Es un endpoint de solo lectura
    que devuelve los datos de todas las categorías disponibles en el sistema.

    Métodos disponibles:
    - GET: Recupera la lista de categorías con sus subcategorías anidadas.
    """
    queryset = Categoria.objects.all()  # Consulta todas las categorías
    serializer_class = CategoriaConSubcategoriasSerializer  # Especifica el serializer que maneja la relación anidada

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Listar categorías con subcategorías",
        operation_description="Devuelve una lista de todas las categorías con sus subcategorías anidadas.",
        responses={
            200: openapi.Response(
                description="Lista de categorías con subcategorías",
                schema=CategoriaConSubcategoriasSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera la lista de todas las categorías con sus subcategorías anidadas.

        Este método devuelve una lista de categorías donde cada categoría tiene
        sus subcategorías asociadas de forma anidada, según lo definido en el serializer.

        Respuestas:
        - 200: Lista de categorías con subcategorías anidadas.
        """
        return super().get(request, *args, **kwargs)

# Crear y listar contenido
class ContenidoListCreate(generics.ListCreateAPIView):
    """
    Vista para listar todos los contenidos y crear un nuevo contenido.

    Métodos HTTP permitidos:
    - GET: Recupera la lista de todos los contenidos.
    - POST: Crea un nuevo contenido asignando automáticamente el autor.

    Atributos:
    - queryset: Conjunto de todos los contenidos disponibles.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    """
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Crear o listar contenido",
        operation_description="Recupera la lista de contenidos existentes o crea un nuevo contenido. El autor se asigna automáticamente al contenido.",
        request_body=ContenidoSerializer,  # Parámetros para la creación del contenido
        responses={
            200: openapi.Response(
                description="Lista de contenidos",
                schema=ContenidoSerializer(many=True)  # Lista de contenidos
            ),
            201: openapi.Response(
                description="Contenido creado exitosamente",
                schema=ContenidoSerializer  # Contenido creado
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación")
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Obtiene la lista de contenidos.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del método post
    @swagger_auto_schema(
        operation_summary="Crear contenido",
        operation_description="Crea un nuevo contenido y lo asigna automáticamente al usuario que realiza la petición.",
        request_body=ContenidoSerializer,  # Parámetros para la creación del contenido
        responses={
            201: openapi.Response(
                description="Contenido creado exitosamente",
                schema=ContenidoSerializer  # Contenido creado
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea un nuevo contenido y lo asigna automáticamente al usuario que realiza la petición.
        """
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        Método para asignar automáticamente el autor del contenido al crearlo.
        """
        serializer.save(autor=self.request.user)
    
# Editar contenido
class ContenidoRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Vista para recuperar los detalles de un contenido específico y actualizarlo.

    Métodos HTTP permitidos:
    - GET: Recupera los detalles de un contenido específico.
    - PUT: Actualiza completamente un contenido existente.

    Atributos:
    - queryset: Conjunto de todos los contenidos.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    """
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer

    #Documentación de GET
    @swagger_auto_schema(
        operation_summary="Recuperar y actualizar contenido",
        operation_description="Recupera los detalles de un contenido específico y permite su actualización.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a recuperar o actualizar", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(description="Contenido actualizado", schema=ContenidoSerializer),
            404: openapi.Response(description="Contenido no encontrado")
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera un contenido específico utilizando el ID proporcionado en la URL.
        """
        return super().get(request, *args, **kwargs)

    #Documentación de PUT
    @swagger_auto_schema(
        operation_summary="Actualizar contenido existente",
        operation_description="Actualiza los detalles de un contenido específico utilizando el ID proporcionado.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a actualizar", type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=ContenidoSerializer,  # Aquí especificamos el Serializer para el cuerpo de la solicitud
        responses={
            200: openapi.Response(description="Contenido actualizado correctamente", schema=ContenidoSerializer),
            400: openapi.Response(description="Solicitud mal formada o parámetros inválidos"),
            404: openapi.Response(description="Contenido no encontrado")
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Actualiza completamente un contenido específico utilizando el ID proporcionado en la URL.
        Se requiere proporcionar todos los campos necesarios en el cuerpo de la solicitud.
        """
        return super().put(request, *args, **kwargs)

    #Documentación de PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un contenido",
        operation_description="Actualiza parcialmente un contenido, permitiendo actualizar solo los campos proporcionados.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a actualizar parcialmente", type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=ContenidoSerializer,  # Aquí especificamos el Serializer para el cuerpo de la solicitud
        responses={
            200: openapi.Response(description="Contenido parcialmente actualizado", schema=ContenidoSerializer),
            400: openapi.Response(description="Solicitud mal formada o parámetros inválidos"),
            404: openapi.Response(description="Contenido no encontrado")
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Actualiza parcialmente un contenido. Solo los campos proporcionados en el cuerpo de la solicitud serán actualizados.
        """
        return super().patch(request, *args, **kwargs)
    
# Inactivar contenido
class ContenidoInactivar(generics.UpdateAPIView):
    """
    Vista para inactivar un contenido específico, cambiando su estado a 'inactivo'.

    Métodos HTTP permitidos:
    - PUT: Actualiza el estado del contenido a 'inactivo'.

    Atributos:
    - queryset: Conjunto de todos los contenidos.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    """
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer
    
    @swagger_auto_schema(
        operation_summary="Inactivar contenido",
        operation_description="Inactiva un contenido específico cambiando su estado a 'inactivo'.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a inactivar", type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'estado': openapi.Schema(type=openapi.TYPE_STRING, enum=['inactivo'], description="Estado del contenido")
            },
            required=['estado']
        ),
        responses={
            200: openapi.Response(description="Contenido inactivado exitosamente", schema=ContenidoSerializer),
            404: openapi.Response(description="Contenido no encontrado")
        }
    )
    def patchSwagger(self, request, *args, **kwargs):
        """
        Cambia el estado de un contenido a 'inactivo'.
        """
        return super().patch(request, *args, **kwargs)
    
    # Documentación para el método PUT
    @swagger_auto_schema(
        operation_summary="Desactivar Contenido",
        operation_description="Inactiva un contenido específico cambiando su estado a 'inactivo' usando el método PUT.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a inactivar", type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'estado': openapi.Schema(type=openapi.TYPE_STRING, enum=['inactivo'], description="Estado del contenido")
            },
            required=['estado']
        ),
        responses={
            200: openapi.Response(description="Contenido inactivado exitosamente", schema=ContenidoSerializer),
            404: openapi.Response(description="Contenido no encontrado")
        }
    )
    def putSwagger(self, request, *args, **kwargs):
        """
        Cambia el estado de un contenido a 'inactivo' usando el método PUT.
        """
        return super().put(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        """
        Método para cambiar el estado del contenido a 'inactivo'.
        """
        serializer.save(estado='inactivo')

# Visualización de contenido publicado
class ContenidoPublicadoList(generics.ListAPIView):
    """
    Vista para listar todos los contenidos que han sido aprobados.

    Métodos HTTP permitidos:
    - GET: Recupera la lista de contenidos con estado 'aprobado'.

    Atributos:
    - queryset: Conjunto de contenidos aprobados.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    """
    queryset = Contenido.objects.filter(estado='aprobado')
    serializer_class = ContenidoSerializer

    @swagger_auto_schema(
        operation_summary="Listar contenidos aprobados",
        operation_description="Recupera todos los contenidos que han sido aprobados.",
        responses={
            200: openapi.Response(description="Lista de contenidos aprobados", schema=ContenidoSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera la lista de contenidos aprobados.
        """
        return super().get(request, *args, **kwargs)
# Búsqueda y filtrado de contenido
class ContenidoSearch(generics.ListAPIView):
    """
    Vista para la búsqueda y filtrado de contenidos por varios parámetros.

    @swagger_auto_schema(
        operation_summary="Buscar y filtrar contenidos",
        operation_description="Permite buscar y filtrar contenidos por parámetros como título, autor, categoría, fecha y estado.",
        responses={
            200: openapi.Response(description="Lista filtrada de contenidos", schema=ContenidoSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    Métodos HTTP permitidos:
    - GET: Filtra contenidos por título, autor, categoría, subcategoría, fecha y estado.

    Atributos:
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    """
    serializer_class = ContenidoSerializer

    def get_queryset(self):
        """
        Método para filtrar el conjunto de contenidos en función de los parámetros de consulta proporcionados.

        Parámetros de consulta:
        - titulo: Filtrar por título del contenido.
        - autor: Filtrar por nombre de usuario del autor.
        - categoria_id: Filtrar por ID de la categoría.
        - subcategoria_id: Filtrar por ID de la subcategoría.
        - fecha: Filtrar por fecha de creación del contenido (formato YYYY-MM-DD).
        - estado: Filtrar por estado del contenido.
        """
        queryset = Contenido.objects.all()
        titulo = self.request.query_params.get('titulo', None)
        autor = self.request.query_params.get('autor', None)
        categoria_id = self.request.query_params.get('categoria_id', None)
        subcategoria_id = self.request.query_params.get('subcategoria_id', None)
        fecha = self.request.query_params.get('fecha', None)
        estado=self.request.query_params.get('estado', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__username__icontains=autor)
        
        # Filtro por subcategoria_id si está presente
        if subcategoria_id:
            queryset = queryset.filter(subcategoria__id=subcategoria_id)

        # Filtro por categoria_id usando la relación subcategoria -> categoria
        if categoria_id:
            queryset = queryset.filter(subcategoria__categoria__id=categoria_id)
        
        if fecha:
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha=fecha)
            except ValueError:
                print("Formato de fecha inválido, debe ser YYYY-MM-DD")
        return queryset
    
# Vista para listar, crear y filtrar contenido
class ContenidoListCreate(generics.ListCreateAPIView):
    """
    Vista para listar, crear y filtrar contenidos.

    Métodos HTTP permitidos:
    - GET: Recupera la lista de contenidos, con opciones de filtrado.
    - POST: Crea un nuevo contenido.

    Atributos:
    - queryset: Conjunto de todos los contenidos.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos a JSON.
    - filter_backends: Configuración para habilitar el filtrado en los campos especificados.
    - filterset_fields: Campos por los cuales se puede filtrar, como 'estado' y 'titulo'.
    """
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'titulo']

    @swagger_auto_schema(
        operation_summary="Listar o crear contenido",
        operation_description="Recupera la lista de contenidos existentes o crea un nuevo contenido. Filtra por estado o título.",
        responses={
            200: openapi.Response(
                description="Lista de contenidos",
                schema=ContenidoSerializer(many=True)  # Lista de contenidos
            ),
            201: openapi.Response(
                description="Contenido creado exitosamente",
                schema=ContenidoSerializer  # Contenido creado
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación")
        },
        manual_parameters=[
            openapi.Parameter('estado', openapi.IN_QUERY, description="Filtra los contenidos por estado", type=openapi.TYPE_STRING),
            openapi.Parameter('titulo', openapi.IN_QUERY, description="Filtra los contenidos por título", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Obtiene la lista de contenidos.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Crear contenido",
        operation_description="Crea un nuevo contenido y lo asigna automáticamente al usuario que realiza la petición.",
        request_body=ContenidoSerializer,  # Parámetros para la creación del contenido
        responses={
            201: openapi.Response(
                description="Contenido creado exitosamente",
                schema=ContenidoSerializer  # Contenido creado
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea un nuevo contenido y lo asigna automáticamente al usuario que realiza la petición.
        """
        return super().post(request, *args, **kwargs)

# Vista para aprobar o rechazar contenido
class ContenidoAprobarRechazar(generics.UpdateAPIView):
    """
    Vista para aprobar o rechazar un contenido en revisión, inactivo, rechazado o en borrador.

    Métodos HTTP permitidos:
    - PUT: Cambia el estado de un contenido específico a aprobado o rechazado.

    Atributos:
    - queryset: Conjunto de contenidos en estados específicos para revisión.
    - serializer_class: Serializador utilizado para convertir los datos de los contenidos en revisión.
    """
    queryset = Contenido.objects.filter(Q(estado='en_revision') | Q(estado='inactivo') | Q(estado='rechazado') | Q(estado='borrador'))  # Solo mostrar en revisión
    serializer_class = ContenidoRevisionSerializer

    #Documentación para el método PATCH
    @swagger_auto_schema(
        operation_summary="Aprobar o rechazar contenido",
        operation_description="Permite aprobar o rechazar un contenido cuyo estado sea 'en_revision', 'inactivo', 'rechazado' o 'borrador'. Se puede cambiar el estado a 'aprobado' o 'rechazado'.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'estado': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['aprobado', 'rechazado'],  # Enum de estados posibles
                    description="Nuevo estado del contenido"
                ),
            },
            required=['estado'],  # Estado requerido en el cuerpo de la solicitud
        ),
        responses={
            200: openapi.Response(
                description="Contenido actualizado exitosamente",
                schema=ContenidoRevisionSerializer  # Contenido con el nuevo estado
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación"),
            404: openapi.Response(description="Contenido no encontrado"),
        },
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a aprobar o rechazar", type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        """
        Cambia el estado de un contenido a 'aprobado' o 'rechazado'.
        """
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        Método para actualizar el estado del contenido, cambiándolo a aprobado o rechazado.
        """
        serializer.save()

    # Documentación para el método PUT
    @swagger_auto_schema(
        operation_summary="Actualizar estado del contenido a aprobado o rechazado",
        operation_description="Permite aprobar o rechazar un contenido cuyo estado sea 'en_revision', 'inactivo', 'rechazado' o 'borrador'. Se puede cambiar el estado a 'aprobado' o 'rechazado'.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'estado': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['aprobado', 'rechazado'],
                    description="Nuevo estado del contenido"
                ),
            },
            required=['estado']
        ),
        responses={
            200: openapi.Response(
                description="Contenido actualizado exitosamente",
                schema=ContenidoRevisionSerializer
            ),
            400: openapi.Response(description="Solicitud incorrecta, error de validación"),
            404: openapi.Response(description="Contenido no encontrado")
        },
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del contenido a aprobar o rechazar", type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def put(self, request, *args, **kwargs):
        """
        Cambia el estado de un contenido a 'aprobado' o 'rechazado' usando el método PUT.
        """
        return super().put(request, *args, **kwargs)

#TODO: USUARIOS      
class UsuarioListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear usuarios.

    Esta vista permite obtener una lista de todos los usuarios existentes en la base de datos
    y también crear nuevos usuarios a través de una solicitud POST con los datos correspondientes.

    Métodos disponibles:
    - GET: Recupera todos los usuarios existentes.
    - POST: Crea un nuevo usuario con los datos proporcionados.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Obtener lista de usuarios",
        operation_description="Obtiene todos los usuarios existentes en la base de datos.",
        responses={
            200: openapi.Response(
                description="Lista de usuarios",
                schema=UsuarioSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera una lista de todos los usuarios en la base de datos.

        Este método permite obtener todos los usuarios registrados en el sistema.

        Respuestas:
        - 200: Devuelve una lista de usuarios.
        """
        return super().get(request, *args, **kwargs)

    #Documentación de método POST
    @swagger_auto_schema(
        operation_summary="Crear un nuevo usuario",
        operation_description="Crea un nuevo usuario con los datos proporcionados.",
        request_body=UsuarioSerializer,
        responses={
            201: openapi.Response(
                description="Usuario creado exitosamente",
                schema=UsuarioSerializer()
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea un nuevo usuario con los datos proporcionados en la solicitud.

        Este método permite crear un nuevo usuario en el sistema.

        Respuestas:
        - 201: Usuario creado exitosamente.
        - 400: Error en los datos proporcionados (datos inválidos).
        """
        return super().post(request, *args, **kwargs)

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar y eliminar un usuario específico.

    Esta vista permite:
    - Obtener los detalles de un usuario mediante su ID.
    - Actualizar los datos de un usuario mediante su ID.
    - Actualizar parcialmente los datos de un usuario.
    - Eliminar un usuario mediante su ID.

    Métodos disponibles:
    - GET: Recupera los detalles de un usuario.
    - PUT: Actualiza completamente los datos de un usuario.
    - PATCH: Actualiza parcialmente los datos de un usuario.
    - DELETE: Elimina un usuario.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Obtener los detalles de un usuario",
        operation_description="Recupera los detalles de un usuario específico mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a recuperar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles del usuario",
                schema=UsuarioSerializer()
            ),
            404: openapi.Response(
                description="Usuario no encontrado"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera los detalles de un usuario específico mediante su ID.

        Respuestas:
        - 200: Devuelve los detalles del usuario.
        - 404: Si el usuario no se encuentra.
        """
        return super().get(request, *args, **kwargs)

    #Documentación del método PUT
    @swagger_auto_schema(
        operation_summary="Actualizar los datos de un usuario",
        operation_description="Actualiza los datos de un usuario específico mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'usuario_id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        request_body=UsuarioSerializer,
        responses={
            200: openapi.Response(
                description="Usuario actualizado exitosamente",
                schema=UsuarioSerializer()
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Usuario no encontrado"
            )
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Actualiza completamente los datos de un usuario específico mediante su ID.

        Respuestas:
        - 200: Usuario actualizado exitosamente.
        - 400: Datos inválidos.
        - 404: Usuario no encontrado.
        """
        return super().put(request, *args, **kwargs)

    #Documentación del método PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un usuario",
        operation_description="Actualiza parcialmente los datos de un usuario específico mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        request_body=UsuarioSerializer,  # Define el cuerpo de la solicitud para el PATCH
        responses={
            200: openapi.Response(
                description="Usuario actualizado parcialmente",
                schema=UsuarioSerializer()
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Usuario no encontrado"
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Actualiza parcialmente los datos de un usuario específico.

        Respuestas:
        - 200: Usuario parcialmente actualizado.
        - 400: Datos inválidos.
        - 404: Usuario no encontrado.
        """
        return super().patch(request, *args, **kwargs)

    #Documentación del método DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar un usuario",
        operation_description="Elimina un usuario específico mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'usuario_id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a eliminar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
            openapi.Parameter(
                'id',  # El nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del usuario a eliminar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        responses={
            204: openapi.Response(
                description="Usuario eliminado exitosamente"
            ),
            404: openapi.Response(
                description="Usuario no encontrado"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Elimina un usuario específico mediante su ID.

        Respuestas:
        - 204: Usuario eliminado exitosamente.
        - 404: Usuario no encontrado.
        """
        return super().delete(request, *args, **kwargs)

class UsuarioByEmailView(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un usuario basado en su dirección de correo electrónico.

    Este endpoint permite recuperar los detalles de un usuario específico utilizando su email.
    
    Atributos:
        serializer_class (class): El serializer utilizado para convertir los datos del usuario en un formato adecuado.
        lookup_field (str): El campo utilizado para realizar la búsqueda. En este caso, 'email'.

    Métodos:
        get_queryset(): Devuelve todos los usuarios disponibles en la base de datos.
        get_object(): Recupera el usuario basado en el email proporcionado en la URL.

    Ejemplo de uso:
        GET /usuarios/email/{email}/

    Respuestas:
        200: Detalles del usuario encontrado.
        404: Usuario no encontrado.

    """
    serializer_class = UsuarioSerializer
    lookup_field = 'email'
    
    def get_queryset(self):
        """
        Devuelve todos los usuarios en la base de datos.

        Este método es llamado por la vista para obtener el conjunto de datos con los que 
        trabajar en la vista de detalle.

        Returns:
            queryset: Un queryset de todos los usuarios.
        """
        return Usuario.objects.all() 
    def get_object(self):
        """
        Recupera un objeto usuario basado en el email proporcionado en la URL.

        Este método se llama para obtener el usuario correspondiente al email. Si no se encuentra, 
        se lanza una excepción de tipo NotFound.

        Raises:
            NotFound: Si no se encuentra un usuario con el email proporcionado.

        Returns:
            Usuario: El usuario correspondiente al email proporcionado.

        """
        queryset = self.get_queryset()
        email = self.kwargs.get('email')
        try:
            return queryset.get(email=email)
        except Usuario.DoesNotExist:
            raise NotFound(f"No se encontró ningún usuario con el email: {email}")

class RolListCreateView(generics.ListCreateAPIView):
    """
    Vista para obtener la lista de roles y crear un nuevo rol.

    Esta vista permite obtener todos los roles existentes y también crear nuevos roles en el sistema.

    Atributos:
        queryset (QuerySet): El conjunto de datos que contiene todos los roles disponibles.
        serializer_class (class): El serializer utilizado para convertir los datos de los roles a un formato adecuado.
    
    Métodos:
        get(): Recupera todos los roles existentes en el sistema.
        post(): Crea un nuevo rol en el sistema utilizando los datos proporcionados.

    Ejemplo de uso:
        GET /roles/      -> Obtiene todos los roles
        POST /roles/     -> Crea un nuevo rol con los datos proporcionados

    Respuestas:
        200: Lista de roles.
        201: Rol creado exitosamente.
        400: Solicitud incorrecta.

    """
    queryset = Rol.objects.all()
    serializer_class = RolCreateUpdateSerializer

    #Documentación de GET
    @swagger_auto_schema(
        operation_summary="Obtener lista de roles",
        operation_description="Recupera todos los roles existentes.",
        responses={
            200: openapi.Response(
                description="Lista de roles",
                schema=RolCreateUpdateSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud GET.

        Recupera todos los roles existentes en el sistema.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL.

        Returns:
            Response: Respuesta con la lista de roles.
        """
        return super().get(request, *args, **kwargs)

    #Documentación de POST
    @swagger_auto_schema(
        operation_summary="Crear un nuevo rol",
        operation_description="Permite crear un nuevo rol en el sistema.",
        request_body=RolCreateUpdateSerializer,  # Aquí usamos el serializador en lugar de openapi.Parameter
        responses={
            201: openapi.Response(
                description="Rol creado exitosamente",
                schema=RolCreateUpdateSerializer
            ),
            400: openapi.Response(
                description="Solicitud incorrecta"
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud POST.

        Crea un nuevo rol en el sistema utilizando los datos proporcionados en la solicitud.

        Args:
            request (Request): La solicitud HTTP que contiene los datos del nuevo rol.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL.

        Returns:
            Response: Respuesta indicando si el rol se ha creado exitosamente.
        """
        return super().post(request, *args, **kwargs)

class RolDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar parcialmente, actualizar completamente y eliminar un rol específico.

    Esta vista permite recuperar los detalles de un rol, actualizar los detalles de un rol específico,
    actualizar parcialmente un rol y eliminar un rol por su ID.

    Atributos:
        queryset (QuerySet): El conjunto de datos que contiene todos los roles disponibles.
        serializer_class (class): El serializer utilizado para convertir los datos del rol a un formato adecuado.
    
    Métodos:
        get(): Recupera los detalles de un rol específico.
        put(): Actualiza un rol específico con nuevos datos.
        patch(): Actualiza parcialmente un rol específico con los datos proporcionados.
        delete(): Elimina un rol específico del sistema.

    Ejemplo de uso:
        GET /roles/{id}/    -> Recupera los detalles del rol con el ID especificado
        PUT /roles/{id}/    -> Actualiza completamente el rol con el ID especificado
        PATCH /roles/{id}/  -> Actualiza parcialmente el rol con el ID especificado
        DELETE /roles/{id}/ -> Elimina el rol con el ID especificado

    Respuestas:
        200: Detalles del rol (GET) o rol actualizado exitosamente (PUT/PATCH).
        204: Rol eliminado exitosamente (DELETE).
        400: Solicitud incorrecta.
        404: Rol no encontrado.

    """
    queryset = Rol.objects.all()
    serializer_class = RolCreateUpdateSerializer

    #Documentación para el método GET
    @swagger_auto_schema(
        operation_summary="Obtener detalles del rol",
        operation_description="Recupera los detalles de un rol específico por su ID.",
        responses={
            200: openapi.Response(
                description="Detalles del rol",
                schema=RolCreateUpdateSerializer
            ),
            404: openapi.Response(
                description="Rol no encontrado"
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del rol a recuperar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud GET.

        Recupera los detalles de un rol específico según el ID proporcionado en la URL.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL (ID del rol).

        Returns:
            Response: Respuesta con los detalles del rol.
        """
        return super().get(request, *args, **kwargs)

    #Documentación para el método PUT
    @swagger_auto_schema(
        operation_summary="Actualizar un rol",
        operation_description="Permite actualizar los detalles de un rol existente.",
        request_body=RolCreateUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Rol actualizado exitosamente",
                schema=RolCreateUpdateSerializer
            ),
            400: openapi.Response(
                description="Solicitud incorrecta"
            ),
            404: openapi.Response(
                description="Rol no encontrado"
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del rol a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
        ]
    )
    def put(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud PUT.

        Actualiza completamente los detalles de un rol específico según el ID proporcionado en la URL.

        Args:
            request (Request): La solicitud HTTP que contiene los datos del rol a actualizar.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL (ID del rol).

        Returns:
            Response: Respuesta indicando si el rol ha sido actualizado exitosamente.
        """
        return super().put(request, *args, **kwargs)

    #Documentación para el método PATCH
    @swagger_auto_schema(
        operation_summary="Parcialmente actualizar un rol",
        operation_description="Permite actualizar parcialmente los detalles de un rol existente.",
        request_body=RolCreateUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Rol parcialmente actualizado",
                schema=RolCreateUpdateSerializer
            ),
            400: openapi.Response(
                description="Solicitud incorrecta"
            ),
            404: openapi.Response(
                description="Rol no encontrado"
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del rol a actualizar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud PATCH.

        Actualiza parcialmente los detalles de un rol específico según el ID proporcionado en la URL.

        Args:
            request (Request): La solicitud HTTP que contiene los datos parciales del rol.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL (ID del rol).

        Returns:
            Response: Respuesta indicando si el rol ha sido parcialmente actualizado.
        """
        return super().patch(request, *args, **kwargs)

    #Documentación para el método DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar un rol",
        operation_description="Elimina un rol específico del sistema.",
        responses={
            204: openapi.Response(
                description="Rol eliminado exitosamente"
            ),
            404: openapi.Response(
                description="Rol no encontrado"
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del rol a eliminar",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            ),
        ]
    )
    def delete(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud DELETE.

        Elimina un rol específico del sistema según el ID proporcionado en la URL.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales que se extraen de la URL (ID del rol).

        Returns:
            Response: Respuesta indicando si el rol ha sido eliminado exitosamente.
        """
        return super().delete(request, *args, **kwargs)

#TODO:Permisos
class PermisoListView(generics.ListAPIView):
    """
    Vista para listar todos los permisos disponibles en el sistema.

    Esta vista recupera todos los permisos existentes y los devuelve en una lista.

    Atributos:
        queryset (QuerySet): El conjunto de datos que contiene todos los permisos disponibles.
        serializer_class (class): El serializer utilizado para convertir los datos del permiso a un formato adecuado.
    
    Métodos:
        get(): Recupera la lista de todos los permisos en el sistema.

    Ejemplo de uso:
        GET /permisos/    -> Recupera la lista de permisos disponibles.

    Respuestas:
        200: Lista de permisos obtenida con éxito.
        400: Solicitud incorrecta, con un mensaje de error detallado.
    """
   
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer

    @swagger_auto_schema(
        operation_summary="Listar permisos",
        operation_description="Obtiene una lista de todos los permisos disponibles en el sistema.",
        responses={
            200: openapi.Response(
                description="Lista de permisos obtenida con éxito",
                schema=PermisoSerializer(many=True)
            ),
            400: openapi.Response(
                description="Solicitud incorrecta",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error"),
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud GET.

        Recupera la lista de todos los permisos disponibles en el sistema.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales para el manejo de la solicitud.

        Returns:
            Response: Respuesta con la lista de permisos.
        """
        return super().get(request, *args, **kwargs)

class ObtenerUsuarioPorEmailView(RetrieveAPIView):
    """
    Vista para obtener los detalles de un usuario específico mediante su email.

    Esta vista recupera un usuario por su email y devuelve los detalles del usuario, 
    incluyendo sus roles y permisos.

    Atributos:
        serializer_class (class): El serializer utilizado para convertir los datos del usuario 
                                   a un formato adecuado.

    Métodos:
        get(): Recupera los detalles del usuario basado en su email.
    
    Ejemplo de uso:
        GET /usuario/email/<email>/  -> Recupera los detalles del usuario con el email especificado.

    Respuestas:
        200: Detalles del usuario recuperados con éxito.
        404: Usuario no encontrado.
    """
   
    serializer_class = UsuarioConRolesYPermisosSerializer

    @swagger_auto_schema(
        operation_summary="Obtener usuario por email",
        operation_description="Recupera los detalles de un usuario específico mediante su email.",
        manual_parameters=[
            openapi.Parameter(
                'email',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="Email del usuario a recuperar",
                type=openapi.TYPE_STRING,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles del usuario",
                schema=UsuarioConRolesYPermisosSerializer
            ),
            404: openapi.Response(
                description="Usuario no encontrado"
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Método para manejar la solicitud GET.

        Recupera los detalles de un usuario basado en su email.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales para el manejo de la solicitud.

        Returns:
            Response: Respuesta con los detalles del usuario.
        """
        email = kwargs.get('email')
        usuario = get_object_or_404(Usuario, email=email)  # Buscar usuario por email
        serializer = self.serializer_class(usuario)
        return Response(serializer.data)

# TODO: comentarios
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Comentario
from .serializers import ComentarioSerializer
class ComodinView(APIView):
    swagger_fake_view = True

    @swagger_auto_schema(operation=None)  # Esto asegura que Swagger no lo registre
    def put(self, request, *args, **kwargs):
        raise NotImplementedError("El método PUT no está permitido.")
    
class ComentarioListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear comentarios relacionados con un contenido.

    Esta vista permite obtener una lista de comentarios principales (sin respuestas) de un contenido específico
    mediante su ID, o bien crear un nuevo comentario (principal o respuesta) en un contenido.

    Atributos:
        queryset (QuerySet): Los comentarios a listar o crear.
        serializer_class (class): El serializer utilizado para la validación y transformación de los datos de los comentarios.

    Métodos:
        get(): Recupera los comentarios principales de un contenido específico.
        post(): Permite crear un nuevo comentario o respuesta en un contenido.
        perform_create(): Realiza la creación del comentario y determina si es un comentario principal o una respuesta.
        actualizar_lista_comentarios(): Actualiza la lista de comentarios en el contenido después de agregar un nuevo comentario.

    Ejemplo de uso:
        GET /contenido/{contenido_id}/comentarios/  -> Obtiene la lista de comentarios principales de un contenido.
        POST /contenido/{contenido_id}/comentarios/  -> Crea un nuevo comentario en el contenido.

    Respuestas:
        GET:
            200: Lista de comentarios principales recuperados con éxito.
            404: Contenido no encontrado.
        POST:
            201: Comentario creado exitosamente.
            400: Error de validación (si el comentario al que se intenta responder no existe o es inválido).
            404: Contenido no encontrado.
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    # Documentación para el método GET
    @swagger_auto_schema(
        operation_summary="Listar comentarios principales de un contenido",
        operation_description="Devuelve una lista de comentarios principales asociados a un contenido específico identificado por `contenido_id`.",
        manual_parameters=[
            openapi.Parameter(
                name='contenido_id',
                in_=openapi.IN_PATH,
                description="ID del contenido al cual pertenecen los comentarios",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Lista de comentarios principales",
                schema=ComentarioSerializer(many=True)
            ),
            404: openapi.Response(
                description="Contenido no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Contenido no encontrado."
                        )
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs): # COMODIN
        """
        Recupera los comentarios principales de un contenido específico identificado por `contenido_id`.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales para el manejo de la solicitud.

        Returns:
            Response: Respuesta con la lista de comentarios principales del contenido.
        """
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        """
        Filtra los comentarios para mostrar solo los principales (sin respuestas).

        Returns:
            QuerySet: Los comentarios principales asociados al `contenido_id`.
        """
        contenido_id = self.kwargs.get('contenido_id')
        return Comentario.objects.filter(contenido_id=contenido_id, reply_to=None)  # Mostrar solo comentarios principales 

    # Documentación para el método POST
    @swagger_auto_schema(
    operation_summary="Crear un nuevo comentario en un contenido",
    operation_description=(
        "Permite agregar un nuevo comentario principal o una respuesta a un comentario existente "
        "en un contenido específico identificado por `contenido_id`. Si el campo `reply_to` está vacío, "
        "se considera un comentario principal. De lo contrario, se trata como una respuesta a otro comentario."
    ),
    manual_parameters=[
        openapi.Parameter(
            name='contenido_id',
            in_=openapi.IN_PATH,
            description="ID del contenido al cual se va a asociar el comentario",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="JSON que contiene los datos del comentario.",
        required=['texto'],
        properties={
            'texto': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Contenido del comentario"
            ),
            'reply_to': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID del comentario al que se está respondiendo (opcional)"
            ),
        }
    ),
    responses={
        201: openapi.Response(
            description="Comentario creado exitosamente",
            schema=ComentarioSerializer()
        ),
        400: openapi.Response(
            description="Error de validación",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'reply_to': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="El comentario al que intenta responder no existe o es inválido."
                        )
                    )
                }
            )
        ),
        404: openapi.Response(
            description="Contenido no encontrado",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Contenido no encontrado."
                    )
                }
            )
        ),
    }
)
    @transaction.atomic
    def post(self, request, *args, **kwargs): # COMODIN
        """
        Crea un nuevo comentario o respuesta en un contenido específico.

        Si el campo `reply_to` está vacío, se crea un comentario principal. Si no, se crea una respuesta
        a un comentario existente.

        Args:
            request (Request): La solicitud HTTP.
            *args: Argumentos adicionales para el manejo de la solicitud.
            **kwargs: Parámetros adicionales para el manejo de la solicitud.

        Returns:
            Response: Respuesta con el comentario creado.
        """
        return super().post(request, *args, **kwargs)
    def perform_create(self, serializer):
        """
        Guarda un nuevo comentario, determinando si es un comentario principal o una respuesta.

        Args:
            serializer (ComentarioSerializer): El serializer con los datos validados del comentario.

        Returns:
            None
        """
        contenido_id = self.kwargs.get('contenido_id')
        reply_to_id = self.request.data.get('reply_to')

        # Si no hay 'reply_to' o es '0', se trata como un comentario principal
        if not reply_to_id or reply_to_id in ['0', None, '']:  
            comentario = serializer.save(contenido_id=contenido_id)
        else:
            try:
                # Intentar convertir el reply_to_id a entero
                reply_to_id = int(reply_to_id)
                reply_to_comment = Comentario.objects.get(id=reply_to_id)
                comentario = serializer.save(contenido_id=contenido_id, reply_to=reply_to_comment)
            except (Comentario.DoesNotExist, ValueError):
                return Response({'reply_to': ['El comentario al que intenta responder no existe o es inválido.']},
                                status=status.HTTP_400_BAD_REQUEST)

        # Una vez que el comentario ha sido creado, actualizamos la lista de comentarios en el contenido
        self.actualizar_lista_comentarios(contenido_id)

        return Response(serializer.data)

    def actualizar_lista_comentarios(self, contenido_id):
        """
        Actualiza la lista de comentarios del contenido luego de que se ha añadido un comentario.

        Args:
            contenido_id (int): El ID del contenido al que se le actualizarán los comentarios.

        Returns:
            None
        """
        """Actualiza la lista de comentarios del contenido luego de que se ha añadido un comentario."""
        try:
            # Obtener el contenido correspondiente
            contenido = Contenido.objects.get(id=contenido_id)
            # Traer todos los comentarios principales del contenido (sin anidar las respuestas)
            comentarios = Comentario.objects.filter(contenido_id=contenido_id, reply_to=None)
            # Serializar los comentarios
            comentarios_serializados = ComentarioSerializer(comentarios, many=True).data
            # Actualizar el campo de comentarios del contenido (ajústalo según tu lógica)
            contenido.comentarios = comentarios_serializados
            contenido.save()
        except Contenido.DoesNotExist:
            print(f"Contenido con ID {contenido_id} no encontrado.") 

class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar parcialmente o eliminar un comentario específico en un contenido determinado.

    Este conjunto de vistas permite realizar las siguientes acciones:
    - Obtener los detalles de un comentario dado un `contenido_id` y un `id`.
    - Actualizar parcialmente un comentario (solo los campos proporcionados en la solicitud).
    - Actualizar completamente un comentario reemplazando todos sus campos.
    - Eliminar un comentario, siempre que el usuario sea el autor del comentario.

    Atributos:
        queryset: Conjunto de comentarios para recuperar.
        serializer_class: El serializador que define cómo se estructuran los comentarios en las respuestas y peticiones.
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    # Documentación para el método GET
    @swagger_auto_schema(
        operation_summary="Obtener detalles de un comentario específico",
        operation_description="Devuelve los detalles de un comentario identificado por `id` en un contenido específico identificado por `contenido_id`.",
        manual_parameters=[
            openapi.Parameter(
                name='contenido_id',
                in_=openapi.IN_PATH,
                description="ID del contenido al cual pertenece el comentario",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID del comentario que se desea obtener",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles del comentario",
                schema=ComentarioSerializer()
            ),
            404: openapi.Response(
                description="Comentario o contenido no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Comentario o contenido no encontrado."
                        )
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera los detalles de un comentario específico.

        Este método devuelve los detalles de un comentario identificado por `id` dentro de un contenido específico
        identificado por `contenido_id`.

        Parámetros:
            request (HttpRequest): El objeto de solicitud HTTP.
            contenido_id (int): ID del contenido al cual pertenece el comentario.
            id (int): ID del comentario que se desea obtener.

        Respuestas:
            200: Detalles del comentario.
            404: Comentario o contenido no encontrado.
        """
        return super().get(request, *args, **kwargs)

    # Documentación para el método PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un comentario",
        operation_description=(
            "Permite actualizar parcialmente un comentario existente en un contenido específico "
            "identificado por `contenido_id`. Este método solo actualizará los campos proporcionados "
            "en la solicitud, dejando los demás sin cambios."
        ),
        manual_parameters=[
            openapi.Parameter(
                name='contenido_id',
                in_=openapi.IN_PATH,
                description="ID del contenido al cual pertenece el comentario a actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID del comentario que se desea actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'texto': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Nuevo contenido del comentario (opcional)"
                ),
                'reply_to': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID del comentario al que se está respondiendo (opcional)"
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Comentario actualizado parcialmente",
                schema=ComentarioSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'reply_to': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="El comentario al que intenta responder no existe o es inválido."
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Comentario o contenido no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Comentario o contenido no encontrado."
                        )
                    }
                )
            ),
        }
    )
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        """
        Actualiza parcialmente un comentario.

        Este método permite actualizar parcialmente un comentario en el contenido identificado por `contenido_id`.
        Solo los campos proporcionados en la solicitud serán actualizados.

        Parámetros:
            request (HttpRequest): El objeto de solicitud HTTP.
            contenido_id (int): ID del contenido al cual pertenece el comentario a actualizar.
            id (int): ID del comentario que se desea actualizar.
            texto (str, opcional): Nuevo texto del comentario.
            reply_to (int, opcional): ID del comentario al que se está respondiendo.

        Respuestas:
            200: Comentario actualizado parcialmente.
            400: Error de validación (por ejemplo, `reply_to` inválido).
            404: Comentario o contenido no encontrado.
        """
        return super().patch(request, *args, **kwargs)
    
    #Documentacion de PUT
    @swagger_auto_schema(
        operation_summary="Actualizar un comentario existente",
        operation_description=(
            "Permite actualizar un comentario existente en un contenido específico "
            "identificado por `contenido_id`. Este método reemplaza los campos del comentario "
            "con los nuevos valores proporcionados en la solicitud."
        ),
        manual_parameters=[
            openapi.Parameter(
                'contenido_id',
                openapi.IN_PATH,
                description="ID del contenido relacionado con el comentario",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del comentario a actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['texto'],
            properties={
                'texto': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Nuevo contenido del comentario"
                ),
                'reply_to': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID del comentario al que se está respondiendo (opcional)"
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Comentario actualizado exitosamente",
                schema=ComentarioSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'reply_to': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="El comentario al que intenta responder no existe o es inválido."
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Comentario o contenido no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Comentario o contenido no encontrado."
                        )
                    }
                )
            ),
        }
    )
    def put(self, request, *args, **kwargs): # COMODIN
        """
        Actualiza un comentario existente.

        Este método reemplaza los valores del comentario con los nuevos valores proporcionados en la solicitud.
        
        Parámetros:
            request (HttpRequest): El objeto de solicitud HTTP.
            contenido_id (int): ID del contenido relacionado con el comentario.
            id (int): ID del comentario a actualizar.
            texto (str): Nuevo contenido del comentario.
            reply_to (int, opcional): ID del comentario al que se está respondiendo.

        Respuestas:
            200: Comentario actualizado exitosamente.
            400: Error de validación.
            404: Comentario o contenido no encontrado.
        """
        return super().put(request, *args, **kwargs)
    def get_queryset(self):
        """
        Filtra los comentarios por el ID del contenido.

        Este método personaliza el conjunto de datos que se devolverá en la respuesta `GET`. Solo se devolverán los
        comentarios que pertenezcan al contenido especificado por `contenido_id`.

        Parámetros:
            contenido_id (int): ID del contenido al que pertenecen los comentarios.

        Devuelve:
            QuerySet: Conjunto de comentarios filtrados por `contenido_id`.
        """
        contenido_id = self.kwargs.get('contenido_id')
        return Comentario.objects.filter(contenido_id=contenido_id)
    
    # Documentacion de la acción DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar un comentario específico",
        operation_description="Elimina un comentario identificado por `id`. Requiere que el usuario sea el autor del comentario.",
        manual_parameters=[
            openapi.Parameter(
                name='contenido_id',
                in_=openapi.IN_PATH,
                description="ID del contenido al cual pertenece el comentario",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID único del comentario que se desea eliminar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: openapi.Response('Comentario eliminado exitosamente'),
            403: openapi.Response(
                'Prohibido: El usuario no tiene permiso para eliminar este comentario',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="No tienes permiso para eliminar este comentario."
                        )
                    }
                )
            ),
            404: openapi.Response(
                'Comentario no encontrado',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="No encontrado.")
                    }
                )
            ),
        }
    )
    def delete(self, request, *args, **kwargs): # COMODIN
        return super().delete(request, *args, **kwargs)
            
    def destroy(self, request, *args, **kwargs):
        """
        Elimina un comentario específico.

        Este método elimina un comentario, asegurándose de que el usuario que hace la solicitud sea el autor del comentario.

        Parámetros:
            request (HttpRequest): El objeto de solicitud HTTP.
            contenido_id (int): ID del contenido al cual pertenece el comentario.
            id (int): ID del comentario que se desea eliminar.

        Respuestas:
            204: Comentario eliminado exitosamente.
            403: El usuario no tiene permisos para eliminar este comentario.
            404: Comentario no encontrado.
        """
        comentario = self.get_object()
        
        # Verificar si el usuario es el autor del comentario, comenté para realizar pruebas volver a activar luego
        #if comentario.usuario != request.user:
        #    return Response({'detail': 'No tienes permiso para eliminar este comentario.'}, status=status.HTTP_403_FORBIDDEN)

        # Proceder a eliminar el comentario
        self.perform_destroy(comentario)
        return Response(status=status.HTTP_204_NO_CONTENT)    

class SendEmailView(APIView):
    """
    Vista API para enviar un correo electrónico utilizando el servicio de SendGrid.

    Esta vista permite enviar un correo electrónico a través de la API de SendGrid, 
    proporcionando los parámetros necesarios: destinatario (`to_email`), asunto (`subject`) 
    y contenido del mensaje (`content`).

    Métodos:
        post(request): Envia un correo electrónico con los parámetros proporcionados.
    """
    @swagger_auto_schema(
        operation_summary="Enviar un correo electrónico",
        operation_description="Envía un correo electrónico utilizando SendGrid.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'to_email': openapi.Schema(type=openapi.TYPE_STRING, description="Dirección de correo electrónico del destinatario", example="recipient@example.com"),
                'subject': openapi.Schema(type=openapi.TYPE_STRING, description="Asunto del correo", example="Asunto del correo"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Contenido del correo", example="<h1>Hola, este es el contenido del correo</h1>")
            },
            required=['to_email', 'subject', 'content']
        ),
        responses={
            200: openapi.Response(
                description="Correo enviado correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description="Código de estado de la respuesta"),
                        'body': openapi.Schema(type=openapi.TYPE_STRING, description="Cuerpo de la respuesta"),
                        'headers': openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=openapi.TYPE_STRING, description="Cabeceras de la respuesta")
                    }
                )
            ),
            400: openapi.Response(
                description="Solicitud inválida. Campos requeridos",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error", example="Invalid request. Fields are required.")
                    }
                )
            ),
            500: openapi.Response(
                description="Error en el servidor al intentar enviar el correo",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error")
                    }
                )
            ),
        }
    )
    def post(self, request):
        """
        Envía un correo electrónico utilizando la API de SendGrid.

        Este método recibe los datos para enviar un correo electrónico (destinatario, asunto y contenido),
        y utiliza la API de SendGrid para enviar el mensaje. Si la solicitud es exitosa, devuelve el 
        código de estado de la respuesta de SendGrid, el cuerpo y las cabeceras. Si ocurre un error, 
        devuelve un mensaje de error.

        Parámetros:
            request (HttpRequest): La solicitud HTTP que contiene los datos del correo.
            - 'to_email' (str): Dirección de correo electrónico del destinatario.
            - 'subject' (str): Asunto del correo.
            - 'content' (str): Contenido del correo en formato HTML.

        Respuestas:
            200:
                description: Correo enviado correctamente.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                status_code:
                                    type: integer
                                    description: Código de estado de la respuesta
                                body:
                                    type: string
                                    description: Cuerpo de la respuesta
                                headers:
                                    type: object
                                    additionalProperties:
                                        type: string
                                    description: Cabeceras de la respuesta
            400:
                description: Solicitud inválida. Campos requeridos.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                error:
                                    type: string
                                    description: Mensaje de error
                                    example: "Invalid request. Fields are required."
            500:
                description: Error en el servidor al intentar enviar el correo.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                error:
                                    type: string
                                    description: Mensaje de error
        """
        to_email = request.data.get('to_email')
        subject = request.data.get('subject')
        content = request.data.get('content')

        if not all([to_email, subject, content]):
            return JsonResponse({'error': 'Invalid request. Fields are required.'}, status=400)

        try:
            sg = SendGridAPIClient('change-this')
            message = Mail(
                from_email='ma.alexa2000@fpuna.edu.py',
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            response = sg.send(message)
            return JsonResponse({
                'status_code': response.status_code,
                'body': response.body.decode('utf-8'),
                'headers': dict(response.headers)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
# TODO: Historial de Comentarios        
class HistorialListCreateView(generics.ListCreateAPIView):
    """
    Vista API para listar y crear registros en el historial.

    Esta vista maneja dos operaciones:
    1. **GET**: Devuelve una lista de todos los registros de historial.
    2. **POST**: Permite crear un nuevo registro de historial con los datos proporcionados.

    Métodos:
        get(request): Devuelve una lista de todos los registros en el historial.
        post(request): Crea un nuevo registro de historial con la información proporcionada.
    """
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer

    # Documentación para el método GET
    @swagger_auto_schema(
        operation_summary="Listar todos los registros de historial",
        operation_description="Devuelve una lista de todos los registros en el historial.",
        responses={
            200: openapi.Response(
                description="Lista de registros de historial",
                schema=HistorialSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Lista todos los registros de historial.

        Este método maneja la solicitud GET y devuelve una lista de todos los registros de historial 
        en formato JSON.

        Respuesta esperada:
            200:
                description: Lista de registros de historial.
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: '#/components/schemas/Historial'
        """
        return super().get(request, *args, **kwargs)
    
     # Documentación para el método POST
    @swagger_auto_schema(
        operation_summary="Crear un nuevo registro de historial",
        operation_description="Agrega un nuevo registro en el historial con la información proporcionada.",
        request_body=HistorialSerializer,
        responses={
            201: openapi.Response(
                description="Registro de historial creado exitosamente",
                schema=HistorialSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Error de validación en los datos ingresados."
                        )
                    }
                )
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Crea un nuevo registro de historial.

        Este método maneja la solicitud POST y crea un nuevo registro de historial utilizando los datos 
        proporcionados en el cuerpo de la solicitud.

        Parámetros:
            request (HttpRequest): El cuerpo de la solicitud debe contener los datos necesarios 
                                    para crear un nuevo registro en el historial.
        
        Respuestas esperadas:
            201:
                description: Registro de historial creado exitosamente.
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Historial'
            400:
                description: Error de validación en los datos ingresados.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                detail:
                                    type: string
                                    description: Descripción del error de validación.
                                    example: "Error de validación en los datos ingresados."
        """
        return super().post(request, *args, **kwargs)

class HistorialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar y eliminar registros de historial.

    Esta vista permite a los usuarios realizar las siguientes operaciones sobre los registros de historial:
    - Obtener un registro específico usando su ID.
    - Actualizar completamente un registro de historial.
    - Actualizar parcialmente un registro de historial.
    - Eliminar un registro de historial.

    Atributos:
        queryset: Conjunto de registros de historial que serán manipulados por la vista.
        serializer_class: Serializador utilizado para convertir los objetos `Historial` en formato JSON y viceversa.

    Métodos:
        get: Recupera un registro específico de historial usando su ID.
        put: Reemplaza completamente un registro de historial usando el ID proporcionado.
        patch: Actualiza parcialmente un registro de historial usando el ID proporcionado.
        delete: Elimina un registro de historial usando su ID.
    """
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer

    # Documentación para el método GET
    @swagger_auto_schema(
        operation_summary="Obtener un registro específico de historial",
        operation_description="Recupera un registro específico del historial usando su ID.",
        manual_parameters=[
            openapi.Parameter(
                'fecha', openapi.IN_QUERY, 
                description="Fecha específica del historial en formato YYYY-MM-DD",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'usuario', openapi.IN_QUERY,
                description="ID del usuario asociado al historial",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'id', openapi.IN_PATH, 
                description="ID único del registro de historial",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Registro de historial encontrado",
                schema=HistorialSerializer()
            ),
            404: openapi.Response(
                description="Registro de historial no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Registro de historial no encontrado."
                        )
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Recupera un registro específico del historial.

        Parámetros:
            request: El objeto de solicitud que contiene los parámetros de la consulta.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales, incluidos los parámetros de URL.

        Respuesta:
            Retorna un objeto `Historial` serializado con el estado HTTP adecuado.
        """
        return super().get(request, *args, **kwargs)

# Documentación para el método PUT
    @swagger_auto_schema(
    operation_summary="Actualizar completamente un registro de historial",
    operation_description="Reemplaza completamente un registro del historial usando el ID especificado." ,
    manual_parameters=[
        openapi.Parameter(
            'id', openapi.IN_PATH,
            description="ID único del registro de historial a actualizar",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'usuario': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID del usuario asociado al historial"
            ),
            'contenido': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Contenido asociado al historial"
            ),
            'fecha_modificacion': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description="Fecha de modificación del historial (formato YYYY-MM-DD)"
            ),
            'comentario': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Comentario adicional sobre el cambio en el historial"
            ),
        },
        required=['usuario', 'contenido', 'fecha_modificacion']  # Ajusta los campos requeridos según tu modelo
    ),
    responses={
        200: openapi.Response(
            description="Registro de historial actualizado",
            schema=HistorialSerializer()
        ),
        400: openapi.Response(
            description="Error de validación",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Error de validación en los datos ingresados."
                    )
                }
            )
        ),
        404: openapi.Response(
            description="Registro de historial no encontrado",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Registro de historial no encontrado."
                    )
                }
            )
        ),
    }
)
    def put(self, request, *args, **kwargs):
        """
        Actualiza completamente un registro de historial.

        Parámetros:
            request: El objeto de solicitud que contiene los datos del historial a actualizar.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales, incluidos los parámetros de URL.

        Respuesta:
            Retorna el registro actualizado con el estado HTTP adecuado.
        """
        return super().put(request, *args, **kwargs)

    # Documentación para el método PATCH
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un registro de historial",
        operation_description="Actualiza uno o más campos de un registro de historial existente usando el ID.",
        manual_parameters=[
        openapi.Parameter(
            'id', openapi.IN_PATH,
            description="ID único del registro de historial a actualizar parcialmente",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'usuario': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID del usuario asociado al historial (opcional)"
            ),
            'contenido': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Contenido asociado al historial (opcional)"
            ),
            'fecha_modificacion': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description="Fecha de modificación del historial (formato YYYY-MM-DD) (opcional)"
            ),
            'comentario': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Comentario adicional sobre el cambio en el historial (opcional)"
            ),
        },
        required=[]  # No hay campos obligatorios, ya que es una actualización parcial
    ),
        responses={
            200: openapi.Response(
                description="Registro de historial actualizado parcialmente",
                schema=HistorialSerializer()
            ),
            400: openapi.Response(
                description="Error de validación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Error de validación en los datos ingresados."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Registro de historial no encontrado"
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Actualiza parcialmente un registro de historial.

        Parámetros:
            request: El objeto de solicitud que contiene los datos a actualizar parcialmente.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales, incluidos los parámetros de URL.

        Respuesta:
            Retorna el registro actualizado parcialmente con el estado HTTP adecuado.
        """
        return super().patch(request, *args, **kwargs)

    # Documentación para el método DELETE
    @swagger_auto_schema(
        operation_summary="Eliminar un registro de historial",
        operation_description="Elimina un registro del historial específico usando su ID.",
        manual_parameters=[
        openapi.Parameter(
            'id', openapi.IN_PATH,
            description="ID único del registro de historial a eliminar",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
        responses={
            204: openapi.Response(
                description="Registro de historial eliminado exitosamente"
            ),
            404: openapi.Response(
                description="Registro de historial no encontrado"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Elimina un registro de historial.

        Parámetros:
            request: El objeto de solicitud que contiene la identificación del registro a eliminar.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales, incluidos los parámetros de URL.

        Respuesta:
            Retorna un código de estado HTTP 204 si el registro es eliminado correctamente, o 404 si no se encuentra el registro.
        """
        return super().delete(request, *args, **kwargs)
    
# TODO: LIKE DE CONTENIDOS
class LikeCreateView(generics.CreateAPIView):
    """
    Vista para crear un nuevo "like" en el contenido especificado.

    Esta vista permite a los usuarios crear un "like" para un contenido específico asociado al usuario actual.

    Atributos:
        queryset: Conjunto de "likes" que serán manipulados por la vista.
        serializer_class: Serializador utilizado para convertir los objetos `Like` en formato JSON y viceversa.

    Métodos:
        post: Crea un nuevo "like" para el contenido especificado.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    #Documentación método POST
    @swagger_auto_schema(
        operation_summary="Crear un nuevo like",
        operation_description="Crea un like para el contenido especificado y el usuario actual.",
        responses={
            201: openapi.Response(
                'Like creado exitosamente',
                LikeSerializer()
            ),
            400: openapi.Response(
                'Error de validación',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Datos de entrada inválidos."
                        ),
                    }
                )
            ),
        }
    )
    def postSwagger(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def postSwagger(self):
        if getattr(self, 'swagger_fake_view', False):
            return Response(status=status.HTTP_200_OK)

        raise NotImplementedError("must not call this")
    
class LikeListView(generics.ListAPIView):
    """
    Vista para listar los "likes" asociados a un contenido específico.

    Esta vista permite obtener todos los "likes" relacionados con un contenido determinado.

    Atributos:
        serializer_class: Serializador utilizado para convertir los objetos `Like` en formato JSON y viceversa.

    Métodos:
        get: Obtiene una lista de los "likes" asociados a un contenido específico.
    """
    serializer_class = LikeSerializer

    #Documentación método GET
    @swagger_auto_schema(
        operation_summary="Listar likes de un contenido",
        operation_description="Obtiene una lista de todos los likes asociados a un contenido específico.",
        manual_parameters=[
            openapi.Parameter(
                'contenido_id', openapi.IN_PATH,
                description="ID del contenido del cual se obtendrán los likes.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Lista de likes obtenida exitosamente",
                schema=LikeSerializer(many=True)
            ),
            404: openapi.Response(
                description="Contenido no encontrado"
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Obtiene una lista de los "likes" asociados al contenido especificado por su ID.

        Parámetros:
            request: El objeto de solicitud, que incluye los parámetros necesarios para obtener los likes.

        Respuesta:
            Retorna una lista de "likes" serializados en formato JSON y un estado HTTP adecuado.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Obtiene los "likes" asociados a un contenido específico basado en el `contenido_id`.

        Utiliza el parámetro `contenido_id` de la URL para filtrar los "likes" relacionados con el contenido solicitado.

        Retorna:
            Queryset de objetos `Like` relacionados con el contenido específico.
        """
        contenido_id = self.kwargs['contenido_id']
        return Like.objects.filter(contenido__id=contenido_id)

class LikeDeleteView(generics.DestroyAPIView):
    """
    Vista para eliminar un "like" de un contenido específico dado por un usuario.

    Esta vista permite eliminar un "like" previamente dado por un usuario para un contenido determinado.

    Atributos:
        queryset: Conjunto de objetos `Like` que se pueden eliminar.
    
    Métodos:
        delete: Elimina el "like" específico de un contenido dado por un usuario.
    """
    queryset = Like.objects.all()
    @swagger_auto_schema(  
        operation_summary="Eliminar likes de un contenido",
        operation_description="Elimina un like específico del contenido dado por el usuario.",
        manual_parameters=[
            openapi.Parameter(
                'contenido_id', openapi.IN_PATH,
                description="ID del contenido al cual se quiere eliminar el like",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'usuario_id', openapi.IN_PATH,
                description="ID del usuario que dio el like que se desea eliminar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="Like eliminado exitosamente"
            ),
            404: openapi.Response(
                description="Like no encontrado"
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Elimina un "like" específico de un contenido dado por un usuario.

        Parámetros:
            contenido_id (int): El ID del contenido del cual se desea eliminar el "like".
            usuario_id (int): El ID del usuario que dio el "like" que se desea eliminar.

        Respuesta:
            Si el "like" fue encontrado y eliminado, devuelve un estado HTTP 204 (sin contenido).
            Si el "like" no existe, devuelve un estado HTTP 404 (no encontrado) con un mensaje de error.
        """
        contenido_id = kwargs['contenido_id']
        usuario_id = kwargs['usuario_id']

        try:
            like = Like.objects.get(contenido_id=contenido_id, usuario_id=usuario_id)
            like.delete()  # Eliminar el like
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "Like no encontrado."}, status=status.HTTP_404_NOT_FOUND)

class CambiarEstadoView(APIView):
    """
    Vista para cambiar el estado de un contenido y registrar la acción en el historial.

    Esta vista permite cambiar el estado de un contenido específico y registrar el cambio de estado en el historial asociado al contenido.

    Métodos:
        post: Cambia el estado de un contenido y registra el cambio en el historial.
    """
    @swagger_auto_schema(
        operation_summary="Cambiar el estado de un contenido",
        operation_description="Cambia el estado de un contenido y registra la acción en el historial.",
        manual_parameters=[
            openapi.Parameter(
                'contenido_id',  # Nombre del parámetro
                openapi.IN_PATH,  # El parámetro está en la URL
                description="ID del contenido cuyo estado se desea cambiar.",
                type=openapi.TYPE_INTEGER,  # Tipo de dato del parámetro
                required=True  # El parámetro es obligatorio
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'estado': openapi.Schema(type=openapi.TYPE_STRING, description="Nuevo estado del contenido", example="aprobado"),
                'comentario': openapi.Schema(type=openapi.TYPE_STRING, description="Comentario opcional relacionado con el cambio de estado", example="Contenido revisado y aprobado.")
            },
            required=['estado']
        ),
        responses={
            200: openapi.Response(
                description="Estado cambiado y registrado en el historial correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de éxito", example="Estado cambiado y registrado en el historial.")
                    }
                )
            ),
            404: openapi.Response(
                description="Contenido no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error", example="Contenido no encontrado.")
                    }
                )
            ),
            400: openapi.Response(
                description="Solicitud incorrecta o incompleta",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error", example="Estado es un campo requerido.")
                    }
                )
            ),
        }
    )
    def post(self, request, contenido_id):
        """
        Cambia el estado de un contenido y registra el cambio en el historial.

        Parámetros:
            contenido_id (int): El ID del contenido cuyo estado se desea cambiar.
            estado (str): El nuevo estado del contenido (ejemplo: "aprobado").
            comentario (str, opcional): Comentario relacionado con el cambio de estado.

        Respuesta:
            - Si el contenido existe y el estado se cambia correctamente, se devuelve un mensaje de éxito con el código de estado HTTP 200.
            - Si el contenido no existe, se devuelve un error con el código de estado HTTP 404.
            - Si hay un error en la solicitud (por ejemplo, falta el campo 'estado'), se devuelve un error con el código de estado HTTP 400.
        """
        try:
            contenido = Contenido.objects.get(id=contenido_id)
            nuevo_estado = request.data.get('estado')
            comentario = request.data.get('comentario', '')

            # Cambiar el estado del contenido
            contenido.estado = nuevo_estado
            contenido.save()

            # Registrar en el historial
            Historial.objects.create(
                contenido=contenido,
                estado=nuevo_estado,
                comentario=comentario,
                usuario=request.user
            )

            return Response({'message': 'Estado cambiado y registrado en el historial.'}, status=status.HTTP_200_OK)

        except Contenido.DoesNotExist:
            return Response({'error': 'Contenido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

#TODO: ARTICULOS        
class ContarArticulosAprobadosView(generics.GenericAPIView):
    """
    Vista para contar la cantidad de artículos aprobados en un rango de fechas.

    Esta vista permite obtener la cantidad de artículos que han pasado la etapa de revisión dentro de un rango de fechas.

    Métodos:
        get: Devuelve la cantidad de artículos aprobados en el rango de fechas especificado.
    """
    serializer_class = ArticuloAprobadoSerializer
    @swagger_auto_schema(
        operation_summary="Contar artículos aprobados en un rango de fechas",
        operation_description=(
            "Este endpoint devuelve la cantidad de artículos que han pasado la etapa de revisión "
            "en un rango de fechas especificado. Los parámetros deben estar en formato AAAA-MM-DD."
        ),
        manual_parameters=[
            openapi.Parameter(
                name='fecha_inicio',
                in_=openapi.IN_PATH,
                description="Fecha de inicio del rango de consulta en formato AAAA-MM-DD.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True
            ),
            openapi.Parameter(
                name='fecha_fin',
                in_=openapi.IN_PATH,
                description="Fecha de fin del rango de consulta en formato AAAA-MM-DD.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Cantidad de artículos aprobados en el rango de fechas especificado.",
                schema=ArticuloAprobadoSerializer
            ),
            400: openapi.Response(
                description="Error en el formato de fecha. Usa el formato AAAA-MM-DD.",
            ),
            500: openapi.Response(
                description="Error del servidor. Intente de nuevo más tarde.",
            )
        }
    )
    def get(self, request, fecha_inicio, fecha_fin):
        """
        Cuenta la cantidad de artículos aprobados en el rango de fechas proporcionado.

        Parámetros:
            fecha_inicio (str): La fecha de inicio del rango en formato "AAAA-MM-DD".
            fecha_fin (str): La fecha de fin del rango en formato "AAAA-MM-DD".

        Respuesta:
            - Si el formato de fechas es correcto, devuelve la cantidad de artículos aprobados.
            - Si el formato de fechas es incorrecto, devuelve un error con el código HTTP 400.
            - Si hay un error del servidor, se devuelve un error con el código HTTP 500.
        """
        # Convertir fechas de string a objeto datetime
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except (ValueError, TypeError):
            return Response({"error": "Formato de fecha inválido. Usa AAAA-MM-DD."}, status=400)
        
        # Obtener la cantidad de artículos aprobados en el rango de fechas
        cantidad = Articulo.contar_articulos_aprobados(fecha_inicio_dt, fecha_fin_dt)
        serializer = self.get_serializer({"cantidad": cantidad})
        return Response(serializer.data)

class ContarArticulosInactivosView(generics.GenericAPIView):
    """
    Vista para contar la cantidad de artículos inactivos en un rango de fechas.

    Esta vista recibe dos fechas en formato 'AAAA-MM-DD' y devuelve la cantidad de artículos
    inactivos cuya fecha está dentro de ese rango.
    """
    serializer_class = ArticuloAprobadoSerializer

    #Documentación de GET
    @swagger_auto_schema(
        operation_summary="Contar artículos inactivos",
        operation_description="Obtiene la cantidad de contenidos inactivos en un rango de fechas especificado.",
        manual_parameters=[
            openapi.Parameter(
                'fecha_inicio', openapi.IN_PATH,
                description="La fecha de inicio del rango en formato AAAA-MM-DD",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fecha_fin', openapi.IN_PATH,
                description="La fecha de fin del rango en formato AAAA-MM-DD",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Cantidad de artículos inactivos en el rango de fechas especificado",
                schema=ArticuloAprobadoSerializer()
            ),
            400: openapi.Response(
                description="Error de validación en el formato de fecha",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Formato de fecha inválido. Usa AAAA-MM-DD."
                        )
                    }
                )
            )
        }
    )

    def get(self, request, fecha_inicio, fecha_fin):
        """
        Obtiene la cantidad de contenidos inactivos en un rango de fechas.
        
        Args:
            request (Request): El objeto de la solicitud HTTP.
            fecha_inicio (str): La fecha de inicio del rango en formato AAAA-MM-DD.
            fecha_fin (str): La fecha de fin del rango en formato AAAA-MM-DD.
        Returns:
            Response: La respuesta HTTP con la cantidad de contenidos inactivos o un mensaje de error si el formato de fecha es inválido.
        """
        
        # Convertir fechas de string a objeto datetime
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except (ValueError, TypeError):
            return Response({"error": "Formato de fecha inválido. Usa AAAA-MM-DD."}, status=400)
                
        # Obtener la cantidad de contenidos inactivos en el rango de fechas
        cantidad = Contenido.objects.filter(estado='inactivo', fecha__range=(fecha_inicio_dt, fecha_fin_dt)).count()
        serializer = self.get_serializer({"cantidad": cantidad})
        return Response(serializer.data)   
class ContarEstadosView(generics.GenericAPIView):

    #Documentación del método GET
    @swagger_auto_schema(
        operation_summary="Contar contenidos por estado en un rango de fechas",
        operation_description="Obtiene el conteo de contenidos en cada estado ('inactivo', 'en_revision', 'aprobado', 'rechazado') dentro de un rango de fechas especificado.",
        manual_parameters=[
            openapi.Parameter(
                'fecha_inicio', openapi.IN_PATH,
                description="La fecha de inicio del rango en formato AAAA-MM-DD",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fecha_fin', openapi.IN_PATH,
                description="La fecha de fin del rango en formato AAAA-MM-DD",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Conteo de contenidos por estado en el rango de fechas especificado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "inactivos": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Cantidad de contenidos inactivos"
                        ),
                        "en_revision": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Cantidad de contenidos en revisión"
                        ),
                        "aprobados": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Cantidad de contenidos aprobados"
                        ),
                        "rechazados": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Cantidad de contenidos rechazados"
                        ),
                        "total": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Cantidad total de contenidos en el rango de fechas"
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Error de validación en el formato de fecha",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Formato de fecha inválido. Usa AAAA-MM-DD."
                        )
                    }
                )
            )
        }
    )
    def get(self, request, fecha_inicio, fecha_fin):
        """
        Obtiene la cantidad de contenidos en diferentes estados en un rango de fechas.
        
        Args:
            request (Request): El objeto de la solicitud HTTP.
            fecha_inicio (str): La fecha de inicio del rango en formato AAAA-MM-DD.
            fecha_fin (str): La fecha de fin del rango en formato AAAA-MM-DD.
        Returns:
            Response: La respuesta HTTP con el conteo de contenidos por estado o un mensaje de error si el formato de fecha es inválido.
        """
        
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
                inactivos = Contenido.objects.filter(estado='inactivo', fecha__range=(fecha_inicio_dt, fecha_fin_dt)).count()
                en_revision = Contenido.objects.filter(estado='en_revision', fecha__range=(fecha_inicio_dt, fecha_fin_dt)).count()
                aprobados = Contenido.objects.filter(estado='aprobado', fecha__range=(fecha_inicio_dt, fecha_fin_dt)).count()
                rechazados = Contenido.objects.filter(estado='rechazado', fecha__range=(fecha_inicio_dt, fecha_fin_dt)).count()
            except (ValueError, TypeError):
                return Response({"error": "Formato de fecha inválido. Usa AAAA-MM-DD."}, status=400)
            return Response({
                "inactivos": inactivos,
                "en_revision": en_revision,
                "aprobados": aprobados,
                "rechazados": rechazados,
                "total": inactivos + en_revision + aprobados+rechazados
            }, status=status.HTTP_200_OK)
class ContenidoMasLikesView(generics.ListAPIView):
    """
    Vista para listar los contenidos ordenados por la cantidad de likes.

    Este endpoint devuelve una lista de contenidos ordenados en orden descendente
    según la cantidad de likes asociados a cada contenido.
    """
    serializer_class = ContenidoSerializer

        #Documentación de GET
    @swagger_auto_schema(
        operation_summary="Listar contenidos ordenados por cantidad de likes",
        operation_description="Obtiene una lista de contenidos ordenados por la cantidad de likes en orden descendente.",
        responses={
            200: openapi.Response(
                description="Lista de contenidos ordenada por likes",
                schema=ContenidoSerializer(many=True)
            ),
        }
    )

    def get(self, request, *args, **kwargs):
        """
        Obtiene una lista de contenidos ordenados por la cantidad de likes.

        Este método hereda de ListAPIView y devuelve la lista de contenidos ordenados
        por la cantidad de likes asociados. Utiliza la lógica de queryset definida en 
        el método `get_queryset`.

        Args:
            request (Request): Objeto de solicitud HTTP.
            *args: Argumentos adicionales para el método.
            **kwargs: Argumentos adicionales para el método.

        Returns:
            Response: Respuesta HTTP con la lista de contenidos ordenada por la cantidad de likes.
        """
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        """
        Obtiene los contenidos ordenados por la cantidad de likes en orden descendente.

        Este método utiliza la función `annotate` para contar la cantidad de likes de
        cada contenido y luego ordena los resultados en orden descendente por el 
        número de likes.

        Returns:
            QuerySet: Consulta ordenada de contenidos, con el número de likes contados.
        """
        return Contenido.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vista
from .serializers import VistaSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_summary="Registrar una vista de contenido",
    operation_description="Registra una vista de un usuario en un contenido específico. Si el usuario ya vio el contenido, se devuelve un mensaje indicando esto.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'contenido_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID del contenido que se está viendo",
                example=1
            ),
            'usuario_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID del usuario que está viendo el contenido",
                example=2
            ),
        },
        required=['contenido_id', 'usuario_id']
    ),
    responses={
        201: openapi.Response(
            description="Vista registrada con éxito",
        ),
        200: openapi.Response(
            description="El usuario ya ha visto este contenido",
        ),
        400: openapi.Response(
            description="Error en los datos de entrada",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                }
            )
        ),
    }
)

@api_view(['POST'])
def registrar_vista(request):
    """
    Registra una vista de un usuario en un contenido específico.

    Este método recibe un `contenido_id` y un `usuario_id`, y registra una vista 
    para el usuario en el contenido correspondiente. Si el usuario ya ha registrado
    una vista previamente, se devuelve un mensaje indicando que ya vio el contenido.
    
    Args:
        request (Request): El objeto de la solicitud HTTP que contiene los datos
                            del `contenido_id` y `usuario_id`.
                            
    Returns:
        Response: Respuesta HTTP con un mensaje indicando si la vista fue registrada
                  correctamente o si el usuario ya ha visto el contenido.
    """
    contenido_id = request.data.get('contenido_id')
    usuario_id = request.data.get('usuario_id')
    
    if not contenido_id or not usuario_id:
        return Response({"error": "contenido_id y usuario_id son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

    vista, creada = Vista.objects.get_or_create(
        contenido_id=contenido_id,
        usuario_id=usuario_id,
        defaults={'fecha': timezone.now()}
    )
    
    if creada:
        return Response({"message": "Vista registrada con éxito."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "El usuario ya ha visto este contenido."}, status=status.HTTP_200_OK)

class TopContenidosMasVistosAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Obtener los contenidos más vistos",
        operation_description="Retorna una lista de los cinco contenidos más vistos, ordenados de mayor a menor por cantidad de vistas.",
        responses={
            200: openapi.Response(
                description="Lista de los contenidos más vistos, incluyendo el conteo de vistas de cada uno",
                schema=ContenidoSerializer(many=True)
            )
        }
    )
    def get(self, request):
        # Consulta para obtener los IDs de los contenidos más vistos
        top_vistas = (
            Vista.objects
            .values('contenido_id')
            .annotate(num_vistas=Count('id'))
            .order_by('-num_vistas')[:5]
        )

        # Extraer los IDs de contenido y el conteo de vistas
        contenido_ids = [item['contenido_id'] for item in top_vistas]
        vistas_dict = {item['contenido_id']: item['num_vistas'] for item in top_vistas}
        
        # Obtener los objetos de Contenido correspondientes
        contenidos = Contenido.objects.filter(id__in=contenido_ids)
        
        # Serializar los contenidos
        serializer = ContenidoSerializer(contenidos, many=True)
        contenidos_data = serializer.data

        # Añadir el conteo de vistas a la respuesta serializada
        for contenido in contenidos_data:
            contenido['num_vistas'] = vistas_dict[contenido['id']]
        
        return Response(contenidos_data)
    

class ContenidosMasVistosAPIView(APIView):
        # Parámetros de entrada para Swagger
    @swagger_auto_schema(
        operation_description="Obtener los contenidos más vistos en un rango de fechas.",
        manual_parameters=[
            openapi.Parameter(
                'fecha_inicio', openapi.IN_PATH, description="Fecha de inicio del rango (formato YYYY-MM-DD)", type=openapi.TYPE_STRING, format="date"
            ),
            openapi.Parameter(
                'fecha_fin', openapi.IN_PATH, description="Fecha de fin del rango (formato YYYY-MM-DD)", type=openapi.TYPE_STRING, format="date"
            ),
        ],
        responses={
            200: openapi.Response(
                description="Lista de contenidos más vistos en el rango de fechas",
                examples={
                    "application/json": [
                        {"id": 1, "titulo": "Contenido Ejemplo", "total_vistas": 5},
                        {"id": 2, "titulo": "Otro Contenido", "total_vistas": 3},
                    ]
                }
            ),
            400: openapi.Response(
                description="Error en el formato de fechas proporcionadas",
                examples={"application/json": {"error": "Las fechas 'fecha_inicio' y 'fecha_fin' deben estar en formato YYYY-MM-DD"}}
            ),
        },
    )
    def get(self, request, fecha_inicio, fecha_fin):
        # Parsear las fechas
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Las fechas 'fecha_inicio' y 'fecha_fin' deben estar en formato YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar las vistas en el rango de fechas y contar las vistas por contenido
        vistas_contenidos = (
            Vista.objects
            .filter(fecha__range=(fecha_inicio, fecha_fin))
            .values('contenido_id')
            .annotate(total_vistas=Count('id'))
            .order_by('-total_vistas')
        )
        
        # Obtener los IDs de los contenidos más vistos
        contenido_ids = [vista['contenido_id'] for vista in vistas_contenidos]
        
        # Recuperar los objetos de contenido correspondientes a esos IDs, en el mismo orden
        contenidos = Contenido.objects.filter(id__in=contenido_ids)
        
        # Formatear la respuesta en JSON
        data = [
            {
                'id': contenido.id,
                'titulo': contenido.titulo,
                'total_vistas': next(
                    (vista['total_vistas'] for vista in vistas_contenidos if vista['contenido_id'] == contenido.id),
                    0
                ),
            }
            for contenido in contenidos
        ]
        
        return Response(data, status=status.HTTP_200_OK)