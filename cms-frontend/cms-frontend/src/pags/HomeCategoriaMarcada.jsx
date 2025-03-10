import { useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom'; // Importa useParams
import { axiosFiltrarContenido, axiosGetContenido } from '../reducers/Contenido/actions';
import PostCard from "../components/PostCard";
import { axiosGetCategorias } from "../reducers/Categorias/actions";

export default function HomeCategoriaMarcada() {
  const { contenido } = useSelector(state => state.Contenido);
  const {categorias}=useSelector(state=>state.Categoria);
  const dispatch = useDispatch();
  const { categoryId } = useParams(); // Obtiene categoryId de la URL
  useEffect(() => {
    dispatch(axiosFiltrarContenido({ categoria_id: categoryId, estado:"aprobado" })); // Filtra contenido por categoryId
  }, []);
  useEffect(() => {dispatch(axiosGetCategorias())}, []);

  return (
    <div className="dashboardContent">
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Post de categoria: </h1>
        </div>
        {contenido.map((content) => (
          <div key={content.id} className="contentPage card">
            <PostCard
              key={content.id}
              title={content.titulo}
              text={content.cuerpo}
              postId={content.id}
              categoryId={categorias?.find(categoria => categoria.subcategorias?.find(subcategoria => subcategoria.id === content.subcategoria))?.id}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
