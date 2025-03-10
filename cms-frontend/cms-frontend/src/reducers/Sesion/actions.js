import axios from "axios"
import { setIsError, setIsLoading } from "../Alert"
import { baseUrl } from "../store"
import Cookies from "js-cookie"
import { setSesion } from "."
import { axiosGetRoles } from "../Roles/actions"

// export const axiosGetToken=(credenciales,navigate)=>async(dispatch)=>{
//     try {
//         dispatch(setIsLoading(true))
//         const response=await axios.post(baseUrl+"/token",credenciales)
//         dispatch(setIsLoading(false))
//         if(response.status===200){
//             Cookies.set("token",response.data.token)
//             dispatch(setSesion(credenciales))
//             navigate("/")
//         }else{
//             dispatch(setIsError("Ocurrió un problema al intentar generar el token."))
//         }
//     } catch (error) {
//         dispatch(setIsError(error?.response?.data?.message?error?.response?.data?.message:error?.message))
//     }
// }
export const axiosGetToken = async () => {
    const { data, status } = await axios.get(baseUrl + "token/")
    console.log(data)
    if (status === 200) {
        return data.csrf_token;
    }
}
export const permisosEnum = {
    LISTAR_USUARIO: "LISTAR_USUARIO",
    LISTAR_CATEGORIA:"LISTAR_CATEGORIA",
    LISTAR_CONTENIDO:"LISTAR_CONTENIDO",
    LISTAR_ROL:"LISTAR_ROL",
    LISTAR_PERMISO:"LISTAR_PERMISO",
    CREAR_USUARIO: 'CREAR_USUARIO',
    EDITAR_USUARIO: 'EDITAR_USUARIO',
    EDITAR_ROL: 'EDITAR_ROL',
    CREAR_ROL: 'CREAR_ROL',
    EDITAR_CATEGORIA: 'EDITAR_CATEGORIA',
    CREAR_CATEGORIA: 'CREAR_CATEGORIA',
    EDITAR_CONTENIDO: 'EDITAR_CONTENIDO',
    CREAR_CONTENIDO: 'CREAR_CONTENIDO',
    PUBLICAR_CONTENIDO: 'PUBLICAR_CONTENIDO',
    RECHAZAR_CONTENIDO: 'RECHAZAR_CONTENIDO',
    ELIMINAR_USUARIO: 'ELIMINAR_USUARIO',
    ELIMINAR_ROL: 'ELIMINAR_ROL',
    ELIMINAR_CATEGORIA: 'ELIMINAR_CATEGORIA',
    INACTIVAR_CONTENIDO: 'INACTIVAR_CONTENIDO'
  };
export const rutasPermisos={
"/admin/usuarios":"LISTAR_USUARIO",
"/admin/usuarios/editar":"EDITAR_USUARIO",
"/admin/usuarios/crear":"CREAR_USUARIO",
"/admin/roles":"LISTAR_ROL",
"/admin/roles/editar":"EDITAR_ROL",
"/admin/roles/nuevo":"CREAR_ROL",
"/admin/categorias":"LISTAR_CATEGORIA",
"/admin/categorias/editar":"EDITAR_CATEGORIA",
"/admin/categorias/crear":"CREAR_CATEGORIA",
"/admin/contenido":"LISTAR_CONTENIDO",
"/admin/contenido/editar":"EDITAR_CONTENIDO",
"/admin/contenido/crear":"CREAR_CONTENIDO",
"/admin/contenido/publicador":"PUBLICAR_CONTENIDO",
"/admin/borradores":"RECHAZAR_CONTENIDO",
"/admin/publicador":"INACTIVAR_CONTENIDO",
"/admin/cms":"LISTAR_CONTENIDO",
"/admin/monitoreo":"LISTAR_MONITOREO",
}
export const verificarPermisosAdmin=(roles)=>{

  const permisosEnumValues = Object.values(permisosEnum);

  return roles.some(rol =>
    rol.permisos.some(permiso =>
      permisosEnumValues.includes(permiso.nombre)
    )
  );
}
export const axiosIniciarSesion = (username, email, profile_pic, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))

        const response = await axios.get(`${baseUrl}/usuarios/email/${email}/`)
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setSesion({
                username:response.data.username,
                rol:response.data.roles,
                id:response.data.id,
                email:email,
                profile_pic:profile_pic
            }))
            const tieneRolAdmin=verificarPermisosAdmin(response.data.roles)
            navigate(tieneRolAdmin?"/admin/cms":"/public/")
        } else {
            dispatch(setIsError("Ocurrió un problema al intentar iniciar sesion."))
        }
    } catch (error) {
        if(error?.response?.status===404){
            dispatch(setIsError(error.response?.data?.detail))
        }else{
            dispatch(setIsError(error.response?.data?.message ? error.response?.data?.message : error?.message))
        }
    }
}
export const axiosIniciarSesionAdm = (credenciales, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const responseToken = await axios.get(baseUrl + "/token/", {
            withCredentials: true
        })

        if (responseToken.status === 200) {
            const response = await axios.post(baseUrl + "/login/", credenciales, {
                "headers": {
                    'X-CSRFToken': responseToken.data.csrf_token
                },
                withCredentials: true
            })
            dispatch(setIsLoading(false))
            if (response.status === 200) {
                Cookies.set("token", response.data.token.access)
                Cookies.set("refresh", response.data.token.refresh)
                if (response.data.usuario.rol === 1 || response.data.usuario.rol === 2 || response.data.usuario.rol === 3 || response.data.usuario.rol === 4) {
                    console.log({ ...credenciales, id: response.data.usuario.id, rol: response.data.usuario.rol })
                    dispatch(setSesion({ ...credenciales, id: response.data.usuario.id, rol: response.data.usuario.rol }))
                    dispatch(axiosGetRoles())
                    navigate("/admin/cms")
                } else {
                    dispatch(setIsError("No tiene los permisos para ingresar al panel de administración."))
                }

            } else {
                dispatch(setIsError("Ocurrió un problema al intentar iniciar sesion."))
            }
        }

    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response?.data?.message : error.message))
    }
}
export const axiosRegistrarUsuario = (registro, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const token = axiosGetToken()
        const response = await axios.post(baseUrl + "/usuarios/registro/", registro, {
            headers: `Bearer ${Cookies.get("token")}`
        })
        dispatch(setIsLoading(false))
        if (response.status === 201) {
            dispatch(axiosIniciarSesion({username:registro.username,password:registro.password},navigate))
            navigate("/")
        } else {
            dispatch(setIsError("Ocurrió un problema al intentar registrarse."))
        }
    } catch (error) {
        dispatch(setIsError(error.response.data.message ? error.response.data.message : error.message))
    }
}