import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
    coverage: {
      reporter: ['text', 'lcov'],
      reportsDirectory: './coverage',
      include: ['src/**/*.{js,vue,ts}'],
      exclude: [
        'src/test/**',
        '**/*.test.js',
        '**/*.spec.js',
        'src/main.js',
        'src/router/**',
        'node_modules/**'
      ],
      all: true,
      thresholds: {
        global: {
          branches: 0,
          functions: 0,
          lines: 0,
          statements: 0
        }
      }
    }
  }
})