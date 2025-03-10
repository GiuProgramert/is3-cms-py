import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearSubCategoria, axiosEliminarSubCateg, axiosModficarCategoria, axiosModficarSubcategoria } from '../reducers/Categorias/actions.js'
import { setIsError } from '../reducers/Alert/index.js'
import { Alert } from "../components/Alert.jsx"
import { Modal, Row, Form } from 'react-bootstrap'
import { Button } from '@mui/material'
import { verificarPermiso } from '../reducers/Roles/actions.js'
import { ModalEliminarItems } from '../components/ModalEliminar.jsx'

export default function PaginaEditarCategorias() {
    const [showEliminarSubCateg, setShowEliminarSubCateg] = useState(false)
    const [subCategoriaAEliminar, setSubCategoriaAEliminar] = useState({})
    const [show, setShow] = useState(false)
    const [editarSubcateg, setEditarSubcateg] = useState(false)
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const { categoriaSeleccionado } = useSelector(state => state.Categoria)
    const [categoriaForm, setCategoriaForm] = useState(categoriaSeleccionado)
    const [subcategoriasForm, setSubcategoriasForm] = useState(categoriaSeleccionado?.subcategorias)
    const { roles } = useSelector(state => state.Rol)
    const { rol } = useSelector(state => state.Sesion)
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const initialSubcateg = {
        "nombre": "",
        "descripcion": "",
        "categoria": 0
    }
    const [formSubcate, setFormSubcate] = useState(initialSubcateg)
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
        return validateStatus
    }
    const handleGuardarCambios = (e) => {

        if (validate()) {
            dispatch(axiosModficarCategoria(categoriaForm, navigate))
        }
    }
    const handleCancelarSub = () => {
        setFormSubcate(initialSubcateg)
        setShow(false)
        setErrores({})
        setEditarSubcateg(false)
    }

    const validateSub = () => {
        let validateStatus = true;
        let errors = {}
        if (!formSubcate.nombre) {
            validateStatus = false
            errors["nombre"] = "Nombre es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!formSubcate.descripcion) {
            validateStatus = false
            errors["descripcion"] = "Descripción es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus

    }
    const handleGuardarEditarSubCateg = () => {
        dispatch(axiosModficarSubcategoria({
            ...formSubcate,
            categoria: categoriaSeleccionado?.id
        },navigate))
        setFormSubcate(initialSubcateg)
        setShow(false)
        setErrores({})
    }
    const handleGuardarSubCateg = () => {
        dispatch(axiosCrearSubCategoria({
            ...formSubcate,
            categoria: categoriaSeleccionado?.id
        },navigate))
        setFormSubcate(initialSubcateg)
        setShow(false)
        setErrores({})
    }

    const handleValidar = (e) => {
        if (!validateSub()) {
            e.preventDefault();
        } else {
            if (!editarSubcateg) {
                handleGuardarSubCateg()
            } else {
                handleGuardarEditarSubCateg()
            }
        }


    }
    const handleEditarRango = (item) => {
        setErrores({})
        setFormSubcate(item)
        setEditarSubcateg(true)
        setShow(true)
    }
    const onAgregarSub = () => {
        setShow(true)
        setEditarSubcateg(false)
        setFormSubcate(initialSubcateg)
    }
    const handleSub = ({ target }) => {
        setFormSubcate({
            ...formSubcate,
            [target.name]: target.value
        })
    }
    const handleEliminar=(item)=>{
        setSubCategoriaAEliminar(item)
        setShowEliminarSubCateg(true)
    }
    const handleEliminarSubCateg=()=>{
        dispatch(axiosEliminarSubCateg(subCategoriaAEliminar?.id,navigate))
        setShowEliminarSubCateg(false)
    }
    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="sectionHeader">
                    <h1 className="page-title"> Editar categoria </h1>
                    {editar === false ?
                        <div className='actions'>
                            <a href={null} onClick={() => { if (verificarPermiso(rol, "EDITAR_CATEGORIA")) { setEditar(true) } else { dispatch(setIsError("Solo el usuario con rol de admin puede editar las categorías.")) } }} className="btn btn-lg btn-primary" style={{ "color": "white" }}>
                                <span className="material-icons-outlined"> edit </span> Editar
                            </a>
                        </div>
                        :
                        <div className='actions'>
                            <Link to="/admin/categorias" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                            <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios}>Guardar categoria </button>
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
                <div className="contentPage card">

                    {/* <!-- Subtitle --> */}
                    <div className="sectionHeader">
                        <h2 className="page-subtitle"> Subcategorías </h2>
                        <div className="actions">
                            <a href={null} className="btn btn-lg btn-primary" style={editar === false ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "grey" } : { "color": "white" }} onClick={onAgregarSub} disabled={!editar}>
                                <span className="material-icons-outlined"> add </span>Agregar
                            </a>
                        </div>
                    </div>

                    {/* <!-- section tabla Docymentos --> */}
                    {subcategoriasForm.length > 0 &&
                        <section id="tabla-establecimientos">
                            <div className="table-responsive">
                                <table className="table table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th scope="col">Nombre</th>
                                            <th scope="col">Descripción</th>
                                            <th scope='col'>Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {subcategoriasForm?.map((item, index) => {
                                            return <tr key={index}>
                                                <td>{item.nombre}</td>
                                                <td>{item.descripcion}</td>
                                                <td>
                                                    <div className="table-actions">
                                                        <a  href={null} className="btn btn-secondary btn-md btn-floating" role='button' onClick={() => { handleEditarRango(item) }} title='EDITAR' style={editar === false ? { "pointerEvents": "none", "cursor": "default" } : { "color": "white" }}>
                                                            <i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                                                        </a>
                                                        <a href={null} className="btn btn-secondary btn-md btn-floating" onClick={() => handleEliminar(item)} title='ELIMINAR' style={editar === false ? { "pointerEvents": "none", "cursor": "default" } : { "color": "grey" }}>
                                                            <i className="material-icons-outlined"> delete_forever </i>
                                                        </a>
                                                    </div>
                                                </td>
                                            </tr>
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </section>
                    }
                    {/* <!-- Fin section tabla Documentos --> */}
                    <Modal show={show} onHide={() => { setShow(false); setErrores({}) }}
                        size="xl"
                        centered
                        className="modal modal-custom fade">
                        <Modal.Header className="modal-header" closeButton>
                            <Modal.Title className="modal-title">{editarSubcateg ? "Editar" : "Agregar"}</Modal.Title>
                        </Modal.Header>
                        <Modal.Body className="modal-body">
                            <form action="" className="form-lotes">
                                <Row className="modal-row">
                                    <div className="form-group md-input">
                                        <Form.Control className="form-control md-form-control" required="" type="text" placeholder=" " name="nombre" onChange={handleSub} value={formSubcate?.nombre} />
                                        {errores.errorMessages &&
                                            <p style={{ color: "red" }}>{errores.errorMessages.nombre}</p>
                                        }
                                        <label className="md-label">Nombre <span>*</span></label>
                                    </div>
                                    <div className="form-group md-input">
                                        <Form.Control className="form-control md-form-control" required="" type="text" placeholder=" " name="descripcion" onChange={handleSub} value={formSubcate?.descripcion} />
                                        {errores.errorMessages &&
                                            <p style={{ color: "red" }}>{errores.errorMessages.descripcion}</p>
                                        }
                                        <label className="md-label">Descripción <span>*</span></label>
                                    </div>
                                </Row>
                            </form>
                        </Modal.Body>
                        <Modal.Footer className="modal-footer">
                            <Button variant="secondary" onClick={handleCancelarSub}>
                                cancelar
                            </Button>

                            <Button className="btn  btn-primary" onClick={handleValidar} >
                                {editarSubcateg ? "Editar" : "Agregar"}
                            </Button>
                        </Modal.Footer>
                    </Modal>
                    <ModalEliminarItems showEliminar={showEliminarSubCateg} setShowEliminar={setShowEliminarSubCateg} handleEliminar={handleEliminarSubCateg} />

                </div>


            </div>
        </div>
    )
}