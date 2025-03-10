from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class Parametro(models.Model):
    """
    Modelo que representa un parámetro en el sistema.

    Atributos:
        id (AutoField): Campo auto incrementable que identifica de manera única a cada parámetro.
        nombre (CharField): Nombre del parámetro.
        valor (TextField): Valor del parámetro, almacenado como texto (puede ser una imagen en base64).

    Métodos:
        __str__: Retorna una representación en cadena del parámetro.
        ModificarParametro: Permite modificar el nombre y el valor del parámetro.
        listar: Retorna todos los parámetros en la base de datos.
        get_id: Retorna el ID del parámetro.
        get_nombre: Retorna el nombre del parámetro.
        get_valor: Retorna el valor del parámetro.
        set_nombre: Modifica el nombre del parámetro.
        set_valor: Modifica el valor del parámetro.
    """

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    valor = models.TextField()  # Cambiado a TextField para almacenar imagen en base64

    def __str__(self):
        """
        Retorna una representación en cadena del parámetro.

        Returns:
            str: Representación en cadena del nombre y valor del parámetro.
        """
        return f"{self.nombre}: {self.valor}"

    def ModificarParametro(self, nombre, valor):
        """
        Modifica el nombre y el valor del parámetro y guarda los cambios en la base de datos.

        Parámetros:
            nombre (str): Nuevo nombre del parámetro.
            valor (str): Nuevo valor del parámetro.

        Returns:
            None

        Uso:
            >>> parametro = Parametro.objects.get(id=1)
            >>> parametro.ModificarParametro("Nuevo nombre", "Nuevo valor")
        """
        self.nombre = nombre
        self.valor = valor
        self.save()

    @staticmethod
    def listar():
        """
        Retorna todos los parámetros almacenados en la base de datos.

        Returns:
            QuerySet: Conjunto de objetos Parametro en la base de datos.

        Uso:
            >>> parametros = Parametro.listar()
        """
        return Parametro.objects.all()

    # Getters y Setters como antes
    def get_id(self):
        """
        Retorna el ID del parámetro.

        Returns:
            int: ID único del parámetro.
        """
        return self.id

    def get_nombre(self):
        """
        Retorna el nombre del parámetro.

        Returns:
            str: Nombre del parámetro.
        """
        return self.nombre

    def get_valor(self):
        """
        Retorna el valor del parámetro.

        Returns:
            str: Valor del parámetro (puede ser texto o imagen en base64).
        """
        return self.valor

    def set_nombre(self, nombre):
        """
        Modifica el nombre del parámetro.

        Parámetros:
            nombre (str): Nuevo nombre para el parámetro.

        Returns:
            None

        Uso:
            >>> parametro = Parametro.objects.get(id=1)
            >>> parametro.set_nombre("Nombre actualizado")
        """
        self.nombre = nombre

    def set_valor(self, valor):
        """
        Modifica el valor del parámetro.

        Parámetros:
            valor (str): Nuevo valor para el parámetro.

        Returns:
            None

        Uso:
            >>> parametro = Parametro.objects.get(id=1)
            >>> parametro.set_valor("Valor actualizado")
        """
        self.valor = valor

class Categoria(models.Model):
    """
    Modelo que representa una categoría en el sistema.

    Atributos:
        id (AutoField): Campo auto incrementable que identifica de manera única a cada categoría.
        codigo (CharField): Código único que identifica la categoría.
        nombre (CharField): Nombre de la categoría.

    Métodos:
        __str__: Retorna una representación en cadena de la categoría.
        get_id: Retorna el ID de la categoría.
        get_codigo: Retorna el código de la categoría.
        get_nombre: Retorna el nombre de la categoría.
        set_codigo: Modifica el código de la categoría.
        set_nombre: Modifica el nombre de la categoría.
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        Retorna una representación en cadena de la categoría.

        Returns:
            str: Nombre de la categoría.
        """
        return self.nombre

