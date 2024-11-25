import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    include: ['**/*.test.js', '**/*.test.jsx', '**/*.test.ts', '**/*.test.tsx'],
    globals: true,
    environment: 'happy-dom',
    allowOnly: true,
    coverage: {
      reportsDirectory: 'public/coverage',
      provider: 'v8',
      reporter: ["text", "json-summary"],
      exclude: [
        'node_modules/**',
        'storybook-static/**',
        'src/stories/**',
        'src/config/**',
        'src/**/*.stories.{js,jsx,ts,tsx}',
        'src/index.tsx',
        'src/serviceWorker.js',
        '.pnp.cjs',
        '.pnp.loader.mjs',
        '.storybook/**',
        '.yarn/**',
        'src/util/testUtils/useEffectDebugger.js',
        'src/util/__mocks__/**',
      ],
    },
  },
  resolve: {
    alias: {
      '@/': '/src/',
    },
  },
})
