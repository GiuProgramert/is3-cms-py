from rest_framework import serializers
from .models import Historial, Like, Parametro, Categoria, Subcategoria, Contenido
from .models import Usuario, Rol, Permiso
class ParametroSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Parametro. 

    Este serializador convierte las instancias del modelo Parametro a JSON y viceversa,
    permitiendo la fácil transmisión de datos entre el modelo y las vistas de la API.

    Métodos:
        Meta: Define el modelo que se serializará y los campos que se incluirán en la serialización.

    Atributos:
        model (Model): El modelo al que se asociará el serializador (en este caso, Parametro).
        fields (list): La lista de campos que serán serializados. En este caso, '__all__' incluye todos los campos del modelo.
    """
    
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Parametro.
        fields (list): Los campos del modelo que se incluyen en la serialización. Usamos '__all__' para incluir todos los campos.

        Ejemplo de uso:
            >>> parametro = Parametro.objects.first()
            >>> serializer = ParametroSerializer(parametro)
            >>> serializer.data
            {'id': 1, 'nombre': 'parametro1', 'valor': 'valor1'}
        """
        model = Parametro
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Categoria.

    Este serializador convierte las instancias del modelo Categoria a JSON y viceversa,
    permitiendo la fácil transmisión de datos entre el modelo y las vistas de la API.

    Métodos:
        Meta: Define el modelo que se serializará y los campos que se incluirán en la serialización.

    Atributos:
        model (Model): El modelo al que se asociará el serializador (en este caso, Categoria).
        fields (list): La lista de campos que serán serializados. En este caso, '__all__' incluye todos los campos del modelo.
    """
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Categoria.
        fields (list): Los campos del modelo que se incluyen en la serialización. Usamos '__all__' para incluir todos los campos.

        Ejemplo de uso:
            >>> categoria = Categoria.objects.first()
            >>> serializer = CategoriaSerializer(categoria)
            >>> serializer.data
            {'id': 1, 'codigo': 'cat_001', 'nombre': 'Categoría 1'}
        """
        model = Categoria
        fields = '__all__'

class SubcategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Subcategoria.

    Este serializador convierte las instancias del modelo Subcategoria a JSON y viceversa, y valida
    que el nombre de la subcategoría sea único dentro de la misma categoría.

    Métodos:
        validate_nombre: Valida que el nombre de la subcategoría sea único dentro de la categoría.
        
    Atributos:
        model (Model): El modelo que se serializa, en este caso, Subcategoria.
        fields (list): Los campos del modelo que se incluyen en la serialización. Usamos '__all__' para incluir todos los campos.
    """
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Subcategoria.
        fields (list): Los campos del modelo que se incluyen en la serialización. Usamos '__all__' para incluir todos los campos.
        """
        model = Subcategoria
        fields = '__all__'

    def validate_nombre(self, value):
        """
        Valida que el nombre de la subcategoría sea único dentro de la categoría.

        Parámetros:
            value (str): El nombre de la subcategoría que se valida.

        Returns:
            str: El valor del nombre si es válido.

        Raises:
            serializers.ValidationError: Si ya existe una subcategoría con el mismo nombre dentro de la misma categoría.
        """
        categoria = self.initial_data.get('categoria')
        if Subcategoria.objects.filter(nombre=value, categoria=categoria).exists():
            raise serializers.ValidationError("El nombre de la subcategoría debe ser único dentro de la categoría.")
        return value
class CategoriaConSubcategoriasSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Categoria con sus subcategorías anidadas.

    Este serializador incluye las subcategorías asociadas a cada categoría dentro de la respuesta JSON.

    Métodos:
        Meta: Define el modelo de la categoría y los campos que se incluirán en la serialización, incluyendo subcategorías.

    Atributos:
        model (Model): El modelo que se serializa, en este caso, Categoria.
        fields (list): Los campos del modelo que se incluyen en la serialización. Incluye 'id', 'nombre', 'codigo' y subcategorías.
    """
    
    # Anidar las subcategorías dentro de la categoría
    subcategorias = SubcategoriaSerializer(many=True, read_only=True)

    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Categoria.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo las subcategorías.
        """
        model = Categoria
        fields = ['id', 'nombre', 'codigo', 'subcategorias']

from rest_framework import serializers
from .models import Comentario

