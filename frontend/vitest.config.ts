import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    include: ['**/*.test.js'],
    globals: true,
    environment: 'happy-dom',
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
