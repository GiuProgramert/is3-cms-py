import React, { useEffect, useState } from 'react'
import { Pagination, Stack } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { setCategoriaSeleccionado } from '../reducers/Categorias';
import { axiosEliminarCategoria, axiosGetCategorias } from '../reducers/Categorias/actions';
import { verificarPermiso } from '../reducers/Roles/actions';
import { Alert } from '../components/Alert';
import { ModalEliminarItems } from '../components/ModalEliminar';


const PaginaCategorias = () => {
  const navigate = useNavigate()
  const [showEliminarCateg, setShowEliminarCateg] = useState(false)
  const [categAEliminar, setCategAEliminar] = useState({})
  const { categorias } = useSelector(state => state.Categoria)
  const { rol } = useSelector(state => state.Sesion)
  // const [categoriasList, setcategoriasList] = useState([])
  const [categoriasListParcial, setListaCategoriaParcial] = useState(categorias)
  const mostrar = [4, 8, 12, 16]
  const [pageCount, setPageCount] = useState(13)
  const [countElementPerPage, setcountElementPerPage] = useState(4)
  const [pageNumber, setPageNumber] = useState(1)
  const dispatch = useDispatch()
  useEffect(() => {
    setcountElementPerPage(4)
    setPageNumber(1)
    setPageCount(Math.ceil(categorias?.length / 4));
  }, [categorias])
  useEffect(() => {
    setListaCategoriaParcial(categorias?.slice(0, mostrar[0]))

  }, [categorias])
  useEffect(() => {
    dispatch(axiosGetCategorias())
  }, [])
  const handleChangeCount = (event, value) => {
    setPageNumber(value)
    setListaCategoriaParcial(categorias?.slice((value - 1) * countElementPerPage, (value - 1) * countElementPerPage + countElementPerPage))
  };

  const handlePageCount = (event, value) => {
    setPageNumber(1)
    setcountElementPerPage(Number(event.target.value))
    setListaCategoriaParcial(categorias?.slice(0, event.target.value))
    setPageCount(Math.ceil(categorias?.length / event.target.value));
  };
  const handleEliminar = () => {
    dispatch(axiosEliminarCategoria(categAEliminar?.id, navigate))
    setShowEliminarCateg(false)
  }
  const onEliminar = (item) => {
    setCategAEliminar(item)
    setShowEliminarCateg(true)
  }
  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Admin categorias </h1>
          {
            verificarPermiso(rol, "CREAR_CATEGORIA") &&
            <div className="actions">
              <Link to="/admin/categorias/crear" className="btn btn-lg btn-primary" style={!verificarPermiso(rol, "CREAR_CATEGORIA") ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }} > Nueva Categoria </Link>   </div>
          }

        </div>
        <Alert />
        <div className="contentPage card">
          <section id="aplicacioens">
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">Nombre</th>
                    {
                      (verificarPermiso(rol, "EDITAR_CATEGORIA") || verificarPermiso(rol, "ELIMINAR_CATEGORIA")) &&
                      <th scope="col">Acciones</th>
                    }
                  </tr>
                </thead>
                <tbody>
                  {categoriasListParcial?.map((item) => {
                    return <tr key={item.id}>
                      <td>{item.nombre}</td>
                      { (verificarPermiso(rol, "EDITAR_CATEGORIA")|| verificarPermiso(rol, "ELIMINAR_CATEGORIA")) &&
                      <td>
                        <div className="table-actions">
                          {
                            verificarPermiso(rol, "EDITAR_CATEGORIA") &&
                            <Link
                              title='EDITAR'
                              to="/admin/categorias/editar"
                              onClick={() => { dispatch(setCategoriaSeleccionado(item)) }}
                            ><i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                            </Link>
                          }
                          {
                            verificarPermiso(rol, "ELIMINAR_CATEGORIA") &&
                            <a href={null} role='button' onClick={() => onEliminar(item)} title='ELIMINAR'>
                              <i className="material-icons-outlined" style={{ "color": "grey" }}> delete_forever </i>
                            </a>
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
      <ModalEliminarItems setShowEliminar={setShowEliminarCateg} showEliminar={showEliminarCateg} handleEliminar={handleEliminar} />
    </div>
  )
}

export default PaginaCategorias;
