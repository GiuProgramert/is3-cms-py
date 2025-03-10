import { createSlice } from '@reduxjs/toolkit';
const RolSlice = createSlice({
    name: 'Rol',
    initialState: {
        roles:[],
        rolSeleccionado:{},
        permisos:[]
    },
    reducers: {
        setRoles: (state, {payload}) => {
            state.roles=payload
        },
        setRol:(state,{payload})=>{
            state.rolSeleccionado=payload
        },
        setPermisos:(state,{payload})=>{
            state.permisos=payload
        }
    }
});
export const { setRol,setRoles ,setPermisos} = RolSlice.actions;
export default RolSlice.reducer;