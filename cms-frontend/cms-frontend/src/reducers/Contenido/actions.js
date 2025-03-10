import axios from "axios"
import { setIsError, setIsLoading, setIsOk } from "../Alert"
import { baseUrl } from "../store"
import { setContenido, setContenidoMasLikes, setContenidoSeleccionado, setContenidosMasVistos, setContenidosTop5, setEstados, setHistorial } from "."
import Cookies from "js-cookie"


export const axiosGetContenido = () => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.get(baseUrl + "/contenido/")
        dispatch(setIsLoading(false))
        if (response.status === 200) {

            dispatch(setContenido(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
const historialModificacionContenido=(contenidoAnterior, contenidoActual)=>{

    let mensaje =contenidoAnterior.estado === "en_revision" ? "El contenido se envió a revisión. " : "El contenido se guardó en borrador. "
    if(contenidoAnterior.titulo !== contenidoActual.titulo) {
        mensaje+="Se modificó el título del contenido. " 
    }
    if(contenidoAnterior.resumen !== contenidoActual.resumen) {
        mensaje+="Se modificó el resumen del contenido. " 
    }
    if(contenidoAnterior.cuerpo !== contenidoActual.cuerpo) {
        mensaje+="Se modificó el cuerpo del contenido. " 
    }
    return mensaje;
}
export const axiosModficarContenido = (contenidoActual,contenido, autor, usuarios,roles, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const { id, ...newContenido } = contenido
        const response = await axios.put(baseUrl + "/contenido/" + id + "/", newContenido)
        dispatch(setIsLoading(false))
        if (response.status === 200) {

            const rolPublicador = roles.find(rol => rol.nombre === "publicador");
            const publicadores = usuarios?.filter(user => user.rol === rolPublicador?.id);
            publicadores?.forEach((publicador) => {
                dispatch(axiosEnviarNotificacion(
                    publicador.email,
                    "Un nuevo contenido acaba de ser revisado para publicar",
                    "Favor ingrese a la pagina para publicar el contenido: " + window.location.origin
                ))
            })

            let mensajeHistorial=historialModificacionContenido(contenidoActual,response.data)
            dispatch(axiosAgregarHistorial(mensajeHistorial, autor, contenido.id, contenido.estado))
            dispatch(setIsOk("El contenido se modificó correctamene."))
            dispatch(axiosGetContenido())
            navigate("/admin/contenido")
        } else {
            dispatch(setIsError("Ocurrió un problema al modificar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response.data.message ? error.response.data.message : error.message))
    }
}
export const axiosCrearContenido = (contenido, roles,autor, usuarios, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))

        const response = await axios.post(baseUrl + "/contenido/", contenido,roles)
        dispatch(setIsLoading(false))
        if (response.status === 201) {
            dispatch(setIsOk("El contenido se creó correctamente."))
            dispatch(axiosGetContenido())
            const rolEditor = roles.find(rol => rol.nombre === "editor");
            const editores = usuarios?.filter(user => user.roles.includes(rolEditor?.id));
            editores?.forEach((editor) => {
                dispatch(axiosEnviarNotificacion(
                    editor.email,
                    "Un nuevo contenido acaba de ser creado para ser revisado",
                    "Favor ingrese a la pagina para revisar el contenido: " + window.location.origin
                ))
            })
            dispatch(axiosAgregarHistorial("Se creó el contenido", autor, response.data.id,"en_revision"))
            navigate("/admin/contenido")
        } else {
            dispatch(setIsError("Ocurrió un problema al crear el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosFiltrarContenido = (filtro) => async (dispatch) => {
    let url = baseUrl + "/contenido/busqueda/";
    if (filtro.estado) {
        if (url === baseUrl + "/contenido/busqueda/") {
            url = url + "?estado=" + filtro.estado
        } else {
            url = url + "&estado=" + filtro.estado
        }
    }
    if (filtro.autor) {
        if (url === baseUrl + "/contenido/busqueda/") {
            url = url + "?autor=" + filtro.autor
        } else {
            url = url + "&autor=" + filtro.autor
        }
    }
    if (filtro.categoria_id) {
        if (url === baseUrl + "/contenido/busqueda/") {
            url = url + "?categoria_id=" + filtro.categoria_id
        } else {
            url = url + "&categoria_id=" + filtro.categoria_id
        }
    }
    if (filtro.fecha) {
        if (url === baseUrl + "/contenido/busqueda/") {
            url = url + "?fecha=" + filtro.fecha
        } else {
            url = url + "&fecha=" + filtro.fecha
        }
    }
    if (filtro.subcategoria_id) {
        if (url === baseUrl + "/contenido/busqueda/") {
            url = url + "?subcategoria_id=" + filtro.subcategoria_id
        } else {
            url = url + "&subcategoria_id=" + filtro.subcategoria_id
        }
    }
    try {
        dispatch(setIsLoading(true))
        const response = await axios.get(url)
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setContenido(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al filtrar contenidos"))
        }

    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response?.data?.message : error.message))
    }

}
export const axiosEnviarNotificacion = (email, asunto, content) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.post(baseUrl + "/send-email/",
            {
                "to_email": email,
                "subject": asunto,
                "content": content
            }, {
            headers: {
                'Authorization': `Bearer ${Cookies.get("token")}`
            }
        })
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setIsOk("Se envio la notificación."))
        } else {
            dispatch(setIsError("Ocurrió un error al notificar."))
        }
    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error?.message)
    }
}
export const axiosAgregarHistorial = (comentario, usuarioId, contenidoId,estado) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.post(baseUrl + "/historial/",
            {
                "comentario": comentario,
                "usuario": usuarioId,
                "contenido": contenidoId,
                "estado":estado
            })
        dispatch(setIsLoading(false))
        if (response.status === 201) {
            dispatch(setIsOk("Se agregó al historial del contenido."))
        } else {
            dispatch(setIsError("Ocurrió un error al agregar al historial del contenido."))
        }
    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error?.message)
    }
}
export const axiosPublicarRechazar = (contenido, autor, estado, motivo, usuarios, roles,navigate) => async (dispatch) => {
    try {

        const { id, ...newContenido } = contenido
        const response = await axios.put(baseUrl + "/contenido/" + id + "/aprobar_rechazar/", {
            titulo: contenido?.titulo,
            estado: estado,
            comentarios: motivo
        })
        if (response.status === 200) {
            if (estado === "rechazado") {
                const rolEditor = roles.find(rol => rol.nombre === "editor");
                const editores = usuarios?.filter(user => user.roles.includes(rolEditor?.id));
                editores?.forEach((editor) => {
                    dispatch(axiosEnviarNotificacion(
                        editor.email,
                        "Un contenido acaba de ser rechazado",
                        "Favor ingrese a la pagina para revisar el contenido: " + window.location.origin
                    ))
                })
                dispatch(axiosAgregarHistorial("Se rechazó el contenido porque: " + motivo, autor, contenido.id,estado))
                dispatch(setIsOk("El contenido fue rechazado correctamente."))
            } else {
                const email = usuarios.find((user) => contenido.autor === user.id)?.email
                dispatch(axiosEnviarNotificacion(
                    email,
                    "Tu contenido acaba de ser publicado",
                    "Favor ingrese a la pagina para ver el contenido: " + window.location.origin
                ))
                dispatch(axiosAgregarHistorial("El contenido se publicó ", autor, contenido.id,estado))
                dispatch(setIsOk("El contenido fue publicado correctamente."))
            }
            navigate("/admin/cms")
        } else {
            dispatch(setIsError("Ocurrió un error al realizar la acción."))
        }

    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error.message)
    }
}
export const axiosInactivar = (contenido, autor, estado, motivo, usuarios, navigate) => async (dispatch) => {
    try {

        const { id, ...newContenido } = contenido
        const response = await axios.put(baseUrl + "/contenido/" + id + "/inactivar/", contenido)
        if (response.status === 200) {

            const email = usuarios.find((user) => contenido.autor === user.id)?.email
            dispatch(axiosEnviarNotificacion(
                email,
                "Tu contenido acaba de ser inactivado",
                "Favor ingrese a la pagina para ver el estado del contenido: " + window.location.origin
            ))
            dispatch(axiosAgregarHistorial("El contenido se inactivó ", autor, contenido.id,"inactivo"))
            dispatch(setIsOk("El contenido fue inactivado correctamente."))
            navigate("/admin/cms")

        }

    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error.message)
    }
}
export const axiosGetHistorial = (id) => async (dispatch) => {
    try {
        const response = await axios.get(baseUrl + "/historiales/" + id, {
            headers: `Bearer ${Cookies.get("token")}`
        })
        if (response.status === 200) {
            dispatch(setHistorial(response.data))
        } else {
            dispatch(setIsError("Ocurrio un error al traer el historial."))
        }
    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error.message)
    }
}
export const axiosGetContenidoById=(id)=>async(dispatch)=>{
    try {
        const response = await axios.get(baseUrl + "/contenido/" + id)
        if (response.status === 200) {
            dispatch(setContenidoSeleccionado(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosComentarContenido = (comentario, contenidoId, usuarioId, avatarUrl,comentarioId) => async (dispatch) => {
    try {
        const response = await axios.post(baseUrl + "/contenido/"+contenidoId+"/comentarios/", {
            "avatarUrl": avatarUrl,
            "texto": comentario,
            "contenido": contenidoId,
            "usuario": usuarioId,
            "reply_to": comentarioId
        })
        if (response.status === 201) {
            dispatch(setIsOk("El comentario se agregó correctamente."))
            dispatch(axiosGetContenidoById(contenidoId))
        } else {
            dispatch(setIsError("Ocurrió un error al agregar el comentario."))
        }
    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error.message)
    }
}
export const axiosEliminarComentario = (comentarioId, contenidoId) => async (dispatch) => {
    try {
        const response = await axios.delete(baseUrl + "/contenido/"+contenidoId+"/comentarios/" + comentarioId)
        if (response.status === 204) {
            dispatch(setIsOk("El comentario se eliminó correctamente."))
            dispatch(axiosGetContenidoById(contenidoId))    
        }
    }

    catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data.message : error.message)
    }   
}
export const axiosEditarComentario = (comentarioId, contenidoId, comentario,avatarUrl,usuarioId,replyTo) => async (dispatch) => {
    try {
        const response = await axios.put(baseUrl + "/contenido/"+contenidoId+"/comentarios/" + comentarioId+"/", {
            "texto": comentario,
            "avatarUrl": avatarUrl,
            "contenido": contenidoId,
            "usuario": usuarioId,
            "reply_to": replyTo
          })
        if (response.status === 200) {
            dispatch(setIsOk("El comentario se editó correctamente."))
            dispatch(axiosGetContenidoById(contenidoId))
        } else {
            dispatch(setIsError("Ocurrió un error al editar el comentario."))
        }
    } catch (error) {
        dispatch(error.response?.data?.message ? error.response?.data?.message : error.message)
    }
}
export const axiosContarEstados = (fechainicio,fechafin) => async (dispatch) => {
    try {
        const response = await axios.get(`${baseUrl}/articulos/contar-estados/${fechainicio}/${fechafin}`)
        if (response.status === 200) {
            const {total,...newData}=response.data
            dispatch(setEstados(newData))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosContenidosConMasLikes = () => async (dispatch) => { 
    try {
        const response = await axios.get(`${baseUrl}/articulos/mas-likes/`)
        if (response.status === 200) {
            dispatch(setContenidoMasLikes(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosGetContenidosTop5 = () => async (dispatch) => {
    try {
        const response = await axios.get(`${baseUrl}/vistas/top-5/`)
        if (response.status === 200) {
            dispatch(setContenidosTop5(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosGetContenidosMasVistos=(fechainicio,fechafin)=>async(dispatch)=>{ 
    try {
        const response = await axios.get(`${baseUrl}/contenidos_mas_vistos/${fechainicio}/${fechafin}/`)
        if (response.status === 200) {
            dispatch(setContenidosMasVistos(response.data))
        } else {
            dispatch(setIsError("Ocurrió un problema al cargar el contenido."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}