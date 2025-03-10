import { useEffect } from "react";
import CategoriaCard from "../components/CategoriaCard";
import { axiosGetCategorias } from '../reducers/Categorias/actions';
import { useDispatch, useSelector } from 'react-redux';

export default function Categorias() {
  const {categorias}=useSelector(state=>state.Categoria)
  const dispatch=useDispatch()
  useEffect(()=>{
    dispatch(axiosGetCategorias())
  },[])
  return (
    <div className="dashboardContent">
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Categorias </h1>
        </div>
        {categorias.map((categoria) => (
          <CategoriaCard 
            key={categoria.id} 
            title={categoria.nombre} 
            categoryId={categoria.id}
          />
        ))}
      </div>
    </div>
  );
}
