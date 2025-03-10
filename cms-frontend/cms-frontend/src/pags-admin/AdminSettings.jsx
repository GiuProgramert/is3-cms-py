import React, { useEffect, useState } from 'react'
import { Button, Form, Modal, Row } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { axiosFiltrarContenido, axiosGetContenido, axiosGetHistorial } from '../reducers/Contenido/actions';
import { setContenidoSeleccionado } from '../reducers/Contenido';
import { Link } from "react-router-dom"
import { axiosGetUsuarios } from '../reducers/Usuarios/actions';
import { axiosGetCategorias } from '../reducers/Categorias/actions';
import { Alert } from '../components/Alert'
import { verificarPermiso } from '../reducers/Roles/actions';
import moment from 'moment';
export default function AdminSettings() {
  const { rol } = useSelector(state => state.Sesion)
  const [borrador, setBorrador] = useState([]);
  const [enRevision, setEnRevision] = useState([]);
  const [publicado, setPublicado] = useState([]);
  const [rechazado, setRechazado] = useState([]);
  const [inactivo, setInactivo] = useState([])
  const [edicion, setEdicion] = useState([])
  const contenidos = useSelector(state => state.Contenido.contenido)
  const [historial, sethistorial] = useState([])
  const [showFiltro, setShowFiltro] = useState(false)
  const { categorias } = useSelector(state => state.Categoria)
  const dispatch = useDispatch()
  const { usuarios } = useSelector(state => state.Usuario)
  const autores = usuarios?.filter(user => user.rol === 4)
  const [verHistorial, setVerHistorial] = useState(false)
  const handleSelectAuthor = (author) => {
    setSelectedAuthor(author);
    setFilterState({
      ...filterState,
      autor: author.nombre
    })
  }
  const initialFilterState = {
    autor: "",
    categoria_id: "",
    subcategoria_id: "",
    fecha: ""
  }
  const [filterState, setFilterState] = useState(initialFilterState)
  const [selectedAuthor, setSelectedAuthor] = useState(null);
  const handleFilter = ({ target }) => {
    setFilterState({
      ...filterState,
      [target.name]: target.value
    })
  }
  const onFilter = () => {
    setBorrador([])
    setEnRevision([])
    setPublicado([])
    setRechazado([])
    dispatch(axiosFiltrarContenido({ ...filterState }))
    setShowFiltro(false)
  }

  const organizarContenidos = () => {
    setBorrador([])
    setEnRevision([])
    setPublicado([])
    setRechazado([])
    setInactivo([])
    contenidos.forEach((contenido) => {
      switch (contenido.estado) {
        case 'borrador':
          setBorrador((prevState) => [...prevState, contenido]);
          break;
        case 'en_revision':
          setEnRevision((prevState) => [...prevState, contenido]);
          break;
        case 'aprobado':
          setPublicado((prevState) => [...prevState, contenido]);
          break;
        case 'rechazado':
          setRechazado((prevState) => [...prevState, contenido]);
          break;
        case 'inactivo':
          setInactivo((prevState) => [...prevState, contenido]);
          break;
        case 'edicion':
          setEdicion((prevState) => [...prevState, contenido]);
          break;
        default:
          break;
      }
    });
  };
  const handleLimpiarTodo = () => {
    if (JSON.stringify(filterState) !== JSON.stringify(initialFilterState)) {
      setFilterState(initialFilterState)
      dispatch(axiosFiltrarContenido(initialFilterState))
    }

  }
  const handleLimpiarFilter = ({ target }) => {
    setFilterState({
      ...filterState,
      [target.name]: ""
    })
    dispatch(axiosFiltrarContenido({
      ...filterState,
      [target.name]: ""
    }))
  }
  useEffect(() => {
    dispatch(axiosGetContenido())
    dispatch(axiosGetUsuarios())
    dispatch(axiosGetCategorias())
  }, [])
  useEffect(() => {
    organizarContenidos();
  }, [contenidos])

  const formatearFecha = (fecha) => {
    let date = new Date(fecha)
    let day = date.getDate()
    let month = date.getMonth() + 1
    let year = date.getFullYear()
    return `${day}/${month}/${year}`
  }

  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Kanban </h1>
        </div>
        <Alert />
        {/* <!-- Filtros --> */}
        <section id="filtros">
          <span className="title"> Filtros activos </span>
          <div className="section-filtros">
            {filterState.autor &&
              <button className="label-filtro" name="autor" onClick={handleLimpiarFilter}>Autor: {filterState.autor}</button>
            }
            {filterState.fecha &&
              <button className="label-filtro" name="fecha" onClick={handleLimpiarFilter}>Fecha: {filterState.fecha}</button>
            }
            {filterState.categoria_id &&
              <button className="label-filtro" name="categoria_id" onClick={handleLimpiarFilter}>Categoria:{categorias.find(categ => categ.id === Number(filterState.categoria_id))?.nombre}</button>
            }
            {filterState.subcategoria_id &&
              <button className="label-filtro" name="subcategoria_id" onClick={handleLimpiarFilter}>Subcategoria:{categorias.find(categ => categ.id === Number(filterState.categoria_id))?.subcategorias.find(sub => sub.id === Number(filterState.subcategoria_id))?.nombre}</button>
            }
            <a role="button" className="btn btn-filter" onClick={() => { setShowFiltro(true) }} > <span className="material-icons-outlined"> filter_list </span> Filtrado avanzado </a>
            <a role="button" onClick={handleLimpiarTodo} style={{ "color": "#0c56d0" }}> Limpiar filtros </a>
          </div>
        </section>
        <div className="contentPage card">
          <div className='tablero-kanban '>
            <div className="column">
              <h2>Borrador</h2>
              {borrador.map((contenido, index) => (
                <div key={index}>
                  <h1 className='page-autor'>{contenido.titulo}</h1>
                  <strong>Categoría:</strong><p>{categorias?.find(categ => categ.id === contenido.categoria)?.nombre}</p>
                  <p>Autor: {usuarios?.find(user => user.id === contenido.autor)?.username}</p>
                  <div className='actions'>
                    {verificarPermiso(rol, "EDITAR_CONTENIDO") && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/editar"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='EDITAR' className="material-icons-outlined"> edit </span></Link>}
                    <button className="btn btn-secondary btn-md btn-floating" onClick={() => { sethistorial(contenido.historiales), setVerHistorial(true) }}>
                      <span class="material-icons-outlined">
                        history
                      </span></button>
                  </div>
                </div>
              ))}
            </div>
            <div className="column">
              <h2>Revisión</h2>
              {enRevision.map((contenido, index) => (
                <div key={index}>
                  <h1 className='page-autor'>{contenido.titulo}</h1>
                  {/* <p>Categoría: {categorias?.find(categ => categ.id === contenido.categoria)?.nombre}</p> */}
                  <p>Autor: {usuarios?.find(user => user.id === contenido.autor)?.username}</p>
                  <div className='actions'>
                    {(verificarPermiso(rol, "EDITAR_CONTENIDO")) && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/editar"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='EDITAR' className="material-icons-outlined"> edit </span></Link>}
                    {(verificarPermiso(rol, "PUBLICAR_CONTENIDO") || verificarPermiso(rol, "RECHAZAR_CONTENIDO")) && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/publicador"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='REVISAR' className="material-icons-outlined"> find_in_page </span></Link>}
                    <button className="btn btn-secondary btn-md btn-floating" onClick={() => { sethistorial(contenido.historiales), setVerHistorial(true) }}>
                      <span className="material-icons-outlined" title='HISTORIAL'>
                        history
                      </span></button>
                  </div>
                </div>
              ))}
            </div>
            <div className="column">
              <h2>Publicado</h2>
              {publicado.map((contenido, index) => (
                <div key={index}>
                  <h1 className='page-autor'>{contenido.titulo}</h1>
                  {/* <p>Categoría: {categorias?.find(categ => categ.id === contenido.categoria)?.nombre}</p> */}
                  <p>Autor: {usuarios?.find(user => user.id === contenido.autor)?.username}</p>
                  {/* {rol === 2 && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/editar"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='EDITAR' className="material-icons-outlined"> edit </span></Link>} */}
                  {/* <a href={null} role='button' className={"btn btn-secondary btn-md btn-floating"}  onClick={() => { setVerHistorial(true);dispatch(axiosGetHistorial(contenido.id))}}><span title='HISTORIAL' className="material-icons-outlined"> visibility </span></a> */}
                  <div className='actions'>
                    {(verificarPermiso(rol, "PUBLICAR_CONTENIDO") || verificarPermiso(rol, "RECHAZAR_CONTENIDO")) && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/publicador"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='REVISAR' className="material-icons-outlined"> find_in_page </span></Link>}
                    <button className="btn btn-secondary btn-md btn-floating" onClick={() => { sethistorial(contenido.historiales), setVerHistorial(true) }}>
                      <span className="material-icons-outlined" title='HISTORIAL'>
                        history
                      </span></button>
                  </div>
                </div>
              ))}
            </div>
            <div className="column">
              <h2>Rechazado</h2>
              {rechazado.map((contenido, index) => (
                <div key={index}>
                  <h1 className='page-autor'>{contenido.titulo}</h1>
                  {/* <p>Categoría: {categorias?.find(categ => categ.id === contenido.categoria)?.nombre}</p> */}
                  <p>Autor: {usuarios?.find(user => user.id === contenido.autor)?.username}</p>
                  <div className='actions'>
                    {verificarPermiso(rol, "EDITAR_CONTENIDO") && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/editar"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='EDITAR' className="material-icons-outlined"> edit </span></Link>}
                    {(verificarPermiso(rol, "PUBLICAR_CONTENIDO") || verificarPermiso(rol, "RECHAZAR_CONTENIDO")) && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/publicador"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='REVISAR' className="material-icons-outlined"> find_in_page </span></Link>}
                    <button className="btn btn-secondary btn-md btn-floating" onClick={() => { sethistorial(contenido.historiales), setVerHistorial(true) }}>
                      <span className="material-icons-outlined" title='HISTORIAL'>
                        history
                      </span></button>
                  </div>
                </div>
              ))}
            </div>
            <div className="column">
              <h2>Inactivo</h2>
              {inactivo.map((contenido, index) => (
                <div key={index}>
                  <h1 className='page-autor'>{contenido.titulo}</h1>
                  {/* <p>Categoría: {categorias?.find(categ => categ.id === contenido.categoria)?.nombre}</p> */}
                  <p>Autor: {usuarios?.find(user => user.id === contenido.autor)?.username}</p>

                  {/* {rol === 2 && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/editar"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='EDITAR' className="material-icons-outlined"> edit </span></Link>} */}
                  <div className='actions'>
                    {(verificarPermiso(rol, "PUBLICAR_CONTENIDO") || verificarPermiso(rol, "RECHAZAR_CONTENIDO")) && <Link className={"btn btn-secondary btn-md btn-floating"} to={"/admin/contenido/publicador"} onClick={() => { dispatch(setContenidoSeleccionado(contenido)) }}><span title='REVISAR' className="material-icons-outlined"> find_in_page </span></Link>}
                    <button className="btn btn-secondary btn-md btn-floating" onClick={() => { sethistorial(contenido.historiales), setVerHistorial(true) }}>
                      <span className="material-icons-outlined" title='HISTORIAL'>
                        history
                      </span></button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      <Modal
        show={showFiltro}
        onHide={() => setShowFiltro(false)}
        centered
        size='lg'
        className="modal modal-custom fade"
      >
        <Modal.Header className="modal-header" closeButton>
          <Modal.Title className="modal-title">Filtrado avanzado</Modal.Title>
        </Modal.Header>

        <Modal.Body className="modal-body">
          <Form className="form-filtros">
            <Row className="modal-row">
              <div className="form-group md-input">
                <select className="form-control md-select" name="categoria_id" onChange={handleFilter} value={filterState.categoria_id}>
                  <option key={'initial'} value=""></option>
                  {
                    categorias.map((item, index) => (
                      <option key={index} value={item.id}>{item.nombre}</option>
                    ))
                  }
                </select>
                <label className="md-label"> Categoria</label>
              </div>
              <div className="form-group md-input">
                <select className="form-control md-select" name="subcategoria_id" onChange={handleFilter} value={filterState.subcategoria_id} disabled={!filterState?.categoria_id}>
                  <option key={'initial'} value=""></option>
                  {
                    categorias.find(categ => categ.id === Number(filterState.categoria_id))?.subcategorias?.map((item) => (
                      <option key={item.id} value={item.id}>{item.nombre}</option>
                    ))
                  }
                </select>
                <label className="md-label"> Subcategoria</label>
              </div>
              <div className="form-group md-input">
                <input className="form-control md-form-control" type="date" name="fecha" onChange={handleFilter} value={filterState.fecha} />
              </div>
              <div className="form-group md-input">
                <input
                  className="form-control md-form-control"
                  type="text"
                  value={filterState.autor}
                  name="autor"
                  onChange={handleFilter}
                />
                <label className="md-label"> Buscar autor</label>
                <ul>
                  {autores?.filter((author) => author.nombre && author.nombre.toLowerCase().includes(filterState.autor.toLowerCase()))
                    .map((item) => (
                      <li key={item.id} onClick={() => handleSelectAuthor(item)}>
                        {item.nombre}
                      </li>
                    ))}
                </ul>
                {selectedAuthor && (
                  <p>Seleccionaste a: {selectedAuthor.nombre}</p>
                )}
              </div>
            </Row>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowFiltro(false)}>
            Cancelar
          </Button>

          <Button variant="primary" onClick={onFilter}>
            Aplicar Filtros
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal
        show={verHistorial}
        onHide={() => setVerHistorial(false)}
        centered
        className="modal modal-custom fade"
        size='xl'
      >
        <Modal.Header className="modal-header" closeButton>
          <Modal.Title className="modal-title">Historial</Modal.Title>
        </Modal.Header>

        <Modal.Body className="modal-body">
          <Form className="form-filtros">
            <ul className="ulprogress">
              {
                historial.map((item, index) => (
                  <li key={item.id} className={`ulprogress-item current}`}>
                    <div className="item-content">
                      <p style={{ margin: '1rem' }}>{moment(item.fecha_modificacion).format("L")} {moment(item.fecha_modificacion).format("LT")}</p>
                      <p style={{ margin: '1rem' }}>{item.comentario}</p>
                      <p style={{ margin: '1rem' }}>por</p>
                      <p style={{ margin: '1rem' }}> {usuarios.find((user) => {
                        return user.id === item.usuario
                      })?.username}</p>
                    </div>
                  </li>
                ))
              }
            </ul>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={() => setVerHistorial(false)}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
