import axios from "axios"
import { setIsError, setIsLoading, setIsOk } from "../Alert"
import { baseUrl } from "../store"
import { setPermisos, setRoles } from "."
import Cookies from "js-cookie"

export const axiosGetRoles = () => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.get(baseUrl + "/roles/")
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setRoles(response.data))
        } else {
            dispatch(setIsError("Ocurrió un error al cargar los roles, error: " + response.status))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message ? error?.response?.data?.message : error?.message))
    }
}
export const axiosModificarRol = (rol, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const {id,...rolCopy}=rol
        const response = await axios.put(baseUrl + "/roles/" + id + "/", rolCopy)
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setIsOk("El rol se modificó correctamene."))
            navigate("/admin/roles")
        } else {
            dispatch(setIsError("Ocurrió un error al modificar el rol, error: " + response.status))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message ? error.response.data.message : error.message))
    }
}
export const axiosGetPermisos = () => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.get(baseUrl + "/permisos")
        dispatch(setIsLoading(false))
        if (response.status === 200) {
            dispatch(setPermisos(response.data))
        } else {
            dispatch(setIsError("Ocurrió un error al cargar los permisos, error: " + response.status))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message ? error?.response?.data?.message : error?.message))
    }
}
export const verificarPermiso = (roles, permisoBuscado) => {
    return roles.some(role =>
        role.permisos.some(permiso => permiso.nombre === permisoBuscado)
    );
}
export const axiosCrearRol = (rol, navigate) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.post(baseUrl + "/roles/", rol)
        dispatch(setIsLoading(false))
        if (response.status === 201) {
            dispatch(setIsOk("El rol se creó correctamente"))
            dispatch(axiosGetRoles())
            navigate("/admin/roles")
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message ? error?.response?.data?.message : error?.message))
    }
}
export const axiosEliminarRol = (id) => async (dispatch) => {
    try {
        dispatch(setIsLoading(true))
        const response = await axios.delete(`${baseUrl}/roles/${id}/`)
        dispatch(setIsLoading(false))
        if (response.status === 204) {
            dispatch(setIsOk("El rol se eliminó correctamente"))
            dispatch(axiosGetRoles())
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message ? error?.response?.data?.message : error?.message))
    }
}