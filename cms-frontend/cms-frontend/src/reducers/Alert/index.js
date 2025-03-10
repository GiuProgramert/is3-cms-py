import { createSlice } from '@reduxjs/toolkit';
export const AlertSlice = createSlice({
    name: 'Alert',
    initialState: {
        isOk:false,
        isLoading:false,
        isError:false,
        error:"",
        message:""
    },
    reducers: {
        setIsLoading: (state, {payload} ) => {
            state.isLoading=payload
        },
        setIsOk:(state,{payload})=>{
            state.isLoading=false
            state.isOk=true
            state.message=payload
        },
        setIsError:(state,{payload})=>{
            state.isLoading=false
            state.isError=true
            state.error=payload
        },
        clearStates:(state)=>{
            state.isOk=false
            state.isLoading=false
            state.isError=false
            state.error=""
        }
    }
});
export const { setIsLoading,setIsError,setIsOk,clearStates } = AlertSlice.actions;
export default AlertSlice.reducer;