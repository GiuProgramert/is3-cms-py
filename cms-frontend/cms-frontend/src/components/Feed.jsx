import PostCard from "./PostCard";
import { useEffect, useState } from "react";
import { axiosFiltrarContenido, axiosGetContenido } from '../reducers/Contenido/actions';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Form, Modal, Row } from "react-bootstrap";
import { Alert } from "./Alert";
import { axiosGetUsuarios } from "../reducers/Usuarios/actions";

export default function Feed() {
  const { contenido } = useSelector(state => state.Contenido)
  const { categorias } = useSelector(state => state.Categoria)
  const { usuarios } = useSelector(state => state.Usuario)
  const autores = usuarios?.filter(user => user.rol === 4)
  const [selectedAuthor, setSelectedAuthor] = useState(null);
  const [showFiltro, setShowFiltro] = useState(false)
  const dispatch = useDispatch()
  const initialFilterState = {
    estado: "aprobado",
    autor: "",
    categoria_id: "",
    subcategoria_id: "",
    fecha: ""
  }
  const [filterState, setFilterState] = useState(initialFilterState)
  const handleFilter = ({ target }) => {
    setFilterState({
      ...filterState,
      [target.name]: target.value
    })
  }
  const onFilter = () => {
    dispatch(axiosFiltrarContenido({ ...filterState }))
    setShowFiltro(false)
  }
  useEffect(() => {
    // dispatch(axiosGetContenido())
    dispatch(axiosFiltrarContenido(filterState))
    dispatch(axiosGetUsuarios())
  }, [])
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
  const handleLimpiarTodo = () => {
    if (JSON.stringify(filterState) !== JSON.stringify(initialFilterState)) {
      setFilterState(initialFilterState)
      dispatch(axiosFiltrarContenido(initialFilterState))
    }

  }
  const handleSelectAuthor = (author) => {
    setSelectedAuthor(author);
    setFilterState({
      ...filterState,
      autor: author.nombre
    })
  }
  return (
    <div className="dashboardContent">
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Página principal </h1>
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
              <button className="label-filtro" name="categoria_id" onClick={handleLimpiarFilter}>Categoria:{categorias.find(categ=>categ.id===Number(filterState.categoria_id))?.nombre }</button>
            }
            {filterState.subcategoria_id &&
              <button className="label-filtro" name="subcategoria_id" onClick={handleLimpiarFilter}>Subcategoria:{categorias.find(categ=>categ.id===Number(filterState.categoria_id))?.subcategorias.find(sub=>sub.id===Number(filterState.subcategoria_id))?.nombre }</button>
            }
            <a role="button" className="btn btn-filter" onClick={() => { setShowFiltro(true) }} > <span className="material-icons-outlined"> filter_list </span> Filtrado avanzado </a>
            <a role="button" onClick={handleLimpiarTodo} style={{ "color": "#0c56d0" }}> Limpiar filtros </a>
          </div>
        </section>

        {contenido.map((content) => (
          <div key={content.id} className="contentPage card">
            <PostCard
              title={content.titulo}
              text={content.cuerpo}
              resumen={content.resumen}
              postId={content.id}
              categoryId={categorias?.find(
                (categoria) => categoria.subcategorias?.find(
                  (subcategoria) => subcategoria.id === content.subcategoria
                )
              )?.id} />
          </div>
        ))}
      </div>
      <Modal
        show={showFiltro}
        onHide={() => setShowFiltro(false)}
        centered
        className="modal modal-custom fade"
        size="lg"
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
                  placeholder="Buscar autor por nombre"
                  value={filterState.autor}
                  name="autor"
                  onChange={handleFilter}
                />
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
    </div>
  );
}