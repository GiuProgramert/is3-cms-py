import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'global': 'window', // Permite que el objeto global sea accesible en el navegador
  },
  // Configura Vite para manejar archivos adicionales si es necesario
  server: {
    port: 3000,
  },
  base:"/"
})
