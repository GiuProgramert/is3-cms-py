import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearContenido } from '../reducers/Contenido/actions'
import { setIsError } from '../reducers/Alert';
import { Alert } from '../components/Alert';
import { TextEditor } from '../components/TextEditor';
import { axiosGetUsuarios } from '../reducers/Usuarios/actions';
import { verificarPermiso } from '../reducers/Roles/actions';

export default function PaginaCrearContenido() {
    const [filteredSubcategorias, setFilteredSubcategorias] = useState([]);
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const { categorias } = useSelector(state => state.Categoria)
    const [categoriaList, setCategoriaList] = useState(categorias)
    const { rol, id, } = useSelector(state => state.Sesion)
    const { usuarios } = useSelector(state => state.Usuario)
    const [contenidoForm, setContenidoForm] = useState({
        "titulo": "",
        "cuerpo": "",
        "resumen": "",
        "estado": "",
        "categoria": "",
        "autor": "",
        "subcategoria": "",
        "comentarios":"",
        "multimedia":""
    })
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const { roles } = useSelector(state => state.Rol)
    // const permiso = contenidoForm.ro.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const handleCancelar = () => {
        setEditar(false)
    }
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
        if (!contenidoForm.categoria) {
            validateStatus = false
            errors["categoria"] = "Categoria es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!contenidoForm.subcategoria) {
            validateStatus = false
            errors["subcategoria"] = "Subcategoria es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus
    }
    useEffect(() => {
        dispatch(axiosGetUsuarios())
    }, [])

    function formatearFecha(fechaOriginal) {
        var partes = fechaOriginal.split('/');
        var mes = partes[0];
        var dia = partes[1];
        var anio = partes[2];
        var fechaFormateada = anio + '-' + mes + '-' + dia;

        return fechaFormateada;
    }
    const handleGuardarCambios = (e) => {
        if (validate()) {
            const {categoria,...contenidoFormCopy}=contenidoForm
            dispatch(axiosCrearContenido({ ...contenidoFormCopy, estado: "en_revision", autor: id },roles, id, usuarios, navigate))
        }
    }
    const handleGuardarCambiosBorrador = (e) => {
        if (validate()) {
            const {categoria,...contenidoFormCopy}=contenidoForm
            dispatch(axiosCrearContenido({ ...contenidoFormCopy, estado: "borrador", autor: id }, roles,id, usuarios, navigate))
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
                    <h1 className="page-title"> Crear Post </h1>
                    {editar === false ?
                        <div className='actions'>
                            <a href={null} onClick={() => { if (verificarPermiso(rol, "CREAR_CONTENIDO")) { setEditar(true) } else { dispatch(setIsError("Solo el usuario con rol de autor puede crear un contenido.")) } }} className="btn btn-lg btn-primary" style={{ "color": "white" }}>
                                <span className="material-icons-outlined"> edit </span> Crear
                            </a>
                        </div>
                        :
                        <div className='actions'>
                            <Link to="/admin/contenido" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                            <button className="btn btn-lg btn-secondary" onClick={handleGuardarCambiosBorrador}>Enviar a Borrador </button>
                            <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios}>Enviar a Revision </button>
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
                        <div className="form-group md-input">
                            <select className="form-control md-select" name="categoria" onChange={handleChange} disabled={!editar} value={contenidoForm?.categoria}>
                                <option value={""}></option>
                                {
                                    categoriaList?.map((item) => (
                                        <option key={item.id} value={String(item.id)}>{item.nombre}</option>
                                    ))
                                }
                            </select>
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.categoria}</p>
                            }
                            <label className="md-label"> Categoria <span>*</span> </label>
                        </div>
                        <div className="form-group md-input">
                            <select className="form-control md-select" name="subcategoria" onChange={handleChange} disabled={!editar && !contenidoForm?.categoria} value={contenidoForm?.subcategoria}>
                                <option value={""}></option>
                                {categorias.find(
                                    (categoria) => categoria.id === parseInt(contenidoForm?.categoria)
                                )?.subcategorias?.map((subcategoria) => (
                                    <option key={subcategoria.id} value={subcategoria.id}>
                                        {subcategoria.nombre}
                                    </option>
                                ))}
                            </select>
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.categoria}</p>
                            }
                            <label className="md-label"> Subcategoría <span>*</span> </label>
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