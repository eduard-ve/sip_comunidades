// Setup for Vitest
import { beforeAll } from 'vitest'

// Mock import.meta.env globally
Object.defineProperty(global, 'import', {
  value: {
    meta: {
      env: {
        VITE_API_BASE_URL: 'http://localhost:8000/api'
      }
    }
  },
  writable: false,
  configurable: true
})

// Mock Vue Router globally
global.vi.mock('vue-router', () => ({
  createRouter: global.vi.fn(() => ({
    push: global.vi.fn(),
    replace: global.vi.fn(),
    go: global.vi.fn(),
    back: global.vi.fn(),
    forward: global.vi.fn()
  })),
  createWebHistory: global.vi.fn(),
  RouterLink: {
    template: '<a><slot></slot></a>',
    props: ['to']
  },
  RouterView: {
    template: '<div><slot></slot></div>'
  },
  useRouter: global.vi.fn(() => ({
    push: global.vi.fn(),
    replace: global.vi.fn(),
    go: global.vi.fn(),
    back: global.vi.fn(),
    forward: global.vi.fn()
  })),
  useRoute: global.vi.fn(() => ({
    path: '/',
    name: 'home',
    params: {},
    query: {},
    hash: ''
  }))
}))

// Setup for Vue 3 tests
import { createPinia } from 'pinia'
import { createApp } from 'vue'

beforeAll(() => {
  // Global test setup
  // Create a mock Pinia instance for tests
  const pinia = createPinia()
  const app = createApp({})
  app.use(pinia)
  global.pinia = pinia
})

// Global stubs for Vue components
global.testStubs = {
  // Vue Router components
  'router-link': {
    template: '<a><slot></slot></a>',
    props: ['to']
  },
  'router-view': {
    template: '<div><slot></slot></div>'
  },
  
  // Application components
  'navbar': true,
  'sidebar': true,
  'Navbar': true,
  'Sidebar': true,
  'BaseModule': true,
  'DataTable': true,
  'AuditTable': true,
  'UserForm': true,
  
  // Missing component stubs
  'KpiCard': {
    template: '<div class="kpi-card"><slot></slot></div>',
    props: ['title', 'value', 'change', 'icon', 'colorIcon', 'colorBorder']
  },
  'ChartPanel': {
    template: '<div class="chart-panel"><slot></slot></div>',
    props: ['data', 'options', 'type', 'height', 'chartId', 'noCard']
  }
}