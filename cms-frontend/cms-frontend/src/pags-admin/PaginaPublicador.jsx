import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosGetUsuarios } from '../reducers/Usuarios/actions'
import { axiosInactivar, axiosPublicarRechazar } from '../reducers/Contenido/actions'
import { Button, Modal } from 'react-bootstrap'
import moment from 'moment'
import { Alert } from '../components/Alert'

export const PaginaPublicador = () => {
    const { contenidoSeleccionado } = useSelector(state => { return state.Contenido })
    const { usuarios } = useSelector(state => state.Usuario)
    const { roles } = useSelector(state => state.Rol)
    const { rol, id } = useSelector(state => state.Sesion)
    const [modalRechazar, setmodalRechazar] = useState(false)
    const [motivo, setmotivo] = useState("")
    let rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const dispatch = useDispatch()
    const navigate = useNavigate()
    useEffect(() => {
        dispatch(axiosGetUsuarios())
    }, [])
    const handleAction = (estado) => {
        if(estado==="inactivar"){
            dispatch(axiosInactivar(contenidoSeleccionado, id, estado, motivo, usuarios, navigate))
        }else{
            dispatch(axiosPublicarRechazar(contenidoSeleccionado, id, estado, motivo, usuarios,roles, navigate))
        }

    }
    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="contentPage card">
                    <Alert/>
                    <div className="sectionHeader">
                        <h1 className="page-title">{contenidoSeleccionado.titulo}</h1>
                    </div>
                    <h1 className='page-autor'>Autor: </h1><p>{usuarios?.find(user => user.id === contenidoSeleccionado.autor)?.username}</p>
                    <h1 className='page-autor'>Fecha: </h1> <p>{moment(contenidoSeleccionado.fecha).format('L')}</p>
                    <div className='post'>
                        <div dangerouslySetInnerHTML={{ __html: contenidoSeleccionado.cuerpo }}></div>
                    </div>
                    <h1 className='page-autor'>Resumen: </h1> <p>{contenidoSeleccionado.resumen}</p>
                    <div className='actions'>
                    {
                            contenidoSeleccionado?.estado === "en_revision" &&
                            <>
                                <button className='btn btn-secondary' onClick={() => setmodalRechazar(true)}>Rechazar</button>
                                <button className='btn btn-primary' onClick={() => { handleAction("aprobado") }}>Publicar</button>
                            </>
                        }
                        {
                            contenidoSeleccionado?.estado === "aprobado" &&
                            <button className='btn btn-primary' onClick={() => { handleAction("inactivar") }}>Inactivar</button>
                        }
                        {
                            (contenidoSeleccionado?.estado === "inactivo" || contenidoSeleccionado?.estado === "rechazado") &&
                            <button className='btn btn-primary' onClick={() => { handleAction("aprobado") }}>Publicar {contenidoSeleccionado?.estado === "inactivo" && "de nuevo"}</button>
                        }
                    </div>
                </div>


            </div>
            <Modal show={modalRechazar} onHide={() => { setmodalRechazar(false); setmotivo("") }}
                size="xl"
                centered
                className="modal modal-custom fade">
                <Modal.Header className="modal-header" closeButton>
                    <Modal.Title className="modal-title">Rechazar contenido</Modal.Title>
                </Modal.Header>
                <Modal.Body className="modal-body">
                    <div className="form-group md-input">
                        <input className="form-control md-form-control" type="text" name="motivo" onChange={({ target }) => { setmotivo(target.value) }} />
                        <label className='md-label'>Motivo <span>*</span></label>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modal-footer">
                    <Button variant="secondary" onClick={() => { setmodalRechazar(false); setmotivo("") }}>
                        Cancelar
                    </Button>
                    <Button className="btn  btn-primary" onClick={() => { handleAction("rechazado"); setmodalRechazar(false) }} >
                        Enviar
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}
