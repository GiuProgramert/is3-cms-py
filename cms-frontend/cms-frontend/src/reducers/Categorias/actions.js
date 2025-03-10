import axios from "axios"
import { setIsError, setIsLoading, setIsOk } from "../Alert"
import { baseUrl } from "../store"
import { setCategorias, setCategoriaSeleccionado } from "."
import Cookies from "js-cookie"

export const axiosGetCategorias=()=>async(dispatch)=>{
    try {
       dispatch(setIsLoading(true))
       const response=await axios.get(baseUrl+"/categorias/") 
       dispatch(setIsLoading(false))
       if(response.status===200){
        dispatch(setCategorias(response.data))
       }else{
        dispatch(setIsError("Ocurrió un problema al cargar las categorias."))
       }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosModficarCategoria=(categoria,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const {id,...newCategoria}=categoria
        const response=await axios.put(baseUrl+"/categorias/"+id+"/",newCategoria)
        dispatch(setIsLoading(false))
        if(response.status===200){
            dispatch(setIsOk("La categoria se modificó correctamente."))
            dispatch(axiosGetCategorias())
            navigate("/admin/categorias")
        }else{
            dispatch(setIsError("Ocurrió un problema al modificar la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message?error?.response?.data?.message:error?.message))
    }
}
export const axiosCrearCategoria=(categoria,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const response=await axios.post(baseUrl+"/categorias/",categoria)
        dispatch(setIsLoading(false))
        if(response.status===201){
            dispatch(setIsOk("La categoria se creó correctamente."))
            navigate("/admin/categorias/")
        }else{
            dispatch(setIsError("Ocurrió un problema al crear la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosCrearSubCategoria=(subcategoria,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const response=await axios.post(baseUrl+"/subcategorias/",subcategoria)
        dispatch(setIsLoading(false))
        if(response.status===201){
            dispatch(setIsOk("La subcategoría se creó correctamente."))
            navigate("/admin/categorias/")
        }else{
            dispatch(setIsError("Ocurrió un problema al crear la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error.response?.data?.message?error.response.data.message:error.message))
    }
}
export const axiosModficarSubcategoria=(subcategoria,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const {id,...subcategoriaCopy}=subcategoria
        const response=await axios.put(baseUrl+"/subcategorias/"+id+"/",subcategoriaCopy)
        dispatch(setIsLoading(false))
        if(response.status===200){
            dispatch(setIsOk("La subcategoria se modificó correctamente."))
            dispatch(axiosGetCategorias())
            navigate("/admin/categorias")
        }else{
            dispatch(setIsError("Ocurrió un problema al modificar la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message?error?.response?.data?.message:error?.message))
    }
}
export const axiosEliminarSubCateg=(id,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))

        const response=await axios.delete(baseUrl+"/subcategorias/"+id+"/")
        dispatch(setIsLoading(false))
        if(response.status===204){
            dispatch(setIsOk("La subcategoria se eliminó correctamente."))
            dispatch(axiosGetCategorias())
            navigate("/admin/categorias")
        }else{
            dispatch(setIsError("Ocurrió un problema al modificar la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message?error?.response?.data?.message:error?.message))
    }
}
export const axiosEliminarCategoria=(id,navigate)=>async(dispatch)=>{
    try {
        dispatch(setIsLoading(true))
        const response=await axios.delete(baseUrl+"/categorias/"+id+"/")
        dispatch(setIsLoading(false))
        if(response.status===204){
            dispatch(setIsOk("La subcategoria se eliminó correctamente."))
            dispatch(axiosGetCategorias())
        }else{
            dispatch(setIsError("Ocurrió un problema al eliminar la categoria."))
        }
    } catch (error) {
        dispatch(setIsError(error?.response?.data?.message?error?.response?.data?.message:error?.message))
    }
}