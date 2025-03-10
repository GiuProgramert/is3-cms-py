import React, { useEffect, useState } from 'react'
import { Pagination, Stack } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from "axios"
import { baseUrl } from '../App';
import { useDispatch, useSelector } from 'react-redux';
import { setContenidoSeleccionado } from '../reducers/Contenido';
import { axiosGetContenido } from '../reducers/Contenido/actions';
import { axiosGetCategorias } from '../reducers/Categorias/actions';


const PaginaBorradores = () => {
 const {categorias}=useSelector(state=>state.Categoria)
 const { contenido } = useSelector(state => state.Contenido)
 const [contenidoList, setContenidoList] = useState(contenido)
 const { roles } = useSelector(state => state.Rol)
 const { rol } = useSelector(state => state.Sesion)
 const mostrar = [4, 8, 12, 16]
 const [contenidoListParcial, setListaCategoriaParcial] = useState(contenidoList)
 const [pageCount, setPageCount] = useState(13)
 const [countElementPerPage, setcountElementPerPage] = useState(4)
 const [pageNumber, setPageNumber] = useState(1)
 const dispatch = useDispatch()
 const { id } = useSelector(state => state.Sesion)

 useEffect(() => {
   const filteredContenido = contenido.filter(item => item.estado === "borrador"&& item.autor === id);
   setContenidoList(filteredContenido);
   setListaCategoriaParcial(filteredContenido);
 }, []);

 useEffect(() => {
   setcountElementPerPage(4)
   setPageNumber(1)
   setPageCount(Math.ceil(contenidoList?.length / 4));
 }, [contenidoList])

 const handleChangeCount = (event, value) => {
   setPageNumber(value)
   setListaCategoriaParcial(contenidoList?.slice((value - 1) * countElementPerPage, (value - 1) * countElementPerPage + countElementPerPage))
 };

 const handlePageCount = (event, value) => {
   setPageNumber(1)
   setcountElementPerPage(Number(event.target.value))
   setListaCategoriaParcial(contenidoList?.slice(0, event.target.value))
   setPageCount(Math.ceil(contenidoList?.length / event.target.value));
 };

  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Borrador </h1>
          <div className="actions">
            
          </div>
        </div>
        {/* <Alert /> */}
        <div className="contentPage card">
          <section id="aplicacioens">
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">Titulo</th>
                    <th scope="col">Categoria</th>
                    <th scope="col">Autor</th>
                    <th scope="col">Fecha</th>
                    <th scope="col">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {contenidoListParcial?.map((item) => {
                    return <tr key={item.id}>
                      <td>{item.titulo}</td>
                      <td>{categorias?.find(cat=>cat.id===item.categoria)?.nombre}</td>
                      <td>{item.autor}</td>
                      <td>{item.fecha}</td>
                      {
                        // rol === 1 &&
                        <td>
                          <div className="table-actions">
                            <Link
                              title='EDITAR'
                              to="/admin/contenido/editar"
                              onClick={() => { dispatch(setContenidoSeleccionado(item)) }}
                            ><i className="material-icons-outlined" style={{ "color": "grey" }}> edit </i>
                            </Link>
                            {/* <a href={null} role='button' onClick={() => handleEliminar(item)} title='ELIMINAR'>
                              <i className="material-icons-outlined" style={{ "color": "grey" }}> delete_forever </i>
                            </a> */}
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

export default PaginaBorradores;
