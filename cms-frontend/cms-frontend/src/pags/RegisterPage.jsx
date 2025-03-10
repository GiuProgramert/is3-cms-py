import React, { useState } from "react";
import {useNavigate, Link } from "react-router-dom";
import loginbg from "../imgs/registerimg.jpg"
import logo_cms from "../imgs/mayuscula.svg"
import {useDispatch, useSelector} from "react-redux"
import {axiosIniciarSesion } from "../reducers/Sesion/actions";
import Cookies from "js-cookie";
import { Alert } from "../components/Alert";
import { axiosCrearUsuario } from '../reducers/Usuarios/actions'
import { permisos, roles } from '../pags-admin/PaginaUsuariosEditar'

const  RegisterPage=()=> {
  const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const permiso = permisos.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const { roles } = useSelector(state => state.Rol)
    const {  rol } = useSelector(state => state.Sesion)
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const [usuarioForm, setUsuarioForm] = useState({
        nombre:"",
        username:"",
        email:"",
        password:"",
        confirmPassword:""
    })
    
    const dispatch = useDispatch()
    const navigate = useNavigate()
    // const permiso = usuarioForm.ro.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const handleCancelar = () => {
        setEditar(false)
        localStorage.removeItem('usuario')
    }
    const handleChange = ({ target }) => {
        setUsuarioForm({
            ...usuarioForm,
            [target.name]: target.value
        })
    }
    const validate = () => {
        let validateStatus = true;
        let errors = {}
        if (!usuarioForm.nombre) {
            validateStatus = false
            errors["nombre"] = "Nombre es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!usuarioForm.username) {
            validateStatus = false
            errors["username"] = "Username es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!usuarioForm.email) {
            validateStatus = false
            errors["email"] = "Email es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        
        if (!usuarioForm.password) {
            validateStatus = false
            errors["password"] = "Contraseña es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!usuarioForm.confirmPassword) {
            validateStatus = false
            errors["confirmPassword"] = "Confirmar contraseña es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (usuarioForm.password && usuarioForm.confirmPassword && (usuarioForm.password !== usuarioForm.confirmPassword)) {
            validateStatus = false
            errors["password"] = "Las contraseñas no coinciden"
            errors["confirmPassword"] = "Las contraseñas no coinciden"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        //else {
        //     if (passwords.password !== usuarioForm.password) {
        //         validateStatus = false
        //         errors["password"] = "La contraseña no coincide"
        //         setErrores({
        //             ...errores,
        //             errorMessages: errors
        //         })
        //     }
        // }
        return validateStatus
    }
    const handleGuardarCambios = (e) => {
      if (validate()) {
          // Establece el valor del campo "rol" en 5
          const { confirmPassword, ...newUsuarioForm } = usuarioForm;
          newUsuarioForm.rol = 5;
          console.log(newUsuarioForm)
          dispatch(axiosCrearUsuario(newUsuarioForm,navigate));
      }
      console.log("No entra guardarCambios")
    }
  
    const handleRoleChange = (role) => {
        if (role.id === usuarioForm.rol) {
            setUsuarioForm({
                ...usuarioForm,
                rol: 0
            })
        } else {
            setUsuarioForm({
                ...usuarioForm,
                rol: role.id
            })
        }
    };
  return (
    <div>
    <div className="loginPage">
      <div className="content-left">
        <img src={loginbg} className="img-fluid" alt="" />
      </div>

      <div className="content-right">

        <div className="content-right__form">

          <div className="loginForm">
            <img src={logo_cms} className="img-fluid img-brand" alt="" />
            <h1> Crear Cuenta </h1>
            <p>Descubre tu mundo, categoría por categoría.</p>

            <div className="form-group md-input">
                <input className="form-control md-form-control" type="text" onChange={handleChange} name="username" value={usuarioForm.username}  />
                {errores.errorMessages &&
                    <p style={{ color: "red" }}>{errores.errorMessages.username}</p>
                }
                <label className="md-label">Username<span>*</span></label>
            </div>
            <div className="form-group md-input">
                <input className="form-control md-form-control" type="text" onChange={handleChange} name="nombre" value={usuarioForm.nombre}  />
                {errores.errorMessages &&
                    <p style={{ color: "red" }}>{errores.errorMessages.nombre}</p>
                }
                <label className="md-label">Nombre<span>*</span></label>
            </div>
            <div className="form-group md-input">
                <input className="form-control md-form-control" type="text" onChange={handleChange} name="email" value={usuarioForm.email}  />
                {errores.errorMessages &&
                    <p style={{ color: "red" }}>{errores.errorMessages.email}</p>
                }
                <label className="md-label">Email<span>*</span></label>
            </div>
            <div className="form-group md-input">
                <input className="form-control md-form-control" type="password" onChange={handleChange} name="password" />
                {errores.errorMessages &&
                    <p style={{ color: "red" }}>{errores.errorMessages.password}</p>
                }
                <label className="md-label">Contraseña<span>*</span></label>
            </div>
            <div className="form-group md-input">
                <input className="form-control md-form-control" type="password" onChange={handleChange} name="confirmPassword" />
                {errores.errorMessages &&
                    <p style={{ color: "red" }}>{errores.errorMessages.confirmPassword}</p>
                }
                <label className="md-label">Confirmar contraseña<span>*</span></label>
            </div>
            
            <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios}>Registrarse </button>
            <span className="forgotPassword"> ¿Aún no sos parte? <br/>Registrate <Link to="/register-page"> aqui </Link> o bien, <Link to="/public/"> navega sin suscripción </Link></span>
          </div> 
            <Alert/>
        </div>

        <div className="poweredby"> <span> Producto desarrollado por el equipo 4</span></div>
      </div>
    </div>
  </div>  
  );
}

export default RegisterPage;
