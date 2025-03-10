import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearContenido, axiosModficarContenido } from '../reducers/Contenido/actions.js'
import { axiosGetCategorias } from '../reducers/Categorias/actions.js';
import moment from 'moment/moment';
import { setIsError } from '../reducers/Alert/index.js';
import { Alert } from "../components/Alert.jsx"

import { axiosGetUsuarios } from '../reducers/Usuarios/actions.js';
import { TextEditor } from '../components/TextEditor.jsx';
import { axiosGetRoles, verificarPermiso } from '../reducers/Roles/actions.js';

export default function PaginaEditarContenido() {
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const { categorias } = useSelector(state => state.Categoria)
    const [categoriaList, setCategoriaList] = useState(categorias)
    const { username, rol, id } = useSelector(state => state.Sesion)
    const { contenidoSeleccionado } = useSelector(state => { return state.Contenido })
    const [contenidoForm, setContenidoForm] = useState(contenidoSeleccionado)
    const { usuarios } = useSelector(state => state.Usuario)
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const { roles } = useSelector(state => state.Rol)
    // const permiso = contenidoForm.ro.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const handleCancelar = () => {
        setEditar(false)
    }
    useEffect(() => {
        dispatch(axiosGetUsuarios())
    }, [])

    const handleChange = ({ target }) => {
        setContenidoForm({
            ...contenidoForm,
            [target.name]: target.value
        })
    }
    const validate = () => {
        let validateStatus = true;
        let errors = {}
        if (!contenidoForm.titulo) {
            validateStatus = false
            errors["titulo"] = "Titulo es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!contenidoForm.cuerpo) {
            validateStatus = false
            errors["cuerpo"] = "Cuerpo es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!contenidoForm.resumen) {
            validateStatus = false
            errors["resumen"] = "Resumen es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus
    }
    function formatearFecha(fechaOriginal) {
        var partes = fechaOriginal.split('/');
        var mes = partes[0];
        var dia = partes[1];
        var anio = partes[2];
        var fechaFormateada = anio + '-' + mes + '-' + dia;

        return fechaFormateada;
    }
    const handleGuardarCambios = (estadoValue) => {
        if (validate()) {
            dispatch(axiosModficarContenido(contenidoSeleccionado,{
                ...contenidoForm,
                estado: estadoValue,
            }, id, usuarios, roles,navigate))
        }
    }
    const handleCuerpo = (content) => {
        setContenidoForm({
            ...contenidoForm,
            cuerpo: content
        })
    }
    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="sectionHeader">
                    <h1 className="page-title"> Editar Post </h1>
                    {editar === false ?
                        <div className='actions'>
                            <a href={null} onClick={() => { if (verificarPermiso(rol, "EDITAR_CONTENIDO")) { setEditar(true) } else { dispatch(setIsError("Solo el usuario con rol de editor puede editar un contenido.")) } }} className="btn btn-lg btn-primary" style={verificarPermiso(rol, "EDITAR_CONTENIDO") ? { "color": "white" } : { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" }}>
                                <span className="material-icons-outlined"> edit </span> Editar
                            </a>
                        </div>
                        :
                        <div className='actions'>
                            <Link to="/admin/contenido" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                            <button className="btn btn-lg btn-secondary" onClick={() => handleGuardarCambios("borrador")}>Enviar a Borrador </button>
                            <button className="btn btn-lg btn-primary" onClick={() => handleGuardarCambios("en_revision")}>Enviar a Revisión </button>
                        </div>
                    }
                </div>

                <div className="contentPage card">
                    <Alert />
                    <div className='form-col-4'>

                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="text" onChange={handleChange} name="titulo" value={contenidoForm.titulo} disabled={!editar} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.titulo}</p>
                            }
                            <label className="md-label">Titulo<span>*</span></label>
                        </div>
                    </div>
                    <div className="form-group md-input">
                        <TextEditor contenido={contenidoForm.cuerpo} handleContenido={handleCuerpo} disable={!editar} />
                        {errores.errorMessages &&
                            <p style={{ color: "red" }}>{errores.errorMessages.cuerpo}</p>
                        }
                        <label className="texteditor-label">Contenido<span style={{ "color": "red" }}>*</span></label>
                    </div>
                    <div className="form-col">
                        <div className="form-group md-input">
                            <textarea className="form-control md-form-control" rows="4" placeholder=" " value={contenidoForm.resumen} onChange={handleChange} disabled={!editar} name='resumen' required={true} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.resumen}</p>
                            }
                            <label className="md-label"> Resumen<span>*</span> </label>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}