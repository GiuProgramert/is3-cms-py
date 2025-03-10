import React from 'react';
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-top">
        <ul className="sidebar-menu">
          <li className='item-sidebar'>Categorías</li>
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
  );
};

export default Sidebar;
