import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { persistor, store } from './reducers/store.js'
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import { GoogleOAuthProvider } from '@react-oauth/google';

createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId='734286294575-bi6jgibm4kv05dtchc2egmk53daiuhin.apps.googleusercontent.com'>
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      {/* <StrictMode> */}
        <App />
      {/* </StrictMode> */}
    </PersistGate>
  </Provider>
  </GoogleOAuthProvider>,
)
