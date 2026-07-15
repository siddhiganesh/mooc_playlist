<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">💬 Subtitles</h1>
      <p class="page-subtitle">Browse, search, and study subtitles</p>
    </div>

    <div class="card mb-3">
      <div class="grid" style="grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        <select v-model="selectedVideo" class="form-select" @change="loadSubs">
          <option value="">-- Select video --</option>
          <option v-for="v in videos" :key="v.id" :value="v.id">{{ v.title }}</option>
        </select>
        <select v-model="language" class="form-select" @change="loadSubs">
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="hi">Hindi</option>
        </select>
        <input v-model="searchQuery" class="form-input" placeholder="Search subtitles..." @input="searchSubs" :disabled="!selectedVideo" />
      </div>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="subtitles.length">
      <div class="card">
        <div v-for="s in subtitles" :key="s.id" class="subtitle-line" :class="{ highlight: searchQuery && s.content.toLowerCase().includes(searchQuery.toLowerCase()) }">
          <span class="subtitle-time">{{ formatTime(s.start_time) }}</span>
          <span class="subtitle-text">{{ s.content }}</span>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">💬</div>
      <p>Select a video to view its subtitles</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../services/api'

const videos = ref([])
const subtitles = ref([])
const selectedVideo = ref('')
const language = ref('en')
const searchQuery = ref('')
const loading = ref(false)

const loadVideos = async () => {
  try {
    const { data } = await api.get('/playlists/videos/all')
    videos.value = data.videos
  } catch (e) { /* empty */ }
}

const loadSubs = async () => {
  if (!selectedVideo.value) { subtitles.value = []; return }
  loading.value = true
  try {
    const { data } = await api.get(`/subtitles/video/${selectedVideo.value}`, { params: { language: language.value } })
    subtitles.value = data.subtitles
  } catch (e) { subtitles.value = [] }
  loading.value = false
}

const searchSubs = async () => {
  if (!selectedVideo.value || !searchQuery.value) { loadSubs(); return }
  try {
    const { data } = await api.get(`/subtitles/video/${selectedVideo.value}/search`, { params: { q: searchQuery.value } })
    subtitles.value = data.subtitles
  } catch (e) { /* empty */ }
}

const formatTime = (s) => {
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}

onMounted(loadVideos)
</script>
