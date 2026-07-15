<template>
  <div class="view-container">
    <div class="page-header flex justify-between items-center">
      <div>
        <h1 class="page-title">Video Playlists</h1>
        <p class="page-subtitle">Watch lectures and build your own playlists</p>
      </div>
      <button class="btn btn-primary" @click="showCreate = true">+ New Playlist</button>
    </div>

    <!-- PLAYER VIEW -->
    <div v-if="activePlaylist || standaloneVideo">
      <button class="btn btn-secondary mb-3" @click="backToList">← Back</button>

      <div class="video-layout">
        <div>
          <div class="video-player-wrapper">
            <iframe v-if="currentVideo" :src="currentVideo.url" allowfullscreen></iframe>
            <div v-else class="empty-state" style="height:100%; display:flex; align-items:center; justify-content:center; color: white;">Select a video to play</div>
          </div>

          <div class="video-info" v-if="currentVideo">
            <h2 class="video-title">{{ currentVideo.title }}</h2>
            <p class="video-description">{{ currentVideo.description }}</p>
            <div class="flex gap-3 text-sm text-muted mt-2">
              <span>📺 {{ currentVideo.course_title || currentVideo.course?.title }}</span>
              <span>⏱ {{ formatTime(currentVideo.duration) }}</span>
            </div>
            <div class="flex gap-2 mt-3">
              <button class="btn btn-primary btn-sm" @click="aiSummarize(currentVideo.id)">🤖 AI Summarize</button>
              <button class="btn btn-secondary btn-sm" @click="goSubtitles(currentVideo.id)">💬 Subtitles</button>
              <button class="btn btn-secondary btn-sm" @click="addNote(currentVideo)">🗒️ Add Note</button>
              <button v-if="!inThisPlaylist" class="btn btn-secondary btn-sm" @click="showAddToPlaylist = true">➕ Add to Playlist</button>
            </div>
          </div>
        </div>

        <!-- Playlist sidebar (only when viewing a playlist) -->
        <div v-if="activePlaylist" class="playlist-sidebar">
          <div class="flex justify-between items-center mb-3">
            <h3 style="margin: 0;">{{ activePlaylist.name }}</h3>
            <button class="btn btn-sm btn-danger" @click="deletePlaylistConfirm">🗑</button>
          </div>
          <p class="text-sm text-muted mb-3" v-if="activePlaylist.description">{{ activePlaylist.description }}</p>
          <div v-if="playlistVideos.length === 0" class="text-sm text-muted">No videos in this playlist</div>
          <div v-for="(v, idx) in playlistVideos" :key="v.id" class="playlist-item" :class="{ active: currentVideo?.id === v.id }" @click="playVideo(v)">
            <div class="playlist-item-num">{{ idx + 1 }}</div>
            <div class="playlist-item-info">
              <div class="playlist-item-title">{{ v.title }}</div>
              <div class="playlist-item-duration">{{ v.course_title }} · {{ formatTime(v.duration) }}</div>
            </div>
            <button class="btn btn-sm btn-danger" style="padding: 4px 8px;" @click.stop="removeFromPlaylist(v)">✕</button>
          </div>
        </div>

        <!-- When playing a standalone video, show all videos instead -->
        <div v-else class="playlist-sidebar">
          <h3 class="mb-3">All Videos</h3>
          <div v-for="(v, idx) in videos" :key="v.id" class="playlist-item" :class="{ active: currentVideo?.id === v.id }" @click="playVideo(v)">
            <div class="playlist-item-num">{{ idx + 1 }}</div>
            <div class="playlist-item-info">
              <div class="playlist-item-title">{{ v.title }}</div>
              <div class="playlist-item-duration">{{ v.course_title }} · {{ formatTime(v.duration) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- LIST VIEW -->
    <div v-else class="grid" style="grid-template-columns: 320px 1fr; gap: 20px;">
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
          <div v-for="v in videos" :key="v.id" class="card card-hover" style="cursor: pointer;" @click="playStandalone(v)">
            <div class="flex gap-3">
              <div style="width: 80px; height: 60px; background: var(--bg-main); border-radius: 6px; display:flex; align-items:center; justify-content:center; font-size: 24px; flex-shrink: 0;">▶</div>
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

    <!-- Create playlist modal -->
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

    <!-- Add to playlist modal -->
    <div v-if="showAddToPlaylist" class="modal-overlay" @click.self="showAddToPlaylist = false">
      <div class="modal">
        <h3 class="mb-3">Add to Playlist</h3>
        <div v-if="playlists.length === 0" class="text-sm text-muted mb-3">You have no playlists. Create one first.</div>
        <div v-else>
          <div v-for="p in playlists" :key="p.id" class="card mb-2" style="cursor: pointer;" @click="addToPlaylist(p)">
            <div class="flex items-center gap-3">
              <div style="width: 36px; height: 36px; background: rgba(99,102,241,0.1); color: var(--primary); border-radius: 8px; display:flex; align-items:center; justify-content:center;">▶</div>
              <div>
                <div style="font-weight: 600; font-size: 14px;">{{ p.name }}</div>
                <div class="text-sm text-muted">{{ p.item_count }} videos</div>
              </div>
            </div>
          </div>
        </div>
        <button class="btn btn-secondary w-full mt-3" @click="showAddToPlaylist = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const playlists = ref([])
const videos = ref([])
const showCreate = ref(false)
const newPlaylist = ref({ name: '', description: '' })
const activePlaylist = ref(null)
const standaloneVideo = ref(false)
const playlistVideos = ref([])
const currentVideo = ref(null)
const showAddToPlaylist = ref(false)

const inThisPlaylist = computed(() => {
  if (!activePlaylist.value || !currentVideo.value) return false
  return playlistVideos.value.some(v => v.id === currentVideo.value.id)
})

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
  standaloneVideo.value = false
  try {
    const { data } = await api.get(`/playlists/${p.id}`)
    playlistVideos.value = data.videos
    if (data.videos.length) currentVideo.value = data.videos[0]
  } catch (e) { /* empty */ }
}

const playVideo = (v) => { currentVideo.value = v }

const playStandalone = (v) => {
  activePlaylist.value = null
  standaloneVideo.value = true
  currentVideo.value = v
}

const backToList = () => {
  activePlaylist.value = null
  standaloneVideo.value = false
  currentVideo.value = null
  playlistVideos.value = []
}

const createPlaylist = async () => {
  if (!newPlaylist.value.name) return
  try {
    const { data } = await api.post('/playlists', newPlaylist.value)
    playlists.value.unshift({ ...data, item_count: 0 })
    newPlaylist.value = { name: '', description: '' }
    showCreate.value = false
  } catch (e) { /* empty */ }
}

const addToPlaylist = async (p) => {
  if (!currentVideo.value) return
  try {
    await api.post(`/playlists/${p.id}/videos`, { video_id: currentVideo.value.id })
    showAddToPlaylist.value = false
    alert(`Added to "${p.name}"!`)
    await load()
  } catch (e) {
    alert('Could not add to playlist')
  }
}

const removeFromPlaylist = async (v) => {
  if (!activePlaylist.value) return
  if (!confirm('Remove this video from the playlist?')) return
  try {
    await api.delete(`/playlists/${activePlaylist.value.id}/videos/${v.id}`)
    playlistVideos.value = playlistVideos.value.filter(x => x.id !== v.id)
    if (currentVideo.value?.id === v.id) {
      currentVideo.value = playlistVideos.value[0] || null
    }
    await load()
  } catch (e) { /* empty */ }
}

const deletePlaylistConfirm = async () => {
  if (!activePlaylist.value) return
  if (!confirm(`Delete playlist "${activePlaylist.value.name}"?`)) return
  try {
    await api.delete(`/playlists/${activePlaylist.value.id}`)
    backToList()
    await load()
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

onMounted(load)
</script>
