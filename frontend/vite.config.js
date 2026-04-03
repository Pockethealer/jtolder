// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Output the build files directly into the backend folder
    outDir: '../backend/static',
    // Wipe the folder clean before every new build
    emptyOutDir: true
  }
})
