import React, { useEffect } from 'react'
import { verificarPermiso } from '../reducers/Roles/actions'
import { useDispatch, useSelector } from 'react-redux'
import { checkTokenExpiry } from './AdminRoutes'
import { setCerrarSesion } from '../reducers/Sesion'
import { Navigate } from 'react-router-dom'

export const SuscriptorRoutes = ({children}) => {
    const dispatch = useDispatch()
    const { isLogged, rol } = useSelector(state => state.Sesion)

    const hasPermission = isLogged /*&& checkTokenExpiry()*/ && verificarPermiso(rol, "VER_PAGINA_PRINCIPAL")

    useEffect(() => {
        if (!hasPermission) {
            dispatch(setCerrarSesion()) // Cerrar sesión si no tiene permiso
        }
    }, [hasPermission, dispatch]) // Se ejecuta solo cuando 'hasPermission' cambia

    if (hasPermission) {
        return children
    } else {
        return <Navigate to="/login-page" />
    }
}
