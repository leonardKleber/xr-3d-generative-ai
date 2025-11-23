import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
  ],
  server: {
    // 1. Ensures the server listens on all IPs (needed for local network/ngrok)
    host: true,

    // 2. THIS IS THE FIX: Disable the host check or allow specific domains
    allowedHosts: true,
    proxy: {
      '/generate': {
        target: 'http://localhost:3001', // Forward to backend
        changeOrigin: true,
        secure: false,
      },
      '/models': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
