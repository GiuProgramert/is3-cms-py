import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { axiosModficarUsuario } from '../reducers/Usuarios/actions'
import { setIsError } from '../reducers/Alert'
import { Alert } from '../components/Alert'
import { verificarPermiso } from '../reducers/Roles/actions'


export const permisos = [
    {
        "id": 1,
        "nombre": "VER_CONTENIDO"
    },
    {
        "id": 2,
        "nombre": "EDITAR_CONTENIDO"
    },
    {
        "id": 3,
        "nombre": "PUBLICAR_CONTENIDO"
    },
    {
        "id": 4,
        "nombre": "RECHAZAR_CONTENIDO"
    },
    {
        "id": 5,
        "nombre": "CREAR_USUARIO"
    },
    {
        "id": 6,
        "nombre": "EDITAR_USUARIO"
    },
    {
        "id": 7,
        "nombre": "ELIMINAR_USUARIO"
    },
    {
        "id": 8,
        "nombre": "EDITAR_ROL"
    },
    {
        "id": 9,
        "nombre": "CREAR_ROL"
    },
    {
        "id": 10,
        "nombre": "COMENTAR"
    },
    {
        "id": 11,
        "nombre": "EDITAR_PERFIL"
    },
    {
        "id": 12,
        "nombre": "PUNTEAR"
    }
]
export const roles = [
    {
        "id": 2,
        "permisos": [
            {
                "id": 5,
                "nombre": "CREAR_USUARIO"
            },
            {
                "id": 6,
                "nombre": "EDITAR_USUARIO"
            }
        ],
        "nombre": "autor"
    },
    {
        "id": 3,
        "permisos": [
            {
                "id": 1,
                "nombre": "VER_CONTENIDO"
            },
            {
                "id": 4,
                "nombre": "RECHAZAR_CONTENIDO"
            }
        ],
        "nombre": "editor"
    },
    {
        "id": 4,
        "permisos": [
            {
                "id": 7,
                "nombre": "ELIMINAR_USUARIO"
            }
        ],
        "nombre": "publicador"
    },
    {
        "id": 5,
        "permisos": [
            {
                "id": 9,
                "nombre": "CREAR_ROL"
            }
        ],
        "nombre": "suscriptor"
    },
    {
        "id": 1,
        "permisos": [
            {
                "id": 1,
                "nombre": "VER_CONTENIDO"
            },
            {
                "id": 6,
                "nombre": "EDITAR_USUARIO"
            }
        ],
        "nombre": "ADMIN"
    },
    {
        "id": 6,
        "permisos": [
            {
                "id": 1,
                "nombre": "VER_CONTENIDO"
            },
            {
                "id": 6,
                "nombre": "EDITAR_USUARIO"
            }
        ],
        "nombre": "Tester"
    }
]
export const PaginaUsuariosEditar = () => {
    const [editar, setEditar] = useState(false)
    const [errores, setErrores] = useState({})
    const { usuarioSeleccionado } = useSelector(state => state.Usuario)
    const permiso = permisos.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const [usuarioForm, setUsuarioForm] = useState(usuarioSeleccionado)
    const { roles } = useSelector(state => state.Rol)
    const { rol } = useSelector(state => state.Sesion)
    const rolNombre = roles?.find((rolItem) => rolItem.id === rol)?.nombre
    const dispatch = useDispatch()
    const navigate = useNavigate()
    // const permiso = usuarioForm.ro.some(permiso => permiso.nombre === "EDITAR_USUARIO")
    const [passwords, setPasswords] = useState({
        password: "",
        newPassword: "",
        confirmNewPassword: ""
    })
    const handleCancelar = () => {
        setEditar(false)
        localStorage.removeItem('usuario')
    }
    const handleChange = ({ target }) => {
        if (target.name === "password" || target.name === "newPassword" || target.name === "confirmNewPassword") {
            setPasswords({
                ...passwords,
                [target.name]: target.value
            })
        } else {
            setUsuarioForm({
                ...usuarioForm,
                [target.name]: target.value
            })
        }

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
        if (usuarioForm.roles<1) {
            validateStatus = false
            errors["roles"] = "Roles es un campo requerido"
            setErrores({
                ...errores,
                errorMessages: errors
            })
        }
        return validateStatus
    }
    const handleGuardarCambios = (e) => {

        if (validate()) {
            dispatch(axiosModficarUsuario(usuarioForm, navigate))
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
    return (
        <>
            <div className='dashboardContent'>
                <div className="container-fluid">
                    <div className="sectionHeader">
                        <h1 className="page-title"> Editar Usuario </h1>
                        {editar === false ?
                            <div className='actions'>
                                <a href={null} onClick={() => { if (!verificarPermiso(rol,"EDITAR_USUARIO")) { dispatch(setIsError("Solo el usuario con rol de admin puede editar un usuario.")) } else { setEditar(true) } }} className="btn btn-lg btn-primary" style={!verificarPermiso(rol,"EDITAR_USUARIO")? { "pointerEvents": "none", "cursor": "default", "backgroundColor": "lightGrey" } : { "color": "white" }}>
                                    <span className="material-icons-outlined"> edit </span> Editar
                                </a>
                            </div>
                            :
                            <div className='actions'>
                                <Link to="/admin/usuarios" className="btn btn-lg btn-cancel" onClick={handleCancelar}> Cancelar </Link>
                                <button className="btn btn-lg btn-primary" onClick={handleGuardarCambios}>Guardar usuario </button>
                            </div>
                        }
                    </div>
                    <Alert />
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
        </>
    )
}