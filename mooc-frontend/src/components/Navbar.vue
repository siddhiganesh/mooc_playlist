<template>
  <header class="navbar">
    <div class="flex items-center gap-3">
      <button class="navbar-icon-btn" @click="$emit('toggle-sidebar')" style="display:none;">☰</button>
      <h2 class="navbar-title">{{ pageTitle }}</h2>
    </div>
    <div class="navbar-actions">
      <div class="navbar-search">
        <span>🔍</span>
        <input v-model="search" placeholder="Search courses, videos..." @keyup.enter="doSearch" />
      </div>
      <button class="navbar-icon-btn" title="Notifications">
        🔔<span class="dot" v-if="hasNotif"></span>
      </button>
      <button class="navbar-icon-btn" title="Messages" @click="$router.push('/messages')">✉️</button>
      <div class="sidebar-user-avatar" style="width:36px;height:36px;background:linear-gradient(135deg,var(--primary),var(--secondary));color:white;display:flex;align-items:center;justify-content:center;border-radius:50%;font-weight:700;cursor:pointer;" @click="$router.push('/profile')">
        {{ userInitial }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store'

defineEmits(['toggle-sidebar'])

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const search = ref('')
const hasNotif = ref(true)

const pageTitle = computed(() => {
  const map = {
    Dashboard: 'Dashboard',
    MyCourses: 'My Courses',
    VideoPlaylists: 'Video Playlists',
    AISummarizer: 'AI Summarizer',
    Subtitles: 'Subtitles',
    Assignments: 'Assignments',
    Quizzes: 'Quizzes',
    Test: 'Tests',
    Notes: 'My Notes',
    Discussion: 'Discussion Forum',
    Certificates: 'Certificates',
    Leaderboard: 'Leaderboard',
    Messages: 'Messages',
    Profile: 'My Profile',
    Settings: 'Settings',
    Help: 'Help & Support'
  }
  return map[route.name] || 'LearnHub'
})

const userInitial = computed(() => {
  const n = auth.user?.full_name || auth.user?.username || 'U'
  return n.charAt(0).toUpperCase()
})

const doSearch = () => {
  if (search.value.trim()) {
    router.push({ path: '/my-courses', query: { search: search.value.trim() } })
  }
}
</script>
