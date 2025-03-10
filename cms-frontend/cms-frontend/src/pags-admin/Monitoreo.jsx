import React, { useEffect, useState } from 'react'

import { axiosContarEstados, axiosContenidosConMasLikes, axiosGetContenidosMasVistos, axiosGetContenidosTop5 } from '../reducers/Contenido/actions';
import { useDispatch, useSelector } from 'react-redux';
import { clearContenidoMasLikes, clearEstados, setContenidosMasVistos, setContenidosTop5 } from '../reducers/Contenido';
import moment from 'moment';
import { Grid } from '@mui/material';
import { CanvasCustomChart } from '../components/CanvasCustomChart';
export const formatDate = (date) => {
    return moment(date).format("YYYY-MM-DD")
}

export const Monitoreo = () => {
    const dispatch = useDispatch();
    const contenidosEstados = useSelector(state => state.Contenido.estados)
    const contenidoMaslikes = useSelector(state => state.Contenido.constenidoMasLikes)
    const contenidosTop5 = useSelector(state => state.Contenido.contenidosTop5)
    const contenidosMasVistos = useSelector(state => state.Contenido.contenidosMasVistos)
    const [fechaInicioEstados, setFechaInicioEstados] = useState(() => {
        const date = new Date();
        date.setMonth(date.getMonth() - 6);
        return date;
    });
    const [fechaFinEstados, setFechaFinEstados] = useState(new Date());
    useEffect(() => {
        if (fechaInicioEstados && fechaFinEstados) {
            dispatch(clearEstados())
            dispatch(axiosContarEstados(formatDate(fechaInicioEstados), formatDate(fechaFinEstados)));
            dispatch(axiosGetContenidosMasVistos(formatDate(fechaInicioEstados), formatDate(fechaFinEstados)))
        }
    }, [fechaInicioEstados, fechaFinEstados])
    useEffect(() => {
        dispatch(clearContenidoMasLikes())
        dispatch(axiosContenidosConMasLikes());
        dispatch(axiosGetContenidosTop5())
    }, [])
    const handleFecha = ({ target }) => {
        if (target.name === "fechaInicioEstados") setFechaInicioEstados(target.value)
        if (target.name === "fechaFinEstados") setFechaFinEstados(target.value)
    }

    return (
        <div className='dashboardContent'>
            <div className="container-fluid">
                <div className="sectionHeader">
                    <h1 className="page-title"> Reportes </h1>
                    <div className="actions">
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="date" name="fechaInicioEstados" onChange={handleFecha} value={formatDate(fechaInicioEstados)} />
                            <label className="md-label"> Fecha inicio</label>
                        </div>
                        <div className="form-group md-input">
                            <input className="form-control md-form-control" type="date" name="fechaFinEstados" onChange={handleFecha} value={formatDate(fechaFinEstados)} />
                            <label className="md-label"> Fecha fin</label>
                        </div>
                    </div>
                </div>
                <div className="contentPage">
                    <div className="dashboard-home">
                        <Grid container spacing={3} >
                            <Grid item xs={12} md={6}>
                                <CanvasCustomChart
                                    title={`Contenidos con más likes`}
                                    data={contenidoMaslikes ? contenidoMaslikes.map((item, index) => ({
                                        y: item.num_likes,
                                        label: item.titulo
                                    })) : []
                                    }
                                    type={"area"}
                                    width={"100%"}
                                    height={"300px"}
                                />
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <CanvasCustomChart
                                    title={`Contenidos desde: ${moment(fechaInicioEstados).format("DD/MM/YYYY")} hasta: ${moment(fechaFinEstados).format("DD/MM/YYYY")}`}
                                    data={contenidosEstados ? Object.keys(contenidosEstados).map((key, index) => ({
                                        y: contenidosEstados[key],
                                        label: key
                                    })) : []}
                                    type={"column"}
                                    width={"100%"}
                                    height={"300px"}
                                />
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <CanvasCustomChart
                                    title={`Top 5 contenidos más vistos`}
                                    data={contenidosTop5 ? contenidosTop5.map((item, index) => ({
                                        y: item.num_vistas,
                                        label: item.titulo
                                    })) : []
                                    }
                                    type={"bar"}
                                    width={"100%"}
                                    height={"300px"}
                                />
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <CanvasCustomChart
                                    title={`Contenidos más vistos desde: ${moment(fechaInicioEstados).format("DD/MM/YYYY")} hasta: ${moment(fechaFinEstados).format("DD/MM/YYYY")}`}
                                    data={contenidosMasVistos ? contenidosMasVistos.map((item, index) => ({
                                        y: item.total_vistas,
                                        label: item.titulo
                                    })) : []
                                    }
                                    type={"pie"}
                                    width={"100%"}
                                    height={"300px"}
                                />
                            </Grid>
                        </Grid>
                    </div>
                </div>
            </div>
        </div>
    )
}
