import { createSlice } from '@reduxjs/toolkit';
const usuarioSlice = createSlice({
    name: 'usuario',
    initialState: {
        usuarios:[],
        usuarioSeleccionado:{}
    },
    reducers: {
        setUsuarios: (state, {payload}) => {
            state.usuarios =payload;
        },
        setUsuarioSeleccionado:(state,{payload})=>{
            state.usuarioSeleccionado=payload
        }
    }
});
export const { setUsuarioSeleccionado,setUsuarios } = usuarioSlice.actions;
export default usuarioSlice.reducer;