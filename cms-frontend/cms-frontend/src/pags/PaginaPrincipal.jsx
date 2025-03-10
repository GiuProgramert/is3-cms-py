import React, { useEffect } from 'react';
import Feed from '../components/Feed';
import { useDispatch } from 'react-redux';
import { axiosGetCategorias } from '../reducers/Categorias/actions';

const PaginaPrincipal = () => {
  const dispatch=useDispatch()
  useEffect(() => {
    dispatch(axiosGetCategorias())
  }, [])
  
  return (
    <>
      <div className="pagina-principal">
        <Feed/>
      </div>
    </>
  );
};

export default PaginaPrincipal;
