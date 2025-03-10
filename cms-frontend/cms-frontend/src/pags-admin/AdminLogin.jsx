import React, { useState } from "react";
import loginbg from "../imgs/login_admin.jpeg"
import logo_admin from "../imgs/ADM.png"
import { Link, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import { setSesion } from "../reducers/Sesion/index.js";
import {useDispatch} from "react-redux"
import { axiosIniciarSesion, axiosIniciarSesionAdm } from "../reducers/Sesion/actions.js";
import {Alert} from "../components/Alert.jsx"
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from "axios";
const AdminLogin=()=> {
  const dispatch=useDispatch()
  const navigate=useNavigate()
  const [credenciales, setCredenciales] = useState({
    username:"",
    password:""
  })

  const handleSubmit = (e) => {
    e.preventDefault();
  };
  const handleChange=({target})=>{
    setCredenciales({
      ...credenciales,
      [target.name]:target.value
    })
  }
  const axiosGetDetallesUsuario=(user)=>{
    axios
    .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
        headers: {
            Authorization: `Bearer ${user.access_token}`,
            Accept: 'application/json'
        }
    })
    .then((res) => {

      dispatch(axiosIniciarSesion(res.data.name,res.data.email,res.data.picture,navigate)) 
    })
    .catch((err) => console.log(err));
  }
  const login = useGoogleLogin({
    onSuccess: (codeResponse) => {
      Cookies.set("token",codeResponse.access_token)
      Cookies.set("expires",codeResponse.expires_in)
      axiosGetDetallesUsuario(codeResponse)
    },
    onError: (error) => console.log(error)
  });
  return (
    <div>
    <div className="loginPage">
      <div className="content-left">
        <img src={loginbg} className="img-fluid" alt="" />
      </div>

      <div className="content-right">

        <div className="content-right__form">

          <form onSubmit={handleSubmit} className="loginForm">
            <img src={logo_admin} className="img-fluid img-brand" alt="" />
            <h1> Administración </h1>
            <p>Gestion de contenido y configuracion.</p>
              <button  onClick={login} className="btn btn-lg btn-primary">Comenzar</button>
              {/* <span className="forgotPassword"> ¿Aún no sos parte? <br/>Registrate <Link to="/register-page"> aqui </Link> o bien, <Link to="/public/"> navega sin suscripción </Link></span> */}
          </form> 
            <Alert/>
        </div>

        <div className="poweredby"> <span> Producto desarrollado por el equipo 4</span></div>
      </div>
    </div>
  </div>  
  );
}

export default AdminLogin;
