import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setRol } from '../reducers/Roles'
import { Link } from 'react-router-dom'
import { Button, Pagination, Stack } from '@mui/material'
import { axiosEliminarRol, axiosGetRoles, verificarPermiso } from '../reducers/Roles/actions'
import { Alert } from '../components/Alert'
import { Modal } from 'react-bootstrap'
import { setIsError } from '../reducers/Alert'

export const PaginaRoles = () => {
    const [modalEliminar, setModalEliminar] = useState(false)
    const mostrar = [4, 8, 12, 16]
    const [pageCount, setPageCount] = useState(13)
    const [countElementPerPage, setcountElementPerPage] = useState(4)
    const { roles } = useSelector(state => state.Rol)
    const { rol } = useSelector(state => state.Sesion)
    const [eliminarRol, setEliminarRol] = useState({})
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const [listaRolesParcial, setListaRolesParcial] = useState(roles)
    const [pageNumber, setPageNumber] = useState(1)
    const dispatch = useDispatch()
    const handleChangeCount = (event, value) => {
        setPageNumber(value)
        setListaRolesParcial(roles?.slice((value - 1) * countElementPerPage, (value - 1) * countElementPerPage + countElementPerPage))
    }
    const handlePageCount = (event, value) => {
        setPageNumber(1)
        setcountElementPerPage(Number(event.target.value))
        setListaRolesParcial(roles?.slice(0, event.target.value))
        setPageCount(Math.ceil(roles?.length / event.target.value));
    }
    useEffect(() => {
        setcountElementPerPage(4)
        setPageNumber(1)
        setPageCount(Math.ceil(roles?.length / 4));
    }, [roles])
    useEffect(() => {
        setListaRolesParcial(roles?.slice(0, mostrar[0]))
    }, [roles])
    useEffect(() => {
        dispatch(axiosGetRoles())
    }, [])
    const handleEliminar = (item) => {
        if (verificarPermiso(rol, "ELIMINAR_ROL")) {
            setEliminarRol(item)
            setModalEliminar(true)
        } else {
            dispatch(setIsError("Se necesitan permisos para realizar esta acción."))
        }

    }
    return (
        <div className="dashboardContent">
            <div className="container-fluid">

                <div className="sectionHeader">
                    <h1 className="page-title"> Roles </h1>
                    {
                        verificarPermiso(rol, "CREAR_ROL") &&
                        <div className="actions">
                            <Link to="/admin/roles/nuevo" className="btn btn-lg btn-primary" style={!verificarPermiso(rol, "CREAR_ROL") ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }}> Nuevo Rol </Link>
                        </div>
                    }

                </div>
                <Alert />
                <div className="contentPage card">

                    <section id="aplicacioens">

                        <div className="table-responsive">
                            <table className="table table-striped table-hover">
                                <thead>
                                    <tr>
                                        <th scope="col">Nombre del rol</th>
                                        {
                                            (verificarPermiso(rol, "EDITAR_ROL") || verificarPermiso(rol, "ELIMINAR_ROL")) &&
                                            <th scope="col">Acciones</th>
                                        }
                                    </tr>
                                </thead>
                                <tbody>
                                    {listaRolesParcial.map((item) => {
                                        return <tr key={item.id}>
                                            <td>{item.nombre}</td>
                                            {
                                                (verificarPermiso(rol, "EDITAR_ROL") || verificarPermiso(rol, "ELIMINAR_ROL")) &&
                                                <td>
                                                    <div className="table-actions">
                                                        <Link
                                                            to='/admin/roles/editar'
                                                            onClick={() => { dispatch(setRol(item)) }}
                                                            title='EDITAR'
                                                        ><i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                                                        </Link>
                                                        <a
                                                            title='ELIMINAR'
                                                            role='button'
                                                            onClick={() => { handleEliminar(item) }}

                                                        ><i className="material-icons-outlined" style={{ "color": "grey" }}> delete_forever  </i>
                                                        </a>
                                                    </div>
                                                </td>
                                            }
                                        </tr>
                                    })}
                                </tbody>
                            </table>
                        </div>

                    </section>

                    <div id="paginador">
                        <label>Mostrar
                            <select
                                value={countElementPerPage}
                                onChange={handlePageCount}
                                className="form-control custom-select"
                                id="maxRows"
                                name="state"
                            >
                                {mostrar.map((item) => {
                                    return <option key={item} value={item}>{item}</option>;
                                })}
                                resultados
                            </select>
                        </label>

                        <Stack spacing="2">
                            <Pagination
                                count={pageCount}
                                page={pageNumber}
                                shape="rounded"
                                onChange={handleChangeCount}
                                color="primary"
                            />
                        </Stack>
                    </div>


                </div>

            </div>
            <Modal show={modalEliminar} onHide={() => { setModalEliminar(false) }}
                size="xl"
                centered
                className="modal modal-custom fade">
                <Modal.Header className="modal-header" closeButton>
                    <Modal.Title className="modal-title">Eliminar Item</Modal.Title>
                </Modal.Header>
                <Modal.Body className="modal-body">
                    <p>¿Esta seguro que desea eliminar el rol {eliminarRol?.nombre}?</p>
                </Modal.Body>
                <Modal.Footer className="modal-footer">
                    <Button variant="secondary" onClick={() => { setModalEliminar(false) }}>
                        Cancelar
                    </Button>
                    <Button className="btn  btn-primary" onClick={() => { dispatch(axiosEliminarRol(eliminarRol.id)); setModalEliminar(false) }} >
                        Eliminar
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}
