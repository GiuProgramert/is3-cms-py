import React from 'react';
import { Link } from 'react-router-dom';

const CategoriaCard = ({ title, categoryId }) => {
  
  return (
    <div className="contentPage card">
      <div className="sectionHeader">
        <h2 className="page-subtitle"> {title} </h2>
      </div>
      <Link
        to={`/public/feed-categoria/${categoryId}`} // Pasa el ID de la categoría en la URL
        id='post-btn'
        className="btn btn-lg btn-primary"
      >
        <span className="material-icons-outlined"> add </span>Ver contenidos
      </Link>
    </div>
  );
};

export default CategoriaCard;