class Subcategoria(models.Model):
    """
    Modelo que representa una subcategoría en el sistema, relacionada con una categoría.

    Atributos:
        nombre (CharField): Nombre de la subcategoría.
        descripcion (TextField): Descripción de la subcategoría.
        categoria (ForeignKey): Relación con el modelo Categoria, estableciendo que cada subcategoría pertenece a una categoría.

    Métodos:
        __str__: Retorna una representación en cadena de la subcategoría.
        get_nombre: Retorna el nombre de la subcategoría.
        get_descripcion: Retorna la descripción de la subcategoría.
        get_categoria: Retorna la categoría asociada a la subcategoría.
        set_nombre: Modifica el nombre de la subcategoría.
        set_descripcion: Modifica la descripción de la subcategoría.
        set_categoria: Modifica la categoría asociada a la subcategoría.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        """
        Retorna una representación en cadena de la subcategoría.

        Returns:
            str: Nombre de la subcategoría.
        """
        return self.nombre

class Permiso(models.Model):
    """
    Modelo que representa un permiso en el sistema.

    Atributos:
        nombre (CharField): Nombre del permiso.

    Métodos:
        __str__: Retorna una representación en cadena del permiso.
        get_nombre: Retorna el nombre del permiso.
        set_nombre: Modifica el nombre del permiso.
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        Retorna una representación en cadena del permiso.

        Returns:
            str: Nombre del permiso.
        """
        return self.nombre

class Rol(models.Model):
    """
    Modelo que representa un rol en el sistema, asociado a varios permisos.

    Atributos:
        nombre (CharField): Nombre del rol.
        permisos (ManyToManyField): Relación con el modelo Permiso, indicando los permisos asociados a este rol.

    Métodos:
        __str__: Retorna una representación en cadena del rol.
        get_nombre: Retorna el nombre del rol.
        get_permisos: Retorna los permisos asociados al rol.
        set_nombre: Modifica el nombre del rol.
        add_permiso: Agrega un permiso al rol.
        remove_permiso: Remueve un permiso del rol.
    """
    nombre = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permiso, related_name='roles')

    def __str__(self):
        """
        Retorna una representación en cadena del rol.

        Returns:
            str: Nombre del rol.
        """
        return self.nombre

class Usuario(models.Model):
    """
    Modelo que representa un usuario en el sistema, asociado a uno o varios roles.

    Atributos:
        username (CharField): Nombre de usuario único para identificar al usuario.
        email (EmailField): Correo electrónico único del usuario.
        roles (ManyToManyField): Relación con el modelo Rol, indicando los roles asociados a este usuario.

    Métodos:
        __str__: Retorna una representación en cadena del nombre de usuario.
        get_username: Retorna el nombre de usuario.
        get_email: Retorna el correo electrónico del usuario.
        get_roles: Retorna los roles asociados al usuario.
        set_username: Modifica el nombre de usuario.
        set_email: Modifica el correo electrónico del usuario.
        add_role: Agrega un rol al usuario.
        remove_role: Remueve un rol del usuario.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    roles = models.ManyToManyField(Rol, related_name='usuarios')

    def __str__(self):
        """
        Retorna una representación en cadena del nombre de usuario.

        Returns:
            str: Nombre de usuario.
        """
        return self.username
    
class Contenido(models.Model):
    ESTADOS = [
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
        ('inactivo', 'Inactivo'),
        ('borrador', 'Borrador'),
        ('rechazado', 'Rechazado'),  # Nuevo estado "Rechazado"
    ]

    titulo = models.CharField(max_length=255)
    resumen = models.TextField()
    cuerpo = models.TextField()
    multimedia = models.TextField(blank=True, null=True)  # Guardar multimedia en base64
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    subcategoria = models.ForeignKey(Subcategoria, related_name='contenidos', on_delete=models.CASCADE,null=True)
    comentarios = models.TextField(blank=True, null=True)  # Comentarios del publicador
    fecha = models.DateField(auto_now_add=True,null=True)
    autor = models.ForeignKey(Usuario, related_name='contenidos', on_delete=models.CASCADE,null=True)  # Nuevo campo
    def __str__(self):
        return self.titulo

    def aprobar(self):
        self.estado = 'aprobado'
        self.save()

    def rechazar(self, comentarios):
        self.estado = 'rechazado'
        self.comentarios = comentarios
        self.save()

# TODO: Implementar comentarios
from django.db import models

