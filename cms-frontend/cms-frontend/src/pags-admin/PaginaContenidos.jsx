import React, { useEffect, useState } from 'react'
import { Pagination, Stack } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from "axios"
import { baseUrl } from '../App';
import { useDispatch, useSelector } from 'react-redux';
import { setContenidoSeleccionado } from '../reducers/Contenido';
import { axiosGetContenido } from '../reducers/Contenido/actions';
import { axiosGetCategorias } from '../reducers/Categorias/actions';
import { axiosGetUsuarios } from '../reducers/Usuarios/actions';
import { verificarPermiso } from '../reducers/Roles/actions';
import { Alert } from '../components/Alert';




const PaginaContenidos = () => {
  const { usuarios } = useSelector(state => state.Usuario)
  const { categorias } = useSelector(state => state.Categoria)
  const { contenido } = useSelector(state => state.Contenido)
  const [contenidoList, setContenidoList] = useState(contenido)
  const { roles } = useSelector(state => state.Rol)
  const { rol } = useSelector(state => state.Sesion)
  // const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
  // const [contenidoList, setcontenidoList] = useState([])
  const [contenidoListParcial, setListaCategoriaParcial] = useState(contenidoList)
  const mostrar = [4, 8, 12, 16]
  const [pageCount, setPageCount] = useState(13)
  const [countElementPerPage, setcountElementPerPage] = useState(4)
  const [pageNumber, setPageNumber] = useState(1)
  const dispatch = useDispatch()
  useEffect(() => {
    setcountElementPerPage(4)
    setPageNumber(1)
    setPageCount(Math.ceil(contenido?.length / 4));
  }, [contenido])
  useEffect(() => {
    setContenidoList(contenido?.slice(0, mostrar[0]))
  }, [contenido])

  useEffect(() => {
    dispatch(axiosGetContenido())
    dispatch(axiosGetCategorias())
    dispatch(axiosGetUsuarios())
  }, [])

  const handleChangeCount = (event, value) => {
    setPageNumber(value)
    setContenidoList(contenido?.slice((value - 1) * countElementPerPage, (value - 1) * countElementPerPage + countElementPerPage))
  };

  const handlePageCount = (event, value) => {
    setPageNumber(1)
    setcountElementPerPage(Number(event.target.value))
    setContenidoList(contenido?.slice(0, event.target.value))
    setPageCount(Math.ceil(contenido?.length / event.target.value));
  };

  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Contenido </h1>
          <div className="actions">
            {
              verificarPermiso(rol, "CREAR_CONTENIDO") &&
              <Link to="/admin/contenido/crear" className="btn btn-lg btn-primary" style={!verificarPermiso(rol, "CREAR_CONTENIDO") ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }}> Nuevo Post </Link>
            }
          </div>
        </div>
        <Alert />
        <div className="contentPage card">
          <section id="aplicacioens">
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">Titulo</th>
                    <th scope="col">Autor</th>
                    <th scope="col">Estado</th>
                    <th scope="col">Fecha</th>
                    {
                      (verificarPermiso(rol,"EDITAR_CONTENIDO") || verificarPermiso(rol,"ELIMINAR_CONTENIDO")) &&
                      <th scope="col">Acciones</th>
                    }
                  </tr>
                </thead>
                <tbody>
                  {contenidoList?.map((item) => {
                    return <tr key={item.id}>
                      <td>{item.titulo}</td>
                      <td>{usuarios?.find(usuario => Number(usuario.id) === Number(item.autor))?.username}</td>
                      <td>{item.estado}</td>
                      <td>{item.fecha}</td>
                      {
                        verificarPermiso(rol,"EDITAR_CONTENIDO") &&
                        <td>
                          <div className="table-actions">
                            {
                              verificarPermiso(rol,"EDITAR_CONTENIDO") &&
                              <Link
                                title='EDITAR'
                                to="/admin/contenido/editar"
                                onClick={() => { dispatch(setContenidoSeleccionado(item)) }}
                              ><i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                              </Link>
                            }
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

    </div>
  )
}

export default PaginaContenidos;
