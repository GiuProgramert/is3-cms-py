import moment from 'moment';
import React, { useEffect, useState } from 'react'
// import QRCode from 'qrcode.react';
import Comments from './Comments';
import EmojiPicker, { Emoji } from 'emoji-picker-react';
import { useDispatch, useSelector } from 'react-redux';
// import Comments from './Comments';
import { Modal } from 'react-bootstrap';
import { axiosGetUsuarios } from '../reducers/Usuarios/actions';
import { axiosGetContenidoById } from '../reducers/Contenido/actions';
import { useParams } from 'react-router-dom';
import {Alert} from "../components/Alert";
import axios from 'axios';
const contarReacciones = (lista) => {
  const contador = {};

  lista.forEach((emoji) => {
    contador[emoji] = (contador[emoji] || 0) + 1;
  });

  return contador;
};
const Post = (props) => {
  const { titulo, cuerpo, autor, fecha, lista_comentarios }=useSelector(state=>state.Contenido.contenidoSeleccionado)
  const { postId: idPost } = useParams(); 
  const dispatch = useDispatch()
  const { usuarios } = useSelector(state => state.Usuario)
  const { id } = useSelector((state) => state.Sesion)
  const userId = id // Asumiendo que tienes el usuario actual en tu store 
  console.log("El ID del usuario es: ", userId)
  const [likes, setLikes] = useState(0);
  const [hasLiked, setHasLiked] = useState(false);
  const [listaReacciones, setListaReacciones] = useState([
    "1f923", "1f60d", "1f636-200d-1f32b-fe0f", "1f60d"
  ])
  const [contadorReacciones, setContadorReacciones] = useState(contarReacciones(listaReacciones))
  const [emojiSelected, setEmojiSelected] = useState("")
  const handleEmoji = (emojiData, event) => {
    setEmojiSelected(emojiData.unified)
  }
  useEffect(() => {
    setContadorReacciones(contarReacciones(listaReacciones))
  }, [listaReacciones])
  const [show, setShow] = useState(false)

  useEffect(() => {
    dispatch(axiosGetUsuarios())
    dispatch(axiosGetContenidoById(idPost))
    if (idPost && userId) {
      registrarVista(idPost, userId);
    }
    
  }, [])
  useEffect(() => {

    const commentTitleElement = document.querySelector('.comment-title');
    const postBtnElement = document.querySelector('.postBtn');
    const postCommentElement = document.querySelector('.postComment');
    if (commentTitleElement) {
      commentTitleElement.textContent = 'Comentarios';
    }

    if (postBtnElement) {
      postBtnElement.textContent = 'Comentar';
    }
    if (postCommentElement) {
      postCommentElement.placeholder = 'Escribe un comentario';
    }

  }, [])
  useEffect(() => {
    // Obtener el número de likes y si el usuario ya ha dado like
    axios.get(`http://127.0.0.1:8000/likes/contenido/${idPost}/`)
      .then(response => {
        setLikes(response.data.length);
        setHasLiked(response.data.some(like => like.usuario === userId));
      });
  }, [idPost, userId]);

  const registrarVista = async (contenido_id, usuario_id) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/registrar_vista/', {
        contenido_id,
        usuario_id,
      });
      console.log(response.data.message); // Mensaje de éxito o si ya se ha registrado
      
    } catch (error) {
      console.error("Error registrando vista:", error);
    }
  };
  
  const handleLike = () => {
    if (hasLiked) {
      console.log("SI ha dado like")
      // Si ya ha dado like, eliminarlo
      axios.delete(`http://127.0.0.1:8000/likes/delete/${idPost}/${userId}/`)
        .then(() => {
          setLikes(likes - 1);
          setHasLiked(false);
        });
    } else {
      console.log("No ha dado like")
      // Si no ha dado like, crearlo
      axios.post('http://127.0.0.1:8000/likes/', {
        contenido: idPost,
        usuario: userId
      })
      .then(() => {
        setLikes(likes + 1);
        setHasLiked(true);
      });
    }
  };
  return (
    <div className='dashboardContent'>
      <div className="container-fluid">
        <div className="contentPage card">
          <div className="sectionHeader">
            <h1 className="page-title">{titulo}</h1>
          </div>
          <Alert/>
          <h1 className='page-autor'>Autor: </h1><p>{usuarios?.find(user => user.id === autor)?.username}</p>
          <h1 className='page-autor'>Fecha: </h1> <p>{moment(fecha).format('L')}</p>
          <div className='post'>
            <div dangerouslySetInnerHTML={{ __html: cuerpo }}></div>
          </div>
          {/* <p>Reacciones:</p>
          <div className='actions'>
            {Object.entries(contadorReacciones).map(([emoji, cantidad], index) => (
              <div key={index}>
                <Emoji unified={emoji} /><span className='emoji-count'>{cantidad}</span>
              </div>
            ))}
          </div> */}
          {/* <div className='actions'>
            <button className='btn btn-lg btn-tertiarity' onClick={() => { setShow(true) }}>Reaccionar</button>
          </div>
          <div >*/}
          <div className='like-section'>
            <button onClick={handleLike} className={`btn ${hasLiked ? 'btn-danger' : 'btn-primary'}`}>
              {hasLiked ? 'Quitar Me gusta' : 'Me gusta'}
            </button>
            <span>{likes} Me gusta</span>
          </div>
          <Comments comentarios={lista_comentarios} />
          {/* </div> */}
          {/* <div className="actions-header"> */}
          {/* <h1>Compartir:</h1> */}
          {/* <QRCode value={window.location.href} renderAs="canvas" /> */}
          {/* <FacebookShareButton url={window.location.href} quote={`lee-todo-sobre-${title}`}><FacebookIcon /></FacebookShareButton>
            <TwitterShareButton url={window.location.href} quote={`lee-todo-sobre-${title}`}><TwitterShareButton /></TwitterShareButton>
            <WhatsappShareButton url={window.location.href} quote={`lee-todo-sobre-${title}`}><WhatsappIcon /></WhatsappShareButton> */}
          {/* </div> */}
        </div>

      </div>
      <Modal show={show} onHide={() => { setShow(false) }}>
        <Modal.Body>
          <div style={{ "alignItems": "center" }}>
            <EmojiPicker onEmojiClick={(emoji, event) => handleEmoji(emoji, event)} />
            <p>Seleccionado: </p><Emoji unified={emojiSelected} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button className='btn btn-lg btn-secondary' onClick={() => { setShow(false) }}>Cancelar</button>
          <button className='btn btn-lg btn-primary' onClick={() => { setListaReacciones([...listaReacciones, emojiSelected]); setShow(false) }}>Elegir</button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

export default Post;