#TODO: COMENTARIOS
class ComentarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Comentario, que incluye campos adicionales para manejar respuestas anidadas y 
    personalizar la representación de los comentarios.

    Atributos:
        replies (SerializerMethodField): Campo personalizado que serializa las respuestas anidadas del comentario.

    Métodos:
        get_replies(obj): Obtiene y serializa todas las respuestas relacionadas con el comentario actual.
        to_representation(instance): Personaliza la representación en JSON del comentario.
        validate_reply_to(value): Valida el valor de `reply_to` para evitar valores inválidos.

    Ejemplo de uso:
        >>> comentario = Comentario.objects.get(id=1)
        >>> serializer = ComentarioSerializer(comentario)
        >>> serializer.data
        {
            "userId": 1,
            "comId": 1,
            "fullName": "NombreUsuario",
            "userProfile": "https://link-to-profile/user@example.com",
            "text": "Texto del comentario",
            "avatarUrl": "https://ui-avatars.com/api/?name=NombreUsuario&background=random",
            "replies": []
        }
    """

    replies = serializers.SerializerMethodField()  # Campo para las respuestas anidadas

    class Meta:
        model = Comentario
        fields = '__all__'  # Incluimos avatarUrl y replies

    def get_replies(self, obj):
        """
        Obtiene todas las respuestas anidadas para el comentario.

        Parámetros:
            obj (Comentario): El comentario actual para el cual se obtienen las respuestas.

        Retorno:
            list: Lista de datos serializados de los comentarios que son respuestas al comentario actual.

        Ejemplo:
            >>> comentario = Comentario.objects.get(id=1)
            >>> serializer = ComentarioSerializer()
            >>> serializer.get_replies(comentario)
            [{'userId': 2, 'text': 'Respuesta'}]
        """
        # Obtenemos todas las respuestas anidadas para el comentario
        replies = Comentario.objects.filter(reply_to=obj)
        return ComentarioSerializer(replies, many=True).data  # Serializamos las respuestas

    def to_representation(self, instance):
        """
        Personaliza la representación JSON de un comentario.

        Parámetros:
            instance (Comentario): Instancia de `Comentario` que se representa en JSON.

        Retorno:
            dict: Representación personalizada en formato JSON del comentario con campos específicos.

        Ejemplo:
            >>> comentario = Comentario.objects.get(id=1)
            >>> serializer = ComentarioSerializer(comentario)
            >>> serializer.to_representation(comentario)
            {
                "userId": 1,
                "comId": 1,
                "fullName": "NombreUsuario",
                "userProfile": "https://link-to-profile/user@example.com",
                "text": "Texto del comentario",
                "avatarUrl": "https://ui-avatars.com/api/?name=NombreUsuario&background=random",
                "replies": []
            }
        """
        representation = super().to_representation(instance)
        # Estructura que queremos generar
        return {
            "userId": instance.usuario.id if instance.usuario else "Anon",
            "comId": instance.id,
            "fullName": instance.usuario.username if instance.usuario else "Anon",
            "userProfile": f"https://link-to-profile/{instance.usuario.email}" if instance.usuario else '',
            "text": instance.texto,
            "avatarUrl": instance.avatarUrl if instance.avatarUrl else f"https://ui-avatars.com/api/?name={instance.usuario.username if instance.usuario else 'Anon'}&background=random",            
            "replies": self.get_replies(instance) 
        }

    def validate_reply_to(self, value):
        """
        Valida el valor de `reply_to` para asegurar que no sea '0' ni otros valores inválidos.

        Parámetros:
            value (Comentario): Instancia de comentario que representa la respuesta.

        Retorno:
            Comentario: Devuelve el valor de `reply_to` si es válido.

        Excepciones:
            serializers.ValidationError: Se lanza si `reply_to` es igual a '0'.

        Ejemplo:
            >>> serializer = ComentarioSerializer()
            >>> serializer.validate_reply_to(comentario_respuesta)
            comentario_respuesta
        """
        if value == '0':
            raise serializers.ValidationError("reply_to no puede ser '0'.")
        return value

#TODO: HISTORIAL
class HistorialSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Historial.

    Este serializer se utiliza para transformar instancias del modelo Historial en representaciones JSON y viceversa, facilitando la comunicación entre el servidor y el cliente.

    Atributos:
    - model: Especifica que el modelo base para el serializer es el modelo Historial.
    - fields: Incluye todos los campos del modelo Historial en el serializer.

    Métodos:
    - create: (heredado) Permite la creación de una instancia del modelo Historial a partir de datos JSON proporcionados.
    - update: (heredado) Permite la actualización de una instancia existente del modelo Historial.

    Uso:
    El HistorialSerializer se usa en vistas para el manejo de las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre instancias del modelo Historial.
    """

    class Meta:
        model = Historial
        fields = '__all__' 
         
