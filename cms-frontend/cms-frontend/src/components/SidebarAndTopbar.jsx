import React, { useState } from 'react'
import logo_cms from "../imgs/CMS.png"
import logo_admin_cms from "../imgs/ADM.png"
import avatar from "../imgs/avatar.png"
import { Link, useLocation } from 'react-router-dom'
import Cookies from "js-cookie";
import { useDispatch, useSelector } from 'react-redux'
import { setCerrarSesion } from '../reducers/Sesion'
import { rutasPermisos, verificarPermisosAdmin } from '../reducers/Sesion/actions'

export const SidebarAndTopbar = ({ router, children }) => {
    const { roles } = useSelector(state => { return state.Rol })
    const dispatch = useDispatch()
    const { username, isLogged, rol, profile_pic } = useSelector((state) => state.Sesion)
    const [toggleSidbar, setToggleSidbar] = useState(true)
    const location = useLocation()
    const onCerrarSesion = () => {
        const cookies = Cookies.get();
        Object.keys(cookies).forEach((key) => {
            Cookies.remove(key);
        });
        dispatch(setCerrarSesion())
    }
    const tienePermisoParaRuta = (permiso) => {
        return rol.some(item =>
            item.permisos.some(permisoRol =>
                permisoRol.nombre === permiso
            )
        );
    }
    return (
        <>
            {/* <!-- Wrapper Page --> */}
            <div className="wrapperPage">
                {/* <!-- Sidebar --> */}
                <nav className={toggleSidbar ? "sidebar" : "sidebar collapsed"}>
                    <div className="navContent dropdown-menu-container">

                        {location.pathname.startsWith("/admin") ?
                            <Link to="/admin/cms" className="brand">
                                <img src={logo_admin_cms} className="img-fluid" alt="Logotipo ADMINISTRACION CMS" />
                            </Link>
                            :
                            <Link to="/public/" className="brand">
                                <img src={logo_cms} className="img-fluid" alt="Logotipo CMS" />
                            </Link>
                        }
                        {
                            location.pathname.startsWith("/admin") ?
                                <ul className="sidebar-nav">
                                    {
                                        tienePermisoParaRuta("LISTAR_USUARIO") &&
                                        <li className={(location.pathname.startsWith("/admin/usuarios")) ? "sidebar-item  active" : "sidebar-item "}>
                                            <Link to="/admin/usuarios" className="sidebar-link collapsed" role="button" >
                                                <div className="link-name">
                                                    <span className="link-icon material-icons-outlined"> person </span>
                                                    Administrar usuarios
                                                </div>
                                            </Link>
                                        </li>
                                    }
                                    {
                                        tienePermisoParaRuta("LISTAR_ROL") &&
                                        <li className={(location.pathname.startsWith("/admin/roles")) ? "sidebar-item  active" : "sidebar-item "}>
                                            <Link to="/admin/roles" className="sidebar-link collapsed" role="button" >
                                                <div className="link-name">
                                                    <span className="link-icon material-icons-outlined"> supervisor_account </span>
                                                    Administrar roles
                                                </div>
                                            </Link>
                                        </li>
                                    }
                                    {
                                        tienePermisoParaRuta("LISTAR_CATEGORIA") &&
                                        <li className={(location.pathname.startsWith("/admin/categorias")) ? "sidebar-item  active" : "sidebar-item "}>
                                            <Link to="/admin/categorias" className="sidebar-link collapsed" role="button" >
                                                <div className="link-name">
                                                    <span className="link-icon material-icons-outlined"> category </span>
                                                    Administrar categorias
                                                </div>
                                            </Link>
                                        </li>
                                    }
                                    {
                                        tienePermisoParaRuta("LISTAR_CONTENIDO") &&
                                        <li className={(location.pathname.startsWith("/admin/contenido")) ? "sidebar-item  active" : "sidebar-item "}>
                                            <Link to="/admin/contenido" className="sidebar-link collapsed" role="button" >
                                                <div className="link-name">
                                                    <span className="link-icon material-icons-outlined"> book </span>
                                                    Administrar contenido
                                                </div>
                                            </Link>
                                        </li>
                                    }
                                    {
                                        tienePermisoParaRuta("LISTAR_MONITOREO") &&
                                        <li className={(location.pathname.startsWith("/admin/monitoreo")) ? "sidebar-item  active" : "sidebar-item "}>
                                            <Link to="/admin/monitoreo" className="sidebar-link collapsed" role="button" >
                                                <div className="link-name">
                                                    <span className="link-icon material-icons-outlined"> analytics </span>
                                                    Monitoreo
                                                </div>
                                            </Link>
                                        </li>
                                    }
                                </ul>
                                :
                                <ul className="sidebar-nav">
                                    <li className={(location.pathname.includes("categorias") || location.pathname.includes("feed-categoria") || location.pathname.includes("post") ? "sidebar-item  active" : "sidebar-item")}>
                                        <Link to="/public/categorias" className="sidebar-link collapsed">
                                            <div className="link-name">
                                                <span className="link-icon material-icons-outlined"> category </span>
                                                <span>Categorias</span>
                                            </div>
                                        </Link>
                                    </li>
                                </ul>
                        }
                        {
                            isLogged && username &&
                            <div className="sidebar-footer">
                                <div className="user-dropdown dropup">
                                    <a href={null} role="button" className="profile-item dropdown-toggle" id="dropdownUser1" data-mdb-toggle="dropdown" aria-expanded="false">
                                        <div className="profile-photo">
                                            <img src={profile_pic} className="img-fluid" alt="Foto de perfil" />
                                        </div>
                                        <div className="profile-name">
                                            <span className="name">{username}</span>
                                            {rol?.map(r => <span className='role' key={r.id}>{r.nombre} </span>)}
                                        </div>
                                        <span className="link-icon material-icons-outlined"> settings </span>
                                    </a>
                                    <ul className="dropdown-menu text-small">
                                        <li><Link className="dropdown-item" to={"#"}>Editar perfil</Link></li>
                                    </ul>
                                </div>

                                <Link to={location.pathname.startsWith("/admin") ? "/admin-login" : "/login-page"} className="sidebar-link" onClick={onCerrarSesion}>
                                    <span className="link-icon material-icons-outlined"> logout </span>
                                    Cerrar sesión
                                </Link>
                            </div>
                        }
                    </div>
                </nav>
                {/* <!-- Fin Sidebar --> */}

                {/* <!-- Main Content --> */}
                <div className="main">

                    {/* <!-- Nav Superior --> */}
                    <nav className="navbar navbar-light">

                        <div className="leftside me-auto">
                            <a href={null} className="sidebar-toggle btn" role="button" onClick={() => { setToggleSidbar(!toggleSidbar) }} >
                                <span className="material-icons-outlined"> menu </span>
                            </a>
                        </div>
                        <div className="topbar-links">
                            {
                                !Cookies.get("token") && !username &&
                                <>
                                    <Link to="/login-page" className="btn btn-primary">
                                        Iniciar sesión <span className='material-icons-outlined'> login </span>
                                    </Link>
                                </>
                            }
                            {
                                location.pathname.startsWith("/admin") &&
                                <Link to="/public/" className="btn btn-primary">
                                    Volver a la pagina principal <span className='material-icons-outlined'> arrow_back </span>
                                </Link>

                            }
                            {
                                isLogged && (verificarPermisosAdmin(rol)) && !location.pathname.startsWith("/admin") &&
                                <Link to={"/admin/cms"} className="btn btn-tertiarity">
                                    Admin settings<span className='material-icons-outlined'> settings </span>
                                </Link>
                            }
                        </div>
                    </nav>
                    {/* <!-- Fin Nav Superior --> */}

                    {/* <!-- Dashboard Content --> */}

                    {children}

                    {/* <!-- FinDashboard Content --> */}

                </div>
                {/* <!-- Main Content --> */}

            </div>
            {/* <!-- Fin Wrapper Page --> */}
        </>
    )
}
