import './App.css';
import { Routes, Route, useLocation, HashRouter, BrowserRouter, Navigate } from 'react-router-dom';
import LoginPage from './pags/LoginPage';
import { listaUsuarios } from './pags-admin/PaginaUsuarios';
import { useEffect } from 'react';

import AdminLogin from './pags-admin/AdminLogin';

import { AdminContentRoutes, PublicContent } from './components/Content';
import { AdminRoutes } from './components/AdminRoutes';
import RegisterPage from './pags/RegisterPage';
import { SidebarAndTopbar } from './components/SidebarAndTopbar.jsx';
import { SuscriptorRoutes } from './components/SuscriptorRoutes.jsx';
export const baseUrl = "http://localhost:8000"
function App() {
  function SidebarAndTopbarWithRouter(props) {
    let location = useLocation();
    return (
      <SidebarAndTopbar {...props} router={{ location }} />
    )
  }
  return (
    <HashRouter >
      <Routes>
        <Route exact path="/login-page" element={<LoginPage />} />
        <Route path="/" element={<Navigate to="/login-page" />} />
        <Route exact path="/register-page" element={<RegisterPage />} />
        <Route exact path="/admin-login" element={<AdminLogin />} />
        <Route path='/admin/*' element={
          <SidebarAndTopbarWithRouter>
            <AdminRoutes>
              <AdminContentRoutes />
            </AdminRoutes>
          </SidebarAndTopbarWithRouter>
        } />
        <Route path='/public/*' element={
          <SidebarAndTopbarWithRouter>
            <SuscriptorRoutes>
              <PublicContent />
            </SuscriptorRoutes>
          </SidebarAndTopbarWithRouter>
        }
        />
      </Routes>
    </HashRouter >
  );
}

export default App;
