import React from 'react';
import Post from '../components/Post';
import { useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom'; // Importa useParams
import { axiosGetContenido } from '../reducers/Contenido/actions';
import { axiosGetUsuarios } from '../reducers/Usuarios/actions';

export default function PostPage() {
  const { contenido } = useSelector(state => state.Contenido);
  const dispatch = useDispatch()
  const { postId } = useParams()
  const { usuarios } = useSelector(state => state.Usuario)

  useEffect(() => {
    dispatch(axiosGetContenido())
    dispatch(axiosGetUsuarios())
  }, []);
  const contenidoFiltrado = contenido?.filter((content) => content.id == postId);
  return (
    <>

      {contenidoFiltrado.map((content) => (
        <Post
          key={content.id}
          title={content.titulo}
          text={content.cuerpo}
          autor={content.autor}
          fecha={content.fecha}
          comentarios={content.lista_comentarios}
        />
      ))}

    </>
  )
}
