import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Navigate, useLocation } from 'react-router-dom'
import { rutasPermisos, verificarPermisosAdmin } from '../reducers/Sesion/actions'
import Cookies from "js-cookie"
import { setCerrarSesion } from '../reducers/Sesion'
export const checkTokenExpiry = () => {
    const expiryDate = Cookies.get("expires")
    if (expiryDate) {
        if (new Date().getTime() < expiryDate) {
            return true
        } else {
            Cookies.remove("token")
            Cookies.remove("expires")
            return false
        }
    } else {
        return false
    }
};
export const AdminRoutes = ({ children }) => {
    const dispatch=useDispatch()
    const { isLogged, rol } = useSelector(state => state.Sesion)
    const location = useLocation()
    const permisoRequerido = rutasPermisos[location.pathname];
    const tieneRolPermitido = verificarPermisosAdmin(rol)
    const estaAutenticado = isLogged /*&& checkTokenExpiry()*/
    console.log(estaAutenticado)
    useEffect(() => {
        if (!estaAutenticado) {
            dispatch(setCerrarSesion())
        }
    }, [estaAutenticado, dispatch])
    
    if (estaAutenticado) {
        if ((tieneRolPermitido) && (!permisoRequerido || rol.map(rol => rol.permisos.map(permiso => permiso.nombre)).flat().includes(permisoRequerido))) {
            return children
        } else {
            const primeraRutaConPermiso = Object.keys(rutasPermisos).find(ruta => rol.map(rol => rol.permisos.map(permiso => permiso.nombre)).flat().includes(rutasPermisos[ruta]))
            if (primeraRutaConPermiso) {
                const [route] = primeraRutaConPermiso.split(":")
                return <Navigate to={route} />
            }
        }
    } else {
        return <Navigate to={"/login-page"} />
    }
}