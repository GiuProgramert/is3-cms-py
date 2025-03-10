import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import loginbg from "../imgs/login.jpeg"
import logo_cms from "../imgs/CMS.png"
import { useDispatch } from "react-redux"
import { axiosIniciarSesion } from "../reducers/Sesion/actions";
import { GoogleLogin } from '@react-oauth/google';
import Cookies from "js-cookie";
import { Alert } from "../components/Alert";
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from "axios";
import { setIsError } from "../reducers/Alert";
import { setSesion } from "../reducers/Sesion";
const LoginPage = () => {
  const [user, setUser] = useState([])
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [credenciales, setCredenciales] = useState({
    username: "",
    password: ""
  })

  const handleSubmit = (e) => {
    e.preventDefault();

  };
  const handleChange = ({ target }) => {
    setCredenciales({
      ...credenciales,
      [target.name]: target.value
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
      const expiryDate = new Date().getTime() + codeResponse.expires_in * 1000
      Cookies.set("expires",expiryDate)
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
              <img src={logo_cms} className="img-fluid img-brand" alt="" />
              <h1> Iniciar Sesión </h1>
              <p>Descubre tu mundo, categoría por categoría.</p>

              <button onClick={login} className="btn btn-lg btn-primary">Comenzar</button>
            </form>
            <Alert />
          </div>

          <div className="poweredby"> <span> Producto desarrollado por el equipo 4</span></div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
