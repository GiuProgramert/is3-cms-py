import React from 'react'
import { Link } from "react-router-dom";

const SidebarAdmin = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-top">
        <ul className="sidebar-menu">
          <li className='item-sidebar'>
            <Link to="/admin/usuarios" className="link-AdminSettings">
              Administrar usuarios
            </Link>
          </li>
          <li className='item-sidebar'>
            <Link to="/admin/roles" className="link-AdminSettings">
              Administrar roles
            </Link>
          </li>
          <li className='item-sidebar'>
            <Link to="/admin/categorias" className="link-AdminSettings">
              Administrar categorias
            </Link>
          </li>
          <li className='item-sidebar'>
            <Link to="/admin/contenido" className="link-AdminSettings">
              Administrar contenido
            </Link>
          </li>
        </ul>
      </div>
      <div className="sidebar-bottom">
        <div className="user-info">
          <p>Nombre-de-Usuario</p>
        </div>
        <button className="logout-button">
          <Link to="/login-page" className="link-AdminSettings">
            Cerrar Sesión
          </Link>
        </button>
      </div>
    </div>
  )
}
export default SidebarAdmin;
