import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosCrearUsuario } from '../reducers/Usuarios/actions'
import { permisos, roles } from './PaginaUsuariosEditar'
import { axiosGetRoles, verificarPermiso } from '../reducers/Roles/actions'

export const PaginaUsuariosCrear = () => {
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const permiso = permisos.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const { roles } = useSelector(state => state.Rol)
    const { rol } = useSelector(state => state.Sesion)
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const [usuarioForm, setUsuarioForm] = useState({
        username: "",
        email: "",
        roles: []
    })

    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleCancelar = () => {
        setEditar(false)
        localStorage.removeItem('usuario')
    }
    const handleChange = ({ target }) => {
        setUsuarioForm({
            ...usuarioForm,
            [target.name]: target.value
        })
    }
    const validate = () => {
        let validateStatus = true;
        let errors = {}
        if (!usuarioForm.username) {
            validateStatus = false
            errors["username"] = "Username es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (!usuarioForm.email) {
            validateStatus = false
            errors["email"] = "Email es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        if (usuarioForm.roles.length < 1) {
            validateStatus = false
            errors["roles"] = "Rol es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus
    }
    const handleGuardarCambios = (e) => {
        if (validate()) {
            dispatch(axiosCrearUsuario(usuarioForm,navigate))
        }
    }
    const handleRoleChange = (roleId) => {
        const updatedRoles = usuarioForm.roles.includes(roleId)
            ? usuarioForm.roles.filter(id => id !== roleId) // Remueve el rol si ya está seleccionado
            : [...usuarioForm.roles, roleId]; // Agrega el rol si no está seleccionado

        setUsuarioForm({
            ...usuarioForm,
            roles: updatedRoles, // Actualiza el array de roles
        });
    };
    useEffect(() => {
        dispatch(axiosGetRoles())
    }, [])
    
    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="sectionHeader">
                    <h1 className="page-title"> Crear usuario </h1>
                    {editar === false ?
                        <div className='actions'>
                            <a href={null} onClick={() => { setEditar(true) }} className="btn btn-lg btn-primary" style={!verificarPermiso(rol, "CREAR_USUARIO") ? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }}>
                                <span className="material-icons-outlined"> edit </span> Crear
                            </a>
                        </div>
                        :
                        <div className='actions'>
                            <Link to="/admin/usuarios" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                            <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios}>Guardar usuario </button>
                        </div>
                    }
                </div>
                {/* <Alert /> */}
                <div className="contentPage card">
                    <div className='form-col-4'>
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="text" onChange={handleChange} name="username" value={usuarioForm.username} disabled={!editar} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.username}</p>
                            }
                            <label className="md-label">Username<span>*</span></label>
                        </div>
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="text" onChange={handleChange} name="email" value={usuarioForm.email} disabled={!editar} />
                            {errores.errorMessages &&
                                <p style={{ color: "red" }}>{errores.errorMessages.email}</p>
                            }
                            <label className="md-label">Email<span>*</span></label>
                        </div>
                    </div>
                    <div className="checkboxes-list">
                        <label style={{ "color": "#1565D8", "fontSize": "12px" }}>Roles</label>
                        {roles.map((item, index) => {
                            return (
                                <div className="form-check form-switch" key={index}>
                                    <label className="form-check-label" htmlFor={`switch-${item.id}`}>
                                        {item.nombre}
                                    </label>
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        id={`switch-${item.id}`}
                                        checked={usuarioForm.roles.includes(item.id)} // Verifica si el rol está seleccionado
                                        onChange={() => handleRoleChange(item.id)}
                                        disabled={!editar}
                                    />
                                </div>
                            );
                        })}
                        {errores.errorMessages && (
                            <p style={{ color: "red" }}>{errores.errorMessages.roles}</p>
                        )}
                    </div>

                </div>
            </div>
        </div>

    )
}