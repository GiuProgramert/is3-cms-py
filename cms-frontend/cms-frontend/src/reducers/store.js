import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import {thunk} from "redux-thunk";
import Sesion from "./Sesion";
import storage from "redux-persist/lib/storage";
import persistReducer from "redux-persist/es/persistReducer";
import persistStore from "redux-persist/es/persistStore";
import Alert from "./Alert";
import Usuarios from "./Usuarios";
import Roles from "./Roles";
import Categorias from "./Categorias";
import Contenido from "./Contenido";

export const baseUrl = "http://localhost:8000"
const persistConfig = {
    key: 'root',
    storage,
}
const sesionPersistConfig = {
    key: 'Sesion',
    storage,
    whitelist: ['username', 'rol', 'id']
}
const UsuarioPersistConfig={
    key:'Usuario',
    storage,
    whitelist:['usuarioSeleccionado']
}
const RolPersistConfig={
    key:'Rol',
    storage,
    whitelist:['rolSeleccionado','roles']
}
const CategoriaPersistConfig={
    key:'Categoria',
    storage,
    whitelist:['categoriaSeleccionado']
}
const ContenidoPersistConfig={
    key:'Contenido',
    storage,
    whitelist:['contenidoSeleccionado']
}
const rootReducer = combineReducers({
    Sesion: persistReducer(sesionPersistConfig, Sesion),
    Alert: Alert,
    Usuario: persistReducer(UsuarioPersistConfig,Usuarios),
    Rol:persistReducer(RolPersistConfig,Roles),
    Categoria: persistReducer(CategoriaPersistConfig,Categorias),
    Contenido: persistReducer(ContenidoPersistConfig,Contenido),
})
const persistedReducer = persistReducer(persistConfig, rootReducer)
export const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
          serializableCheck: {
            ignoredActions: ["persist/PERSIST"],
            ignoredPaths: ["persist/PERSIST"],
          },
        }),
});
export const persistor = persistStore(store);
export const disqusShortname = "CMS_GRUPO_2"