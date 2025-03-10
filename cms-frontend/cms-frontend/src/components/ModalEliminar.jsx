import React from 'react'
import { Button, Col, Form, Modal } from 'react-bootstrap'

export const ModalEliminarItems = ({showEliminar,setShowEliminar,handleEliminar}) => {
  return (
    <Modal show={showEliminar} onHide={() => setShowEliminar(false)}
    size="xl"
    centered
    className="modal modal-custom fade">
    <Modal.Header className="modal-header" closeButton>
      <Modal.Title className="modal-title">Eliminar</Modal.Title>
    </Modal.Header>
    <Modal.Body className="modal-body">
      <form action="" className="form-filtros">
        <Col className="col">
          <Form.Group className="form-group md-input">
            <p>¿Está seguro que desea eliminar el item?</p>
          </Form.Group>
        </Col>
      </form>
    </Modal.Body>
    <Modal.Footer className="modal-footer">
      <Button variant="link" onClick={() => setShowEliminar(false)}>Cancelar</Button>
      <Button variant="primary" onClick={handleEliminar}>Eliminar</Button>
    </Modal.Footer>
  </Modal>
  )
}
