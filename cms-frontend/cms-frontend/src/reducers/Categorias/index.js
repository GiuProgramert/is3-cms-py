import { createSlice } from '@reduxjs/toolkit';
const categoriaSlice = createSlice({
    name: 'categoria',
    initialState: {
        categorias:[],
        categoriaSeleccionado:{}
    },
    reducers: {
        setCategorias: (state, {payload}) => {
            state.categorias =payload;
        },
        setCategoriaSeleccionado:(state,{payload})=>{
            state.categoriaSeleccionado=payload
        }
    }
});
export const { setCategoriaSeleccionado,setCategorias } = categoriaSlice.actions;
export default categoriaSlice.reducer;