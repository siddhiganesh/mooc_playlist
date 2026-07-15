<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <div class="sidebar-logo">🎓</div>
      <div>
        <div class="sidebar-brand">LearnHub</div>
        <div class="sidebar-subtitle">MOOC Platform</div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="sidebar-section-title">Main</div>
      <router-link
        v-for="item in mainItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-link"
        active-class="active"
      >
        <span class="sidebar-link-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>

      <div class="sidebar-section-title">Learn</div>
      <router-link
        v-for="item in learnItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-link"
        active-class="active"
      >
        <span class="sidebar-link-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>

      <div class="sidebar-section-title">Account</div>
      <router-link
        v-for="item in accountItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-link"
        active-class="active"
      >
        <span class="sidebar-link-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <div class="sidebar-user">
        <div class="sidebar-user-avatar">{{ userInitial }}</div>
        <div style="flex:1; min-width:0;">
          <div class="sidebar-user-name">{{ user?.full_name || user?.username || 'User' }}</div>
          <div class="sidebar-user-role">{{ user?.points || 0 }} points</div>
        </div>
        <button @click="logout" title="Logout" style="color: rgba(255,255,255,0.6); font-size: 18px;">⏻</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store'

const props = defineProps({ isOpen: Boolean })

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const user = computed(() => auth.user)
const userInitial = computed(() => {
  const n = auth.user?.full_name || auth.user?.username || 'U'
  return n.charAt(0).toUpperCase()
})

const mainItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '🏠' },
  { to: '/my-courses', label: 'My Courses', icon: '📚' },
  { to: '/playlists', label: 'Video Playlists', icon: '▶️' },
  { to: '/ai-summarizer', label: 'AI Summarizer', icon: '🤖' },
  { to: '/subtitles', label: 'Subtitles', icon: '💬' }
]
const learnItems = [
  { to: '/assignments', label: 'Assignments', icon: '📝' },
  { to: '/quizzes', label: 'Quizzes', icon: '❓' },
  { to: '/test', label: 'Test', icon: '📊' },
  { to: '/notes', label: 'Notes', icon: '🗒️' },
  { to: '/discussion', label: 'Discussion Forum', icon: '💭' }
]
const accountItems = [
  { to: '/certificates', label: 'Certificates', icon: '🏆' },
  { to: '/leaderboard', label: 'Leaderboard', icon: '🥇' },
  { to: '/messages', label: 'Messages', icon: '✉️' },
  { to: '/profile', label: 'Profile', icon: '👤' },
  { to: '/settings', label: 'Settings', icon: '⚙️' },
  { to: '/help', label: 'Help', icon: '❔' }
]

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
