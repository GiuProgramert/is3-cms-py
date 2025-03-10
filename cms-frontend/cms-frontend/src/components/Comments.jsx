import React, { useEffect } from 'react';
import { CommentSection } from 'react-comments-section';
import 'react-comments-section/dist/index.css';
import { useDispatch, useSelector } from 'react-redux';
import { axiosComentarContenido, axiosEditarComentario, axiosEliminarComentario } from '../reducers/Contenido/actions';
import { useParams } from 'react-router-dom';

const Comments = ({ comentarios }) => {
  const data = comentarios.map(comment => ({
    ...comment,
    // Clonar profundamente las respuestas también
    replies: Array.isArray(comment.replies) ? comment.replies.map(reply => ({ ...reply })) : []
  }));

  const dispatch = useDispatch();
  const { username, id, isLogged, profile_pic } = useSelector((state) => state.Sesion);
  const { postId: idPost } = useParams();

  return (
    <CommentSection
      replyTop={false}
      customNoComment={() => <div>No hay comentarios aún</div>}
      currentUser={isLogged && username ? {
        currentUserId: id,
        currentUserImg: profile_pic,
        currentUserProfile: '',
        currentUserFullName: username,
      } : null}
      logIn={{
        loginLink: `${window.location.origin}/#/login-page`,
        signupLink: `${window.location.origin}/#/register-page`,
      }}
      commentData={data}
      onSubmitAction={(newComment) => {
        // Clona el comentario antes de enviarlo al backend
        const clonedComment = { ...newComment, replies: [] };

        // Enviar el comentario mediante una acción de Redux
        dispatch(axiosComentarContenido(clonedComment.text, idPost, id, profile_pic, null));
      }}
      onReplyAction={(replyData) => {
        // Clona la respuesta antes de enviarla
        const clonedReply = { ...replyData };

        // Enviar la respuesta mediante una acción de Redux
         dispatch(axiosComentarContenido(clonedReply.text, idPost, id, profile_pic, clonedReply.repliedToCommentId));
      }}
      onEditAction={(editedData) => {

         dispatch(axiosEditarComentario(editedData.comId, idPost,editedData.text,profile_pic,id,editedData.parentOfEditedCommentId));
        // Aquí podrías agregar lógica para manejar la edición del comentario
      }}
      onDeleteAction={(deletedData) => {

        dispatch(axiosEliminarComentario(deletedData.comIdToDelete, idPost));
      }}
      currentData={(currentComments) => {
        // Si necesitas guardar o procesar los comentarios actuales
        // console.log('Current comments data: ', currentComments);
      }}
    />
  );
};

export default Comments;
