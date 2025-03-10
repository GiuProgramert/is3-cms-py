import React, { useEffect, useState } from 'react'
import { Button, Pagination, Stack } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from "axios"
import { baseUrl } from '../App';
import { useDispatch, useSelector } from 'react-redux';
import { setUsuarioSeleccionado } from '../reducers/Usuarios';
import { axiosEliminarUsuario, axiosGetUsuarios } from '../reducers/Usuarios/actions';
import { Alert } from '../components/Alert';
import { axiosGetRoles, verificarPermiso } from '../reducers/Roles/actions';
import { Modal } from 'react-bootstrap';
import { setIsError } from '../reducers/Alert';

export const listaUsuarios = [
  {
    "id": 1,
    "roles": [
      {
        "id": 2,
        "permisos": [
          {
            "id": 5,
            "nombre": "CREAR_USUARIO"
          },
          {
            "id": 6,
            "nombre": "EDITAR_USUARIO"
          }
        ],
        "nombre": "autor"
      }
    ],
    "username": "Alejandra",
    "email": "alezcanosalinas@gmail.com",
    "password": "1234"
  },
  {
    "id": 2,
    "roles": [
      {
        "id": 3,
        "permisos": [
          {
            "id": 1,
            "nombre": "VER_CONTENIDO"
          },
          {
            "id": 4,
            "nombre": "RECHAZAR_CONTENIDO"
          }
        ],
        "nombre": "editor"
      }
    ],
    "username": "Hadi",
    "email": "hfour@gmail.com",
    "password": "1234"
  },
  {
    "id": 3,
    "roles": [
      {
        "id": 5,
        "permisos": [
          {
            "id": 9,
            "nombre": "CREAR_ROL"
          }
        ],
        "nombre": "suscriptor"
      }
    ],
    "username": "Pablo",
    "email": "pbatiliana@gmail.com",
    "password": "1234"
  },
  {
    "id": 4,
    "roles": [
      {
        "id": 4,
        "permisos": [
          {
            "id": 7,
            "nombre": "ELIMINAR_USUARIO"
          }
        ],
        "nombre": "publicador"
      }
    ],
    "username": "anaChamorro",
    "email": "ancha@gmail.com",
    "password": "48456"
  },
  {
    "id": 5,
    "roles": [
      {
        "id": 4,
        "permisos": [
          {
            "id": 7,
            "nombre": "ELIMINAR_USUARIO"
          }
        ],
        "nombre": "publicador"
      }
    ],
    "username": "belenMendieta",
    "email": "bMendieta@gmail.com",
    "password": "1234"
  },
  {
    "id": 6,
    "roles": [
      {
        "id": 1,
        "permisos": [
          {
            "id": 1,
            "nombre": "VER_CONTENIDO"
          },
          {
            "id": 6,
            "nombre": "EDITAR_USUARIO"
          }
        ],
        "nombre": "ADMIN"
      }
    ],
    "username": "client",
    "email": "cli@gmail.com",
    "password": "1234"
  },
  {
    "id": 7,
    "roles": [
      {
        "id": 2,
        "permisos": [
          {
            "id": 5,
            "nombre": "CREAR_USUARIO"
          },
          {
            "id": 6,
            "nombre": "EDITAR_USUARIO"
          }
        ],
        "nombre": "autor"
      },
      {
        "id": 1,
        "permisos": [
          {
            "id": 1,
            "nombre": "VER_CONTENIDO"
          },
          {
            "id": 6,
            "nombre": "EDITAR_USUARIO"
          }
        ],
        "nombre": "ADMIN"
      }
    ],
    "username": "client",
    "email": "cli@gmail.com",
    "password": "1234"
  },
]; // Tu lista de usuarios

