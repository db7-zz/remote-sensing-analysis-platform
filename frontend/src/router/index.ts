import { createRouter, createWebHistory } from 'vue-router'

import AboutView from '../views/AboutView.vue'
import AnalysisView from '../views/AnalysisView.vue'
import DashboardView from '../views/DashboardView.vue'
import HistoryView from '../views/HistoryView.vue'
import TaskDetailView from '../views/TaskDetailView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/analysis', name: 'analysis', component: AnalysisView },
    { path: '/tasks', name: 'tasks', component: HistoryView },
    { path: '/tasks/:id', name: 'task-detail', component: TaskDetailView },
    { path: '/about', name: 'about', component: AboutView },
  ],
})

export default router
