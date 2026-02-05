import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
    plugins: [
        react({
            jsxImportSource: "@emotion/react",
        }), 
        tsconfigPaths()
    ],
    server: {
        host: '0.0.0.0',
        port: 3000,
        strictPort: true,
    },
    build: {
        outDir: 'build',
        sourcemap: true,
    },
    resolve: {
        alias: {
            '@/': '/src/',
        },
    },
})