# likes
class LikeSerializer(serializers.ModelSerializer):
    """
    Serializador que representa un "like" en el contenido por parte de un usuario.

    Este serializador se utiliza para validar y serializar los datos relacionados con el modelo `Like`.
    Permite crear un "like" y valida que un usuario no pueda dar "like" múltiples veces al mismo contenido.

    Atributos:
        id (IntegerField): Campo auto incrementable que identifica de manera única a cada "like".
        contenido (ForeignKey): Relación con el modelo 'Contenido', indicando a qué contenido se refiere el "like".
        usuario (ForeignKey): Relación con el modelo 'Usuario', indicando qué usuario ha dado el "like".
        fecha (DateTimeField): Fecha y hora en que se registró el "like".

    Métodos:
        create(validated_data): Crea un nuevo objeto `Like` con los datos validados.
        validate(attrs): Valida los datos, asegurándose de que un usuario no pueda dar "like" a un mismo contenido más de una vez.

    Ejemplo:
        >>> like_serializer = LikeSerializer(data={'contenido': contenido_obj, 'usuario': usuario_obj})
        >>> like_serializer.is_valid()
        True
        >>> like_serializer.save()

    """
    class Meta:
        model = Like
        fields = ['id', 'contenido', 'usuario', 'fecha']

    def create(self, validated_data):
        """
        Crea un nuevo objeto `Like` con los datos validados.

        Parámetros:
            validated_data (dict): Los datos validados que se usarán para crear el "like".

        Retorno:
            Like: Instancia del objeto `Like` creado.

        Ejemplo:
            >>> validated_data = {'contenido': contenido_obj, 'usuario': usuario_obj}
            >>> like = self.create(validated_data)
            >>> like
            Like(id=1, contenido=contenido_obj, usuario=usuario_obj, fecha=<fecha>)
        """
        return Like.objects.create(**validated_data)

    def validate(self, attrs):
        """
        Valida los datos para asegurar que un usuario no pueda dar "like" al mismo contenido más de una vez.

        Parámetros:
            attrs (dict): Los datos a validar (contenido y usuario).

        Retorno:
            dict: Los datos validados.

        Excepciones:
            serializers.ValidationError: Si el usuario ya ha dado "like" al contenido.

        Ejemplo:
            >>> attrs = {'contenido': contenido_obj, 'usuario': usuario_obj}
            >>> self.validate(attrs)
        """
        contenido = attrs.get('contenido')
        usuario = attrs.get('usuario')

        if Like.objects.filter(contenido=contenido, usuario=usuario).exists():
            raise serializers.ValidationError("El usuario ya ha dado like a este contenido.")
        
        return attrs           
class ContenidoSerializer(serializers.ModelSerializer):
    lista_comentarios = serializers.SerializerMethodField()  # Incluir solo comentarios principales
    historiales = HistorialSerializer(many=True, read_only=True)  # Anidar los historiales
    num_likes = serializers.SerializerMethodField()  # Contador de likes
    class Meta:
        model = Contenido
        fields = '__all__'

    def get_lista_comentarios(self, obj):
        # Obtener los comentarios principales del contenido (reply_to=None)
        comentarios_principales = Comentario.objects.filter(contenido=obj, reply_to=None)
        # Usar ComentarioSerializer para serializar solo los comentarios principales
        return ComentarioSerializer(comentarios_principales, many=True).data
    def get_num_likes(self, obj):
        return obj.likes.count()  # Contar los likes relacionados con el contenido    

class ContenidoRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenido
        fields = ['id', 'titulo', 'estado', 'comentarios']

    def update(self, instance, validated_data):
        if 'estado' in validated_data and validated_data['estado'] == 'rechazado':
            comentarios = self.initial_data.get('comentarios')
            instance.rechazar(comentarios=comentarios)
        else:
            instance.aprobar()
        return instance
    
class RolSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Rol.

    Este serializador convierte las instancias del modelo Rol a JSON y viceversa, permitiendo
    la fácil transmisión de datos entre el modelo y las vistas de la API.

    Métodos:
        Meta: Define el modelo que se serializará y los campos que se incluirán en la serialización.

    Atributos:
        model (Model): El modelo al que se asociará el serializador (en este caso, Rol).
        fields (list): La lista de campos que serán serializados. En este caso, incluye 'id' y 'nombre'.
    """
    
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Rol.
        fields (list): Los campos del modelo que se incluyen en la serialización. En este caso, 'id' y 'nombre'.

        Ejemplo de uso:
            >>> rol = Rol.objects.first()
            >>> serializer = RolSerializer(rol)
            >>> serializer.data
            {'id': 1, 'nombre': 'Administrador'}
        """
        model = Rol
        fields = ['id', 'nombre']

class PermisoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Permiso.

    Este serializador convierte las instancias del modelo Permiso a JSON y viceversa, permitiendo
    la transmisión de datos entre el modelo y las vistas de la API.

    Métodos:
        Meta: Define el modelo que se serializará y los campos que se incluirán en la serialización.

    Atributos:
        model (Model): El modelo al que se asociará el serializador (en este caso, Permiso).
        fields (list): La lista de campos que serán serializados. En este caso, incluye 'id' y 'nombre'.

        Ejemplo de uso:
            >>> permiso = Permiso.objects.first()
            >>> serializer = PermisoSerializer(permiso)
            >>> serializer.data
            {'id': 1, 'nombre': 'ver_contenido'}
    """
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Permiso.
        fields (list): Los campos del modelo que se incluyen en la serialización. En este caso, 'id' y 'nombre'.
        """
        model = Permiso
        fields = ['id', 'nombre']

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.

    Este serializador convierte las instancias del modelo Usuario a JSON y viceversa, permitiendo
    la creación, actualización y representación de usuarios junto con sus roles asignados.

    Atributos:
        roles (PrimaryKeyRelatedField): Permite asignar múltiples roles a un usuario utilizando sus identificadores primarios.
        model (Model): El modelo que se serializa, en este caso, Usuario.
        fields (list): La lista de campos que se incluyen en la serialización, incluyendo 'id', 'username', 'email' y 'roles'.

    Métodos:
        create (validated_data): Crea una nueva instancia de Usuario, asignando los roles especificados.
        update (instance, validated_data): Actualiza la instancia de Usuario, modificando los roles si es necesario.
    
    Ejemplo de uso:
        >>> usuario = Usuario.objects.first()
        >>> serializer = UsuarioSerializer(usuario)
        >>> serializer.data
        {'id': 1, 'username': 'juanp', 'email': 'juanp@ejemplo.com', 'roles': [1, 2]}
    """
    roles = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), many=True)
    
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Usuario.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'username', 'email' y 'roles'.
        """
        model = Usuario
        fields = ['id', 'username', 'email', 'roles']

    def create(self, validated_data):
        """
        Crea un nuevo usuario en el sistema.

        Se extraen los roles del `validated_data`, se crea la instancia del usuario, 
        y luego se asignan los roles correspondientes al usuario creado.

        Parámetros:
            validated_data (dict): Los datos validados para crear el nuevo usuario.

        Retorna:
            Usuario: El objeto usuario recién creado, con sus roles asignados.

        Ejemplo de uso:
            >>> validated_data = {'username': 'juanp', 'email': 'juanp@ejemplo.com', 'roles': [1, 2]}
            >>> serializer = UsuarioSerializer(data=validated_data)
            >>> usuario = serializer.save()
        """
        roles_ids = validated_data.pop('roles')
        usuario = super().create(validated_data)
        usuario.roles.set(roles_ids)
        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza un usuario existente en el sistema.

        Se extraen los roles del `validated_data`, se actualizan los campos del usuario,
        y si se proporcionan roles nuevos, se asignan a la instancia de usuario.

        Parámetros:
            instance (Usuario): La instancia del usuario a actualizar.
            validated_data (dict): Los datos validados para actualizar el usuario.

        Retorna:
            Usuario: La instancia de usuario actualizada, con los roles modificados si es necesario.

        Ejemplo de uso:
            >>> instance = Usuario.objects.first()
            >>> validated_data = {'email': 'nuevoemail@ejemplo.com', 'roles': [1]}
            >>> serializer = UsuarioSerializer(instance, data=validated_data)
            >>> usuario = serializer.save()
        """
        roles_ids = validated_data.pop('roles', None)
        usuario = super().update(instance, validated_data)
        if roles_ids is not None:
            usuario.roles.set(roles_ids)
        return usuario

class RolCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para la creación y actualización del modelo Rol.

    Este serializador convierte las instancias del modelo Rol a JSON y viceversa, 
    permitiendo la creación y actualización de roles junto con la asignación de permisos.

    Atributos:
        permisos (PrimaryKeyRelatedField): Permite asignar múltiples permisos a un rol utilizando sus identificadores primarios.
        model (Model): El modelo que se serializa, en este caso, Rol.
        fields (list): La lista de campos que se incluyen en la serialización, incluyendo 'id', 'nombre' y 'permisos'.

    Métodos:
        create (validated_data): Crea una nueva instancia de Rol, asignando los permisos especificados.
        update (instance, validated_data): Actualiza la instancia de Rol, modificando los permisos si es necesario.

    Ejemplo de uso:
        >>> rol = Rol.objects.first()
        >>> serializer = RolCreateUpdateSerializer(rol)
        >>> serializer.data
        {'id': 1, 'nombre': 'Administrador', 'permisos': [1, 2]}
    """
    permisos = serializers.PrimaryKeyRelatedField(queryset=Permiso.objects.all(), many=True)

    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Rol.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'nombre' y 'permisos'.
        """
        model = Rol
        fields = ['id', 'nombre', 'permisos']

    def create(self, validated_data):
        """
        Crea un nuevo rol en el sistema.

        Se extraen los permisos del `validated_data`, se crea la instancia del rol,
        y luego se asignan los permisos correspondientes al rol creado.

        Parámetros:
            validated_data (dict): Los datos validados para crear el nuevo rol.

        Retorna:
            Rol: El objeto rol recién creado, con sus permisos asignados.

        Ejemplo de uso:
            >>> validated_data = {'nombre': 'Editor', 'permisos': [1, 3]}
            >>> serializer = RolCreateUpdateSerializer(data=validated_data)
            >>> rol = serializer.save()
        """
        permisos_ids = validated_data.pop('permisos')
        rol = super().create(validated_data)
        rol.permisos.set(permisos_ids)
        return rol

    def update(self, instance, validated_data):
        """
        Actualiza un rol existente en el sistema.

        Se extraen los permisos del `validated_data`, se actualizan los campos del rol,
        y si se proporcionan permisos nuevos, se asignan a la instancia de rol.

        Parámetros:
            instance (Rol): La instancia del rol a actualizar.
            validated_data (dict): Los datos validados para actualizar el rol.

        Retorna:
            Rol: La instancia de rol actualizada, con los permisos modificados si es necesario.

        Ejemplo de uso:
            >>> instance = Rol.objects.first()
            >>> validated_data = {'nombre': 'Editor', 'permisos': [2, 3]}
            >>> serializer = RolCreateUpdateSerializer(instance, data=validated_data)
            >>> rol = serializer.save()
        """
        permisos_ids = validated_data.pop('permisos', None)
        rol = super().update(instance, validated_data)
        if permisos_ids is not None:
            rol.permisos.set(permisos_ids)
        return rol
    
class RolConPermisosSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Rol, con los permisos anidados.

    Este serializador convierte las instancias del modelo Rol a JSON y viceversa, 
    incluyendo la información detallada de los permisos asociados a cada rol.

    Atributos:
        permisos (PermisoSerializer): Un serializador anidado que incluye los detalles de los permisos asociados al rol.
        model (Model): El modelo que se serializa, en este caso, Rol.
        fields (list): La lista de campos que se incluyen en la serialización, incluyendo 'id', 'nombre' y los permisos anidados.

    Métodos:
        - No tiene métodos adicionales ya que solo se encarga de serializar el rol con sus permisos.

    Ejemplo de uso:
        >>> rol = Rol.objects.first()
        >>> serializer = RolConPermisosSerializer(rol)
        >>> serializer.data
        {'id': 1, 'nombre': 'Administrador', 'permisos': [{'id': 1, 'nombre': 'Crear'}, {'id': 2, 'nombre': 'Eliminar'}]}
    """
    permisos = PermisoSerializer(many=True)  # Anidar los permisos

    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Rol.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'nombre' y 'permisos'.
        """
        model = Rol
        fields = ['id', 'nombre', 'permisos']

class UsuarioConRolesYPermisosSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario, con los roles y permisos anidados.

    Este serializador convierte las instancias del modelo Usuario a JSON y viceversa, 
    incluyendo los detalles de los roles y los permisos asociados a cada rol.

    Atributos:
        roles (RolConPermisosSerializer): Un serializador anidado que incluye los detalles de los roles asociados al usuario,
                                           junto con los permisos que tiene cada rol.

    Meta:
        model (Model): El modelo que se serializa, en este caso, Usuario.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'username', 'email' y los roles con sus permisos anidados.

    Métodos:
        - No tiene métodos adicionales, ya que solo se encarga de serializar el usuario con sus roles y permisos.

    Ejemplo de uso:
        >>> usuario = Usuario.objects.first()
        >>> serializer = UsuarioConRolesYPermisosSerializer(usuario)
        >>> serializer.data
        {'id': 1, 'username': 'jdoe', 'email': 'jdoe@example.com', 
         'roles': [{'id': 1, 'nombre': 'Administrador', 'permisos': [{'id': 1, 'nombre': 'Crear'}, {'id': 2, 'nombre': 'Eliminar'}]}]}
    """
    roles = RolConPermisosSerializer(many=True)  # Anidar los roles

    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Usuario.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'username', 'email' y los roles con permisos anidados.
        """
        model = Usuario
        fields = ['id', 'username', 'email', 'roles']

class ArticuloAprobadoSerializer(serializers.Serializer):
    """
    Clase: ArticuloAprobadoSerializer

    Descripción:
    Este serializer se utiliza para representar la cantidad de artículos aprobados en un rango de fechas. 
    Es parte del proceso de serialización de datos para facilitar la comunicación entre el servidor y el cliente.

    Campos:
    - cantidad (IntegerField): Representa el número total de artículos que han sido aprobados dentro de un rango de fechas específico.
    
    Validaciones:
    - cantidad: Debe ser un número entero. Si no se proporciona un valor válido, se generará un error de validación.

    Uso:
    Este serializer se utiliza para devolver la cantidad de artículos aprobados cuando se consulta la API para contar artículos aprobados en un rango de fechas.
    
    Ejemplo:
    >>> from rest_framework.renderers import JSONRenderer
    >>> serializer = ArticuloAprobadoSerializer(data={'cantidad': 5})
    >>> serializer.is_valid()
    True
    >>> JSONRenderer().render(serializer.data)
    b'{"cantidad": 5}'
    
    Métodos:
    - `__init__(data=None)`: Inicializa el serializer con los datos proporcionados.
    - `is_valid()`: Valida que los datos proporcionados sean correctos.
    - `validated_data`: Devuelve los datos que fueron validados y listos para ser usados.
    """
    cantidad = serializers.IntegerField()

from .models import Vista

class VistaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Vista.

    Este serializador convierte las instancias del modelo Vista a JSON y viceversa.

    Atributos:
        id (int): El identificador único de la vista.
        fecha (datetime): La fecha y hora en la que se registró la vista.
        contenido_id (int): El identificador del contenido asociado a la vista.
        usuario_id (int): El identificador del usuario que realizó la vista.

    Meta:
        model (Model): El modelo que se serializa, en este caso, Vista.
        fields (list): Los campos del modelo que se incluyen en la serialización, incluyendo 'id', 'fecha', 'contenido_id' y 'usuario_id'.

    Métodos:
        - No tiene métodos adicionales, ya que se limita a serializar la vista con los campos definidos.

    Ejemplo de uso:
        >>> vista = Vista.objects.first()
        >>> serializer = VistaSerializer(vista)
        >>> serializer.data
        {'id': 1, 'fecha': '2024-11-01T12:00:00Z', 'contenido_id': 1, 'usuario_id': 42}
    """
    class Meta:
        """
        Definición de las configuraciones del serializador.

        model (Model): El modelo que se serializa, en este caso, Vista.
        fields (list): Los campos del modelo que se incluyen en la serialización, que son 'id', 'fecha', 'contenido_id' y 'usuario_id'.
        """
        model = Vista
        fields = ['id', 'fecha', 'contenido_id', 'usuario_id']