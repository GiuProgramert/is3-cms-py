import loginbg from "../imgs/login.jpeg"
import logo_cms from "../"
import React, { useState } from 'react'
import { useNavigate } from "react-router-dom"
import { useDispatch } from "react-redux"
import { axiosRegistrarUsuario } from "../reducers/Sesion/actions"

export const RegistroUsuario = () => {
    const navigate=useNavigate()
    const dispatch=useDispatch()
    const [registroUsuario, setRegistroUsuario] = useState({})
    const [errores, setErrores] = useState({})
    const handleChange=({target})=>{
        setRegistroUsuario({
            ...registroUsuario,
            [target.name]:target.value
        })
    }
    const handleSubmit=(event)=>{
        let errors={}
        event.preventDefault()
        if(registroUsuario.password!==registroUsuario.confirmPassword){
            errors["password"] = "Las constraseñas no coinciden."
            errors["confirmPassword"] = "Las constraseñas no coinciden."
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }else{
            const {confirmPassword,...newRegistroUsuario}=registroUsuario
            dispatch(axiosRegistrarUsuario(newRegistroUsuario,navigate))
        }
    }
  return (
    <div className="loginPage">
    <div className="content-left">
      <img src={loginbg} className="img-fluid" alt="" />
    </div>

    <div className="content-right">

      <div className="content-right__form">

        <form onSubmit={handleSubmit} className="loginForm">
          <img src={logo_cms} className="img-fluid img-brand" alt="" />
          <h1> Registro de usuario </h1>
          <p>Registrate para aprovechar al máximo!</p>
        
          <div className="form-group md-input">
            <input className="form-control md-form-control" required={true} type="text" placeholder=" " name="username" onChange={handleChange}/>
            <label className="md-label">Username<span>*</span></label>
          </div>
          <div className="form-group md-input">
            <input className="form-control md-form-control" required={true} type="text" placeholder=" " name="nombre" onChange={handleChange}/>
            <label className="md-label">Nombre<span>*</span></label>
          </div>
          <div className="form-group md-input">
            <input className="form-control md-form-control" required={true} type="email" placeholder=" " name="email" onChange={handleChange}/>
            <label className="md-label">Email<span>*</span></label>
          </div>
          <div className="form-group md-input">
            <input className="form-control md-form-control" required={true} type="password" placeholder=" " name="password" onChange={handleChange}/>
            <label className="md-label">Contraseña<span>*</span></label>
          </div>
          <div className="form-group md-input">
            <input className="form-control md-form-control" required={true} type="password" placeholder=" " name="confirmPassword" onChange={handleChange}/>
            <label className="md-label">Confirmar contraseña<span>*</span></label>
          </div>
            <button  type="submit" className="btn btn-lg btn-primary">Comenzar</button>
          <span className="forgotPassword"> ¿Aún no sos parte? <br/>Registrate <a href={null} role="button" style={{"color":"blue"}}> aquí </a></span>
        </form> 
          {/* <Alert/> */}
      </div>

      <div className="poweredby"> <span> Producto desarrollado por el equipo 4</span></div>
    </div>
  </div>
  )
}
