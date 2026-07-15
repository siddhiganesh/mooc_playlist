<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">🥇 Leaderboard</h1>
      <p class="page-subtitle">Top learners on LearnHub</p>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else class="leaderboard-list">
      <div v-for="u in users" :key="u.id" class="lb-item" :class="{ you: u.is_you }">
        <div class="lb-rank" :class="u.rank === 1 ? 'gold' : u.rank === 2 ? 'silver' : u.rank === 3 ? 'bronze' : ''">
          {{ u.rank === 1 ? '🥇' : u.rank === 2 ? '🥈' : u.rank === 3 ? '🥉' : u.rank }}
        </div>
        <div class="post-avatar">{{ u.username.charAt(0).toUpperCase() }}</div>
        <div class="lb-info">
          <div class="lb-name">{{ u.full_name || u.username }} {{ u.is_you ? '(You)' : '' }}</div>
          <div class="lb-stats">🏆 {{ u.certificates }} certs · 📚 {{ u.courses_completed }} courses</div>
        </div>
        <div class="lb-points">⭐ {{ u.points }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const users = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/leaderboard')
    users.value = data.leaderboard
  } catch (e) { /* empty */ }
  loading.value = false
})
</script>
