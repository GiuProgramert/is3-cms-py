import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearCategoria } from '../reducers/Categorias/actions.js'
import { setIsError } from '../reducers/Alert/index.js'
import { Alert } from "../components/Alert.jsx"
import { verificarPermiso } from '../reducers/Roles/actions.js'

export default function PaginaCrearCategoria() {
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const [categoriaForm, setCategoriaForm] = useState({ nombre: "" ,codigo:""})
    const { roles } = useSelector(state => state.Rol)
    const { rol } = useSelector(state => state.Sesion)
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleCancelar = () => {
        setEditar(false)
    }
    const handleChange = ({ target }) => {
        setCategoriaForm({
            ...categoriaForm,
            [target.name]: target.value
        })
    }
    const validate = () => {
        let validateStatus = true;
        let errors = {}
        if (!categoriaForm.nombre) {
            validateStatus = false
            errors["nombre"] = "Nombre es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!categoriaForm.codigo) {
            validateStatus = false
            errors["codigo"] = "Código es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus
    }
    const handleGuardarCambios = (e) => {
        if (validate()) {
            dispatch(axiosCrearCategoria(categoriaForm, navigate))
        }
    }

    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="sectionHeader">
                    <h1 className="page-title"> Crear categoria </h1>
                    {editar === false ?
                        <div className='actions'>
                            <a href={null} onClick={() => { if (verificarPermiso(rol, "CREAR_CATEGORIA")) { setEditar(true) } else { dispatch(setIsError("Solo el usuario con rol de admin puede crear categorías.")) } }} className="btn btn-lg btn-primary" style={{ "color": "white" }}>
                                <span className="material-icons-outlined"> edit </span> Crear
                            </a>
                        </div>
                        :
                        <div className='actions'>
                            <Link to="/admin/categorias" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                            <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios} >Guardar categoria </button>
                        </div>
                    }
                </div>
                <Alert />
                <div className="contentPage card">
                    <div className='form-col-4'>
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="text" onChange={handleChange} name="codigo" value={categoriaForm.codigo} disabled={!editar} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.codigo}</p>
                            }
                            <label className="md-label">Código categoria<span>*</span></label>
                        </div>
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="text" onChange={handleChange} name="nombre" value={categoriaForm.nombre} disabled={!editar} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.nombre}</p>
                            }
                            <label className="md-label">Nombre categoria<span>*</span></label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}