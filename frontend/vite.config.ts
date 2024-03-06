import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import viteTsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
  },
  esbuild: {
    include: /\.[jt]sx?$/,
    exclude: [],
    loader: 'jsx',
  },
  resolve: {
    alias: {
      '@/': '/src/',
    },
  },
})