class Comentario(models.Model):
    """
    Modelo para almacenar los comentarios asociados a un contenido específico en la aplicación.

    Atributos:
        contenido (ForeignKey): Relación con el modelo `Contenido` para identificar a qué contenido pertenece el comentario.
            Parámetro de entrada: un objeto `Contenido`.
        texto (TextField): Texto del comentario.
            Parámetro de entrada: cadena de texto.
        usuario (ForeignKey): Relación con el modelo `Usuario` para identificar al autor del comentario.
            Parámetro de entrada: un objeto `Usuario` o `None` para comentarios anónimos.
        reply_to (ForeignKey): Relación autorreferencial al modelo `Comentario` para identificar si el comentario es una respuesta a otro comentario.
            Parámetro de entrada: un objeto `Comentario` o `None` si no es una respuesta.
        avatarUrl (URLField): URL opcional que apunta al avatar del usuario.
            Parámetro de entrada: cadena de texto que representa una URL o `None` si no se proporciona avatar.

    Métodos:
        __str__(): Devuelve una representación en cadena del comentario.

    Uso:
        >>> contenido_obj = Contenido.objects.get(id=1)
        >>> usuario_obj = Usuario.objects.get(id=1)
        >>> comentario = Comentario(
        ...     contenido=contenido_obj,
        ...     texto="Este es un comentario de prueba.",
        ...     usuario=usuario_obj,
        ...     avatarUrl="https://example.com/avatar.jpg"
        ... )
        >>> print(comentario)
        Usuario: Este es un comentario...
    """
    contenido = models.ForeignKey('Contenido', related_name='lista_comentarios', on_delete=models.CASCADE)
    texto = models.TextField()
    usuario = models.ForeignKey('Usuario', related_name='comentarios', on_delete=models.SET_NULL, null=True, blank=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # Relación autorreferencial
    avatarUrl = models.URLField(max_length=500, null=True, blank=True)  # Campo para la URL del avatar
    def __str__(self):
        """
        Devuelve una representación en cadena del comentario.

        Parámetros:
            Ninguno.

        Retorno:
            str: Representación en cadena del comentario, incluyendo el nombre del usuario (o 'Anon' si es anónimo) 
            y los primeros 20 caracteres del comentario.

        Ejemplo:
            >>> comentario = Comentario(
            ...     usuario=usuario_obj, texto="Este es un comentario de prueba"
            ... )
            >>> print(str(comentario))
            'Usuario: Este es un comentario...'
        """
        return f"{self.usuario.username if self.usuario else 'Anon'}: {self.texto[:20]}"


# TODO: implementar historial de cambios
class Historial(models.Model):
    """
    Modelo que representa el historial de cambios de un contenido en el sistema.

    Atributos:
    - id: Campo auto incrementable que identifica de manera única a cada entrada del historial.
    - contenido: Relación con el modelo Contenido que indica a qué contenido se refiere el historial.
    - fecha_modificacion: Fecha y hora en que se realizó el cambio.
    - estado: Estado del contenido
    - comentario: Comentario opcional sobre el cambio realizado.
    - usuario: Relación con el modelo User que indica quién realizó el cambio.

    Métodos:
    - __str__: Retorna una representación en cadena del historial.
    """
    contenido = models.ForeignKey('Contenido', on_delete=models.CASCADE, related_name='historiales')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    comentario = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=Contenido.ESTADOS,default='borrador')
    usuario = models.ForeignKey('Usuario', related_name='historiales', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del historial de cambios, mostrando el título del contenido
        y la fecha de modificación.

        Retorno:
            str: Representación en cadena del historial de cambios.

        Ejemplo:
            >>> historial = HistorialCambio(contenido=contenido_obj, fecha_modificacion=fecha_obj)
            >>> str(historial)
            'Historial de Título del contenido - 2024-11-06 10:15:00'
        """
        return f"Historial de {self.contenido.titulo} - {self.fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
    
# Implementación de likes
class Like(models.Model):
    """
    Modelo que representa un "like" en el sistema.

    Este modelo se utiliza para almacenar los "likes" que los usuarios pueden dar a los contenidos. 
    Cada "like" está asociado con un contenido y un usuario específico, y almacena la fecha y hora 
    en que se realizó el "like".

    Atributos:
        contenido (ForeignKey): Relación con el modelo 'Contenido', indicando a qué contenido 
                                se le ha dado el "like".
        usuario (ForeignKey): Relación con el modelo 'Usuario', indicando quién ha dado el "like".
        fecha (DateTimeField): Fecha y hora en que se dio el "like", establecida automáticamente al 
                               momento de la creación.

    Métodos:
        __str__(): Retorna una representación en cadena del "like", mostrando el nombre del usuario, 
                   el título del contenido y la fecha del "like".

    Ejemplo:
        >>> like = Like(contenido=contenido_obj, usuario=usuario_obj)
        >>> like.save()
    """
    contenido = models.ForeignKey('Contenido', related_name='likes', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', related_name='likes', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('contenido', 'usuario')  # Para asegurar que un usuario no pueda dar "like" varias veces al mismo contenido

    def __str__(self):
        """
        Retorna una representación en cadena del "like", mostrando el nombre del usuario, 
        el título del contenido y la fecha en la que se dio el "like".

        Retorno:
            str: Representación en cadena del "like".

        Ejemplo:
            >>> like = Like(contenido=contenido_obj, usuario=usuario_obj)
            >>> str(like)
            'usuario1 liked Título del contenido on 2024-11-06 10:15:00'
        """
        return f"{self.usuario.username} liked {self.contenido.titulo} on {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"

class Articulo(models.Model):
    """
    Modelo `Articulo`
    ------------------
    Este modelo representa un artículo asociado a un contenido específico, incluyendo información sobre su estado y su historial de modificaciones.

    Campos:
    - titulo (`CharField`): Almacena el título del artículo, con un límite máximo de 200 caracteres.
    - contenido (`ForeignKey` a `Contenido`): Relación con el modelo `Contenido`, que indica el contenido al que pertenece el artículo. La opción `on_delete=models.CASCADE` asegura que si el contenido asociado se elimina, también se eliminará el artículo.
    - estado (`CharField`): Representa el estado del artículo, con un límite máximo de 20 caracteres. Este campo utiliza las opciones definidas en `Contenido.ESTADOS`, lo que garantiza que el estado del artículo se mantenga dentro de un conjunto específico de valores válidos.
    - fecha_modificacion (`DateTimeField`): Almacena la fecha y hora de la última modificación del artículo. Se establece automáticamente a la fecha y hora actual cada vez que se guarda el artículo.

    Métodos:
    - contar_articulos_aprobados (método estático): Este método cuenta la cantidad de artículos cuyo estado es "aprobado" dentro de un rango de fechas específico. Toma como parámetros `fecha_inicio` y `fecha_fin`, que deben ser objetos de fecha.

    - Parámetros:
    - `fecha_inicio`: Fecha de inicio del rango.
    - `fecha_fin`: Fecha de fin del rango.

    - Retorno: 
    Devuelve un entero que representa la cantidad de artículos aprobados en el rango de fechas especificado.

    Uso:
    Este modelo es útil para la gestión de artículos en un sistema de contenidos, permitiendo un seguimiento del estado de cada artículo y su relación con el contenido correspondiente. La función para contar artículos aprobados facilita la generación de informes y análisis basados en estados de contenido.

    """
    titulo = models.CharField(max_length=200)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=Contenido.ESTADOS)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def contar_articulos_aprobados(fecha_inicio, fecha_fin):
        """
        Cuenta la cantidad de artículos aprobados en un rango de fechas.

        Este método estático permite obtener el número de artículos cuyo estado es 
        "aprobado" y cuya fecha de creación se encuentra dentro del rango proporcionado.

        Parámetros:
            fecha_inicio (datetime.date): La fecha de inicio del rango de fechas.
            fecha_fin (datetime.date): La fecha de fin del rango de fechas.

        Retorno:
            int: El número de artículos aprobados dentro del rango de fechas.

        Ejemplo:
            >>> fecha_inicio = datetime.date(2023, 1, 1)
            >>> fecha_fin = datetime.date(2023, 12, 31)
            >>> Contenido.contar_articulos_aprobados(fecha_inicio, fecha_fin)
            15
        """
        return Contenido.objects.filter(
            estado='aprobado',
            fecha__range=(fecha_inicio, fecha_fin)
        ).count()
    
    
class Vista(models.Model):
    """
    Modelo que representa una vista de contenido por un usuario en el sistema.

    Atributos:
        fecha (DateTimeField): Fecha y hora en que se registró la vista, se establece automáticamente al momento de crear la vista.
        contenido_id (BigIntegerField): Identificador único del contenido que fue visto.
        usuario_id (BigIntegerField): Identificador único del usuario que vio el contenido.

    Métodos:
        __str__: Retorna una representación en cadena de la vista.
        get_fecha: Retorna la fecha de la vista.
        get_contenido_id: Retorna el identificador del contenido visto.
        get_usuario_id: Retorna el identificador del usuario que vio el contenido.
    """
    fecha = models.DateTimeField(auto_now_add=True)
    contenido_id = models.BigIntegerField()
    usuario_id = models.BigIntegerField()

    class Meta:
        """
        Definición de las restricciones y configuraciones para el modelo.

        unique_together (tuple): Asegura que no haya duplicados de la misma vista para el mismo contenido y usuario.
        """
        unique_together = ('contenido_id', 'usuario_id')
