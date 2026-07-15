<template>
  <div class="app-layout">
    <Sidebar :is-open="sidebarOpen" />
    <div class="main-area">
      <Navbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="content-area">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import Navbar from '../components/Navbar.vue'
import { useAuthStore } from '../store'

const sidebarOpen = ref(false)
const auth = useAuthStore()

onMounted(() => {
  if (auth.token && !auth.user) {
    auth.fetchMe()
  }
})
</script>
