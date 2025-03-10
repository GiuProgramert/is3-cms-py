import React from 'react';

const ProtectedComponent = () => {
  return (
    <div>
      <h1>Este es un componente protegido</h1>
      <p>Solo es accesible si el usuario está autenticado.</p>
    </div>
  );
};

export default ProtectedComponent;
