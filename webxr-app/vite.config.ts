import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
  ],
  server: {
    host: true,
    allowedHosts: true,
    proxy: {
      '/generate_image': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      },
      '/generate_model': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      },
      '/images': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      },
      '/models': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      },
    }
  }
})
