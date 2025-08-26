import { createRouter, createWebHistory } from 'vue-router'

// Layout principal
import MainLayout from '../layouts/MainLayout.vue'

// Vistas
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import GestionPoblacional from '../views/GestionPoblacional.vue'
import GestionSalud from '../views/GestionSalud.vue'
import GestionSocial from '../views/GestionSocial.vue'
import GestionEncuestas from '../views/GestionEncuestas.vue'
import Reportes from '../views/Reportes.vue'
import UsuariosRoles from '../views/UsuariosRoles.vue'
import Auditoria from '../views/Auditoria.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },

  {
    path: '/',
    component: MainLayout,
    children: [
      { path: 'dashboard', name: 'Home', component: Dashboard },
      { path: 'poblacion', name: 'GestionPoblacional', component: GestionPoblacional },
      { path: 'salud', name: 'GestionSalud', component: GestionSalud },
      { path: 'social', name: 'GestionSocial', component: GestionSocial },
      { path: 'encuestas', name: 'GestionEncuestas', component: GestionEncuestas },
      { path: 'reportes', name: 'Reportes', component: Reportes },
      { path: 'usuarios', name: 'UsuariosRoles', component: UsuariosRoles },
      { path: 'auditoria', name: 'Auditoria', component: Auditoria }
    ]
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
