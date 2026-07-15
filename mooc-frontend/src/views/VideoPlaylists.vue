<template>
  <div class="view-container">
    <div class="page-header flex justify-between items-center">
      <div>
        <h1 class="page-title">Video Playlists</h1>
        <p class="page-subtitle">Watch lectures and build your own playlists</p>
      </div>
      <button class="btn btn-primary" @click="showCreate = true">+ New Playlist</button>
    </div>

    <div class="grid" style="grid-template-columns: 320px 1fr; gap: 20px;" v-if="!activePlaylist">
      <div>
        <h3 class="mb-3" style="font-size: 16px;">My Playlists</h3>
        <div v-if="playlists.length === 0" class="empty-state">
          <div class="empty-state-icon">📂</div>
          <p class="text-sm">No playlists yet</p>
        </div>
        <div v-for="p in playlists" :key="p.id" class="card card-hover mb-2" style="cursor: pointer;" @click="openPlaylist(p)">
          <div class="flex items-center gap-3">
            <div style="width: 40px; height: 40px; background: rgba(99,102,241,0.1); color: var(--primary); border-radius: 8px; display:flex; align-items:center; justify-content:center; font-size: 18px;">▶</div>
            <div style="flex:1; min-width:0;">
              <div style="font-weight: 600;">{{ p.name }}</div>
              <div class="text-sm text-muted">{{ p.item_count }} videos</div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h3 class="mb-3" style="font-size: 16px;">All Available Videos</h3>
        <div v-if="videos.length" class="grid grid-2">
          <div v-for="v in videos" :key="v.id" class="card card-hover" style="cursor: pointer;" @click="playVideo(v)">
            <div class="flex gap-3">
              <div style="width: 80px; height: 60px; background: var(--bg-main); border-radius: 6px; display:flex; align-items:center; justify-content:center; font-size: 24px;">▶</div>
              <div style="flex:1; min-width:0;">
                <div style="font-weight: 600; font-size: 14px; line-height: 1.3;">{{ v.title }}</div>
                <div class="text-sm text-muted mt-2">{{ v.course_title }}</div>
                <div class="text-sm text-muted">{{ formatTime(v.duration) }}</div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">🎬</div>
          <p>No videos available</p>
        </div>
      </div>
    </div>

    <!-- Active playlist with player -->
    <div v-else>
      <button class="btn btn-secondary mb-3" @click="activePlaylist = null">← Back to playlists</button>
      <div class="video-layout">
        <div>
          <div class="video-player-wrapper">
            <iframe v-if="currentVideo" :src="currentVideo.url" allowfullscreen></iframe>
            <div v-else class="empty-state" style="height:100%; display:flex; align-items:center; justify-content:center; color: white;">Select a video to play</div>
          </div>
          <div class="video-info" v-if="currentVideo">
            <h2 class="video-title">{{ currentVideo.title }}</h2>
            <p class="video-description">{{ currentVideo.description }}</p>
            <div class="flex gap-2 mt-3">
              <button class="btn btn-primary btn-sm" @click="aiSummarize(currentVideo.id)">🤖 AI Summarize</button>
              <button class="btn btn-secondary btn-sm" @click="goSubtitles(currentVideo.id)">💬 Subtitles</button>
              <button class="btn btn-secondary btn-sm" @click="addNote(currentVideo)">🗒️ Add Note</button>
            </div>
          </div>
        </div>
        <div class="playlist-sidebar">
          <h3 style="margin-bottom: 12px;">{{ activePlaylist.name }}</h3>
          <div v-if="playlistVideos.length === 0" class="text-sm text-muted">No videos in this playlist</div>
          <div v-for="(v, idx) in playlistVideos" :key="v.id" class="playlist-item" :class="{ active: currentVideo?.id === v.id }" @click="playVideo(v)">
            <div class="playlist-item-num">{{ idx + 1 }}</div>
            <div class="playlist-item-info">
              <div class="playlist-item-title">{{ v.title }}</div>
              <div class="playlist-item-duration">{{ v.course_title }} · {{ formatTime(v.duration) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <h3 class="mb-3">Create New Playlist</h3>
        <div class="form-group">
          <label class="form-label">Name</label>
          <input v-model="newPlaylist.name" class="form-input" placeholder="My Python Course" />
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea v-model="newPlaylist.description" class="form-textarea"></textarea>
        </div>
        <div class="flex gap-3 justify-between">
          <button class="btn btn-secondary" @click="showCreate = false">Cancel</button>
          <button class="btn btn-primary" @click="createPlaylist">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const playlists = ref([])
const videos = ref([])
const showCreate = ref(false)
const newPlaylist = ref({ name: '', description: '' })
const activePlaylist = ref(null)
const playlistVideos = ref([])
const currentVideo = ref(null)

const load = async () => {
  try {
    const { data } = await api.get('/playlists')
    playlists.value = data.playlists
  } catch (e) { /* empty */ }
  try {
    const { data } = await api.get('/playlists/videos/all')
    videos.value = data.videos
  } catch (e) { /* empty */ }
}

const openPlaylist = async (p) => {
  activePlaylist.value = p
  try {
    const { data } = await api.get(`/playlists/${p.id}`)
    playlistVideos.value = data.videos
    if (data.videos.length) currentVideo.value = data.videos[0]
  } catch (e) { /* empty */ }
}

const playVideo = (v) => { currentVideo.value = v }

const createPlaylist = async () => {
  if (!newPlaylist.value.name) return
  try {
    const { data } = await api.post('/playlists', newPlaylist.value)
    playlists.value.unshift({ ...data, item_count: 0 })
    newPlaylist.value = { name: '', description: '' }
    showCreate.value = false
  } catch (e) { /* empty */ }
}

const formatTime = (s) => {
  if (!s) return '0:00'
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${String(sec).padStart(2, '0')}`
}

const aiSummarize = (id) => router.push({ path: '/ai-summarizer', query: { video: id } })
const goSubtitles = (id) => router.push({ path: '/subtitles', query: { video: id } })
const addNote = async (v) => {
  const content = prompt('Note content:')
  if (!content) return
  try {
    await api.post('/notes', { video_id: v.id, content, timestamp: 0 })
    alert('Note added!')
  } catch (e) { /* empty */ }
}

onMounted(async () => {
  await load()
  if (route.query.course) {
    // open first playlist or just show videos
  }
})
</script>
