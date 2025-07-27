import { createRouter, createWebHistory } from 'vue-router'
import ProjectDashboard from '@/views/ProjectDashboard.vue'
import ProjectDetail from '@/views/ProjectDetail.vue'
import About from '@/views/About.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ProjectDashboard
    },
    {
      path: '/project/:id',
      name: 'project-detail',
      component: ProjectDetail,
      props: true
    },
    {
      path: '/about',
      name: 'about',
      component: About
    }
  ]
})

export default router