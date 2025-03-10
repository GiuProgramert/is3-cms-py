import { createSlice } from '@reduxjs/toolkit';
const contenidoSlice = createSlice({
    name: 'contenido',
    initialState: {
        contenido: [],
        contenidoSeleccionado: {},
        historial: [],
        estados: {
            "inactivos": null,
            "en_revision": null,
            "aprobados": null,
            "rechazados": null,
            "total": null
        },
        constenidoMasLikes:[],
        contenidosTop5:[],
        contenidosMasVistos:[]
    },
    reducers: {
        setContenido: (state, { payload }) => {
            state.contenido = payload;
        },
        setContenidoSeleccionado: (state, { payload }) => {
            state.contenidoSeleccionado = payload
        },
        setHistorial: (state, { payload }) => {
            state.historial = payload
        },
        setEstados: (state, { payload }) => {
            state.estados = payload
        },
        clearEstados: (state) => {
            state.estados = {
                "inactivos": null,
                "en_revision": null,
                "aprobados": null,
                "total": null
            }
        },
        setContenidoMasLikes:(state,{payload})=>{
            state.constenidoMasLikes = payload
        },
        clearContenidoMasLikes:(state)=>{
            state.constenidoMasLikes = []
        },
        setContenidosTop5:(state,{payload})=>{
            state.contenidosTop5 = payload
        },
        setContenidosMasVistos:(state,{payload})=>{
            state.contenidosMasVistos = payload
        }
    }
});
export const { setContenidoSeleccionado, setContenido, setHistorial,setEstados,clearEstados,setContenidoMasLikes,clearContenidoMasLikes,setContenidosTop5,setContenidosMasVistos } = contenidoSlice.actions;
export default contenidoSlice.reducer;