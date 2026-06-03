import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../FastAPI/static',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/items': 'http://localhost:8000',
    },
  },
})