export const PaginaUsuarios = () => {
  const [modalEliminar, setModalEliminar] = useState(false)
  const { usuarios } = useSelector(state => state.Usuario)
  const [usuarioEliminar, setUsuarioEliminar] = useState({})
  const { roles } = useSelector(state => state.Rol)
  const { rol } = useSelector(state => state.Sesion)
  useEffect(() => {
    dispatch(axiosGetRoles())
  }, [])
  const [usuariosParcial, setListaUsuarioParcial] = useState(usuarios)
  const mostrar = [4, 8, 12, 16]
  const [pageCount, setPageCount] = useState(13)
  const [countElementPerPage, setcountElementPerPage] = useState(4)
  const [pageNumber, setPageNumber] = useState(1)
  const dispatch = useDispatch()
  useEffect(() => {
    setcountElementPerPage(4)
    setPageNumber(1)
    setPageCount(Math.ceil(usuarios?.length / 4));
  }, [usuarios])
  useEffect(() => {
    setListaUsuarioParcial(usuarios?.slice(0, mostrar[0]))
  }, [usuarios])
  useEffect(() => {
    dispatch(axiosGetUsuarios())
  }, [])

  const handleChangeCount = (event, value) => {
    setPageNumber(value)
    setListaUsuarioParcial(usuarios?.slice((value - 1) * countElementPerPage, (value - 1) * countElementPerPage + countElementPerPage))
  };
  const handleEliminar = (item) => {
    if (verificarPermiso(rol, "ELIMINAR_USUARIO")) {
      setUsuarioEliminar(item)
      setModalEliminar(true)
    } else {
      dispatch(setIsError("Se necesitan permisos para realizar esta acción."))
    }

  }
  const handlePageCount = (event, value) => {
    setPageNumber(1)
    setcountElementPerPage(Number(event.target.value))
    setListaUsuarioParcial(usuarios?.slice(0, event.target.value))
    setPageCount(Math.ceil(usuarios?.length / event.target.value));
  };


  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Usuarios </h1>
          {
            verificarPermiso(rol,"CREAR_USUARIO") &&
            <Link to="/admin/usuarios/crear" className="btn btn-lg btn-primary" style={!verificarPermiso(rol, "CREAR_USUARIO") ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }}> Nuevo Usuario </Link>
          }
        </div>
        <Alert />
        <div className="contentPage card">
          <section id="aplicacioens">
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">Username</th>
                    <th scope="col">Email</th>
                    <th scope="col">Roles</th>
                    <th scope="col">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {usuariosParcial?.map((item) => {
                    return <tr key={item.id}>
                      <td>{item.username}</td>
                      <td>{item.email}</td>
                      <td>  {item.roles
                        .map(roleId => roles.find(r => r.id === roleId)?.nombre) // Encuentra el nombre del rol
                        .filter(Boolean) // Elimina cualquier valor undefined si no se encuentra un rol
                        .join(", ") // Une los nombres con comas
                      }</td>
                      <td>
                        <div className="table-actions">
                          {
                            verificarPermiso(rol,"EDITAR_USUARIO") &&
                            <Link
                              title='EDITAR'
                              to="/admin/usuarios/editar"
                              onClick={() => { dispatch(setUsuarioSeleccionado(item)) }}
                            ><i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                            </Link>
                          }
                          {
                            verificarPermiso(rol, "ELIMINAR_USUARIO") &&
                            <a
                              title='ELIMINAR'
                              role='button'
                              onClick={() => { handleEliminar(item) }}

                            ><i className="material-icons-outlined" style={{ "color": "grey" }}> delete_forever  </i>
                            </a>
                          }

                          {/* <a href={null} role='button' onClick={() => handleEliminar(item)} title='ELIMINAR'>
                              <i className="material-icons-outlined" style={{ "color": "grey" }}> delete_forever </i>
                            </a> */}
                        </div>
                      </td>
                    </tr>
                  })}
                </tbody>
              </table>
            </div>
          </section>
          <div id="paginador">
            <label>
              Mostrar
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
          <p>¿Esta seguro que desea eliminar el usuario {usuarioEliminar.nombre}?</p>
        </Modal.Body>
        <Modal.Footer className="modal-footer">
          <Button variant="secondary" onClick={() => { setModalEliminar(false) }}>
            Cancelar
          </Button>
          <Button className="btn  btn-primary" onClick={() => { dispatch(axiosEliminarUsuario(usuarioEliminar.id)); setModalEliminar(false) }} >
            Eliminar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
