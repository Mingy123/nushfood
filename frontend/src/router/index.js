import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import Segment from '../views/Segment.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Index,
    },
    {
      path: '/food',
      name: 'Food Detection',
      component: Segment,
    },
  ]
})

export default router
