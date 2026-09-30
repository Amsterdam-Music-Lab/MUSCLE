import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
import { analyzer } from 'vite-bundle-analyzer'

export default defineConfig({
    plugins: [
        react({
            jsxImportSource: "@emotion/react",
        }), 
        tsconfigPaths(),
        analyzer({analyzerMode: "static"})
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
