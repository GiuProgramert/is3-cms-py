import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearRol, axiosGetPermisos, axiosModificarRol, verificarPermiso } from '../reducers/Roles/actions'
import { setRol } from '../reducers/Roles'
import { setIsError } from '../reducers/Alert'
import { Alert } from '../components/Alert'

export const PaginaRolesCrear = () => {
  //const permisosUsuario=useSelector(state=>{return state.Rol.rolSeleccionado.permisos})
  //const permiso=permisosUsuario.some(permiso=>permiso.codigo==="ROL_EDITAR")
  const [errores, setErrores] = useState({});
  const { roles } = useSelector(state => state.Rol)
  const { rol } = useSelector(state => state.Sesion)
  const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
  const permisos = useSelector(state => state.Rol.permisos)
  const [rolForm, setRolForm] = useState({
    nombre: "",
    permisos: []
  })
  const [activePermisos, setActivePermisos] = useState(rolForm.permisos);
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [editar, setEditar] = useState(false)
  const handleChangeForm = ({ target }) => {
    setRolForm({
      ...rolForm,
      [target.name]: target.value
    })
  }


  useEffect(() => {
    dispatch(axiosGetPermisos())
  }
    , [])
  const handleCahngePermiso = (permiso) => {
    const index = rolForm.permisos.findIndex((r) => r === Number(permiso));
    if (index >= 0) {
      const newPermisoList = [...rolForm.permisos];
      newPermisoList.splice(index, 1);
      setRolForm({
        ...rolForm,
        permisos: newPermisoList
      })
    } else {
      setRolForm({
        ...rolForm,
        permisos: [...rolForm.permisos, Number(permiso)]
      })
    }
  };
  const validate = () => {
    let validateStatus = true;
    let errors = {}
    if (!rolForm["nombre"]) {
      validateStatus = false
      errors["nombre"] = "Nombre es un campo requerido"
      setErrores({
        ...errores,
        errorMessages: errors
      })
    }
    if (rolForm.permisos.length === 0) {
      validateStatus = false
      errors["permisos"] = "Permisos es un campo requerido"
      setErrores({
        ...errores,
        errorMessages: errors
      })
    }

    return validateStatus

  }
  const handleDispatch = (e) => {
    if (!validate()) {
      e.preventDefault();
    } else {
      dispatch(axiosCrearRol(rolForm,navigate))
    }
  }
  const handleCancelar = () => {
    dispatch(setRol({}))
    navigate("/Roles")
  }

  return (
    <div className="dashboardContent">
      <div className="container-fluid">
        <div className="sectionHeader">
          <h1 className="page-title"> Crear Rol</h1>

          <div className="actions">
            {editar === false ?
              <a href={null} onClick={() => { if (verificarPermiso(rol,"CREAR_ROL")) { setEditar(true) } else { dispatch(setIsError("Solo el usuario con rol de admin puede crear un rol.")) } }} className="btn btn-lg btn-primary" >
                <span className="material-icons-outlined"> edit </span> Crear
              </a>
              :
              <>
                <Link to="/admin/roles" onClick={handleCancelar} className="btn btn-lg btn-cancel"> Cancelar </Link>
                <Link to="/admin/roles" onClick={handleDispatch} className="btn btn-lg btn-primary"> Guardar </Link>
              </>
            }
          </div>
        </div>
        <Alert />
        <div className="contentPage card">
          <form action="" className="">

            <div className="form-col-4">

              <div className="form-group md-input">
                <input className="form-control md-form-control" required={true} type="text" placeholder=" " value={rolForm.nombre} onChange={handleChangeForm} name='nombre' disabled={!editar} />
                <label className="md-label"> Nombre del rol <span>*</span></label>
                {errores.errorMessages &&
                  <p style={{ color: "red" }}>{errores.errorMessages.nombre}</p>
                }
              </div>

            </div>

            <div className="checkboxes-list">
              {
                errores.errorMessages &&
                <p style={{ color: "red" }}>{errores.errorMessages.permisos}</p>
              }
              {permisos.map((item, index) => {
                return < div className="form-check form-switch" key={index} >
                  <label className="form-check-label" htmlFor="activeSwitch"> {item.nombre} </label>
                  <input className="form-check-input" type="checkbox" role="switch" id="activeSwitch" checked={rolForm.permisos?.some((r) => r === item.id)} onChange={() => handleCahngePermiso(item.id)} disabled={!editar} />
                </div>
              }
              )}

            </div>

          </form>
        </div>

      </div >
    </div >
  )
}
