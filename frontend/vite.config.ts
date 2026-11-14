import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import cesium from 'vite-plugin-cesium'

// Support both ESM default and direct callable
const cesiumPlugin = typeof cesium === 'function' ? cesium : (cesium as unknown as { default: () => any }).default

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    cesiumPlugin()
  ],
  server: {
    port: 5173,
    host: true
  }
})
