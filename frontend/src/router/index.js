import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../stores/auth.js'

// Layout principal
import MainLayout from '../components/layouts/MainLayout.vue'

// Vistas
import Login from '../views/usuarios/Login.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import GestionPoblacional from '../views/poblacional/GestionPoblacional.vue'
import GestionSalud from '../views/salud/GestionSalud.vue'
import GestionSocial from '../views/social/GestionSocial.vue'
import GestionEncuestas from '../views/encuestas/GestionEncuestas.vue'
import ResponderEncuesta from '../views/encuestas/ResponderEncuesta.vue'
import Reportes from '../views/reportes/Reportes.vue'
import UsuariosRoles from '../views/usuarios/UsuariosRoles.vue'
import Auditoria from '../views/auditoria/Auditoria.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/encuesta/:token', name: 'ResponderEncuesta', component: ResponderEncuesta },

  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Home',
        component: Dashboard,
        meta: { allowedRoles: ['admin', 'editor', 'invitado'] }
      },
      {
        path: 'poblacion',
        name: 'GestionPoblacional',
        component: GestionPoblacional,
        meta: { allowedRoles: ['admin', 'editor'] }
      },
      {
        path: 'salud',
        name: 'GestionSalud',
        component: GestionSalud,
        meta: { allowedRoles: ['admin', 'editor'] }
      },
      {
        path: 'social',
        name: 'GestionSocial',
        component: GestionSocial,
        meta: { allowedRoles: ['admin', 'editor'] }
      },
      {
        path: 'encuestas',
        name: 'GestionEncuestas',
        component: GestionEncuestas,
        meta: { allowedRoles: ['admin', 'editor'] }
      },
      {
        path: 'reportes',
        name: 'Reportes',
        component: Reportes,
        meta: { allowedRoles: ['admin', 'editor', 'invitado'] }
      },
      {
        path: 'usuarios',
        name: 'UsuariosRoles',
        component: UsuariosRoles,
        meta: { allowedRoles: ['admin'] }
      },
      {
        path: 'auditoria',
        name: 'Auditoria',
        component: Auditoria,
        meta: { allowedRoles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard para control de acceso basado en roles
router.beforeEach((to, from, next) => {
  const { isAuthenticated, hasRole, initAuth } = useAuth()

  // Inicializar autenticación desde localStorage
  initAuth()

  // Verificar si la ruta requiere autenticación
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated.value) {
      // Usuario no autenticado, redirigir a login
      next('/login')
      return
    }

    // Verificar roles permitidos
    if (to.meta.allowedRoles) {
      if (!hasRole(to.meta.allowedRoles)) {
        // Usuario no tiene el rol requerido, redirigir al dashboard
        next('/dashboard')
        return
      }
    }
  }

  // Si el usuario está autenticado y trata de ir a login, redirigir al dashboard
  if (to.path === '/login' && isAuthenticated.value) {
    next('/dashboard')
    return
  }

  next()
})

export default router
