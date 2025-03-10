import { createSlice } from '@reduxjs/toolkit';
const estadoInicial= {
    isLogged:false,
    username:"",
    rol:[],
    id:"",
    email:"",
    profile_pic:""
}
const SesionSlice = createSlice({
    name: 'Sesion',
    initialState:estadoInicial,
    reducers: {
        setSesion:(state,{payload})=>{
            state.isLogged=true
            state.username=payload.username
            state.rol=payload.rol
            state.id=payload.id
            state.email=payload.email
            state.profile_pic=payload.profile_pic
        },
        setCerrarSesion:(state)=>{
            state.isLogged=false
            state.username=""
            state.rol=[]
            state.id=""
            state.email=""
            state.profile_pic=""
        }
    }
});
export const { setSesion,setCerrarSesion } = SesionSlice.actions;
export default SesionSlice.reducer;