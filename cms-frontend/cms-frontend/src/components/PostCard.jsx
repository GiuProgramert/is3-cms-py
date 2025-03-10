import React from 'react';
import { useDispatch } from 'react-redux';
import { Link } from "react-router-dom";
import { setContenidoSeleccionado } from '../reducers/Contenido';
import { axiosGetContenidoById } from '../reducers/Contenido/actions';

const PostCard = ({ title, text, postId, categoryId, resumen }) => {
  // Limitar el texto a 150 caracteres
  const limitedText = text.length > 150 ? text.slice(0, 150) + '...' : text;
  const dispatch = useDispatch();
  return (
    <>
      <div className="sectionHeader">
        <h2 className="page-subtitle"> {title} </h2>
      </div>
      <p>{resumen}</p>

      <Link to={`/public/post/${categoryId}/${postId}`} id='post-btn' className="btn btn-lg btn-primary" onClick={() => { dispatch(axiosGetContenidoById(postId))}}>
        <span className="material-icons-outlined"> add </span>Ver más
      </Link>

    </>
  );
};

export default PostCard;
