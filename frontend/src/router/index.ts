import { createRouter, createWebHistory } from 'vue-router'

import AboutView from '../views/AboutView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/about', name: 'about', component: AboutView },
  ],
})

export default router

