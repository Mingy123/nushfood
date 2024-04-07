import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import CNN from '../views/CNN.vue'
import Segment from '../views/Segment.vue'
import FoodResult from '../views/FoodResult.vue'
import DrinkResult from '../views/DrinkResult.vue'

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
    {
      path: '/food/result',
      name: 'Food Result',
      component: FoodResult,
      props: (route) => ({ rawData: route.query.rawData }), 
    },
    {
      path: '/drink',
      name: 'Drink Detection',
      component: CNN,
    },
    {
      path: '/drink/result',
      name: 'Drink Result',
      component: DrinkResult,
      props: (route) => ({ rawData: route.query.rawData }), 
    },
  ]
})

export default router
