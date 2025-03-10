import axios from "axios"
import { setIsError, setIsLoading, setIsOk } from "../Alert"
import { baseUrl } from "../store"
import { setUsuarios } from "."
import Cookies from "js-cookie"

export const axiosGetUsuarios=()=>async(dispatch)=>{
    try {
       dispatch(setIsLoading(true))
       const response=await axios.get(baseUrl+"/usuarios/") 
       dispatch(setIsLoading(false))
       if(response.status===200){
        dispatch(setUsuarios(response.data))
       }else{
        dispatch(setIsError("Ocurrió un problema al cargar los usuarios."))
       }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosModficarUsuario=(usuario,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const {id,...newUsuario}=usuario
        const response=await axios.put(baseUrl+"/usuarios/"+id+"/",newUsuario)
        dispatch(setIsLoading(false))
        if(response.status===200){
            dispatch(setIsOk("El usuario se modificó correctamene."))
            navigate("/admin/usuarios")
        }else{
            dispatch(setIsError("Ocurrió un problema al modificar el usuario."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosCrearUsuario=(usuario,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const  response=await axios.post(baseUrl+"/usuarios/",usuario)
        dispatch(setIsLoading(false))
        if(response.status===201){
            dispatch(setIsOk("El usuario se creó correctamene."))
            navigate("/admin/usuarios")
        }else{
            dispatch(setIsError("Ocurrió un problema al crear el usuario."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosEliminarUsuario=(usuarioId)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const response=await axios.delete(baseUrl+"/usuarios/"+usuarioId+"/")
        dispatch(setIsLoading(false))
        if(response.status===204){
            dispatch(setIsOk("El usuario se eliminó correctamente."))
            dispatch(axiosGetUsuarios())
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}