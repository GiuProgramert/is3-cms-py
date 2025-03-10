import React from 'react'
import {  Route, Routes } from 'react-router-dom'
import PaginaPrincipal from '../pags/PaginaPrincipal'
import AdminSettings from '../pags-admin/AdminSettings'
import PaginaCategorias from '../pags-admin/PaginaCategorias'
import PaginaContenidos from '../pags-admin/PaginaContenidos'
import { PaginaUsuarios } from '../pags-admin/PaginaUsuarios'
import { PaginaUsuariosEditar } from '../pags-admin/PaginaUsuariosEditar'
import { PaginaUsuariosCrear } from '../pags-admin/PaginaUsuariosCrear'
import PostPage from '../pags/PostPage'
import PaginaCrearCategoria from '../pags-admin/PaginaCrearCategoria'
import Categorias from '../pags/Categorias'
import { PaginaRoles } from '../pags-admin/PaginaRoles'
import { PaginaRolesEditar } from '../pags-admin/PaginaRolesEditar'
import HomeCategoriaMarcada from '../pags/HomeCategoriaMarcada'
import PaginaEditarContenido from '../pags-admin/PaginaEditarContenido'
import PaginaEditarCategorias from '../pags-admin/PaginaEditarCategorias'
import PaginaCrearContenido from '../pags-admin/PaginaCrearContenido'
import PaginaBorradores from '../pags-admin/PaginaBorradores'
import { PaginaPublicador } from '../pags-admin/PaginaPublicador'
import { PaginaRolesCrear } from '../pags-admin/PaginaRolesCrear'
import { Monitoreo } from '../pags-admin/Monitoreo'
export const PublicContent = () => {
  return (
    <Routes>
      <Route path="/" element={<PaginaPrincipal />} />
      <Route exact path="/categorias" element={<Categorias />} />
      <Route path="/feed-categoria/:categoryId" element={<HomeCategoriaMarcada />} />
      <Route path="/post/:categoryId/:postId" element={<PostPage />} />
    </Routes>
  )
}
export const AdminContentRoutes = () => {
  return (
<Routes>
      <Route path="/cms" element={<AdminSettings/>} />
      <Route path="/feed-categoria/:categoryId" element={<HomeCategoriaMarcada />} />
      <Route path="/roles" element={<PaginaRoles/>} />
      <Route path="/roles/editar" element={<PaginaRolesEditar/>} />
      <Route path="/categorias" element={<PaginaCategorias/>} />
      <Route path="/contenido" element={<PaginaContenidos/>} />
      <Route path="/usuarios" element={<PaginaUsuarios/>}/>
      <Route path="/usuarios/editar" element={<PaginaUsuariosEditar/>}/>
      <Route path="/usuarios/crear" element={<PaginaUsuariosCrear/>}/>
      <Route path="/contenido/crear" element={<PaginaCrearContenido />} />
      <Route path="/categorias/crear" element={<PaginaCrearCategoria />} />
      <Route path="/contenido/editar" element={<PaginaEditarContenido />} />
      <Route path="/categorias/editar" element={<PaginaEditarCategorias />} />
      <Route path="/borradores" element={<PaginaBorradores />} />
      <Route path="/contenido/publicador" element={<PaginaPublicador />} />
      <Route path="/roles/nuevo" element={<PaginaRolesCrear/>} />
      <Route path='/publicador' element={<PaginaPublicador/>}/>
      <Route path='/monitoreo' element={<Monitoreo/>}/>
</Routes>
)
}
