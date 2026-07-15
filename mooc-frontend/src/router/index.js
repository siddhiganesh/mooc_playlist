import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'my-courses', name: 'MyCourses', component: () => import('../views/MyCourses.vue') },
      { path: 'playlists', name: 'VideoPlaylists', component: () => import('../views/VideoPlaylists.vue') },
      { path: 'ai-summarizer', name: 'AISummarizer', component: () => import('../views/AISummarizer.vue') },
      { path: 'subtitles', name: 'Subtitles', component: () => import('../views/Subtitles.vue') },
      { path: 'assignments', name: 'Assignments', component: () => import('../views/Assignments.vue') },
      { path: 'quizzes', name: 'Quizzes', component: () => import('../views/Quizzes.vue') },
      { path: 'test', name: 'Test', component: () => import('../views/Test.vue') },
      { path: 'notes', name: 'Notes', component: () => import('../views/Notes.vue') },
      { path: 'discussion', name: 'Discussion', component: () => import('../views/Discussion.vue') },
      { path: 'certificates', name: 'Certificates', component: () => import('../views/Certificates.vue') },
      { path: 'leaderboard', name: 'Leaderboard', component: () => import('../views/Leaderboard.vue') },
      { path: 'messages', name: 'Messages', component: () => import('../views/Messages.vue') },
      { path: 'profile', name: 'Profile', component: () => import('../views/Profile.vue') },
      { path: 'settings', name: 'Settings', component: () => import('../views/Settings.vue') },
      { path: 'help', name: 'Help', component: () => import('../views/Help.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) next('/login')
  else if (to.meta.guest && auth.token) next('/dashboard')
  else next()
})

export default router
