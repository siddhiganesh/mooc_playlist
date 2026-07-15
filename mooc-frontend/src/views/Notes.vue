<template>
  <div class="view-container">
    <div class="page-header flex justify-between items-center">
      <div>
        <h1 class="page-title">🗒️ My Notes</h1>
        <p class="page-subtitle">Your personal study notes</p>
      </div>
      <button class="btn btn-primary" @click="showAdd = true">+ New Note</button>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="notes.length" class="notes-list">
      <div v-for="n in notes" :key="n.id" class="note-card">
        <div class="flex justify-between items-center mb-2">
          <div>
            <span class="note-timestamp">📺 {{ n.video_title }}</span>
            <span v-if="n.timestamp > 0" class="text-sm text-muted" style="margin-left: 12px;">⏱ {{ formatTime(n.timestamp) }}</span>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-sm btn-secondary" @click="editNote(n)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteNote(n.id)">Delete</button>
          </div>
        </div>
        <p style="line-height: 1.6;">{{ n.content }}</p>
        <div class="text-sm text-muted mt-2">Created: {{ new Date(n.created_at).toLocaleString() }}</div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">🗒️</div>
      <p>No notes yet. Start taking notes while watching videos!</p>
    </div>

    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd = false">
      <div class="modal">
        <h3 class="mb-3">{{ editing ? 'Edit Note' : 'New Note' }}</h3>
        <div class="form-group">
          <label class="form-label">Video</label>
          <select v-model="form.video_id" class="form-select">
            <option v-for="v in videos" :key="v.id" :value="v.id">{{ v.title }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Timestamp (seconds)</label>
          <input v-model.number="form.timestamp" type="number" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Note</label>
          <textarea v-model="form.content" class="form-textarea" rows="6"></textarea>
        </div>
        <div class="flex gap-3 justify-between">
          <button class="btn btn-secondary" @click="showAdd = false">Cancel</button>
          <button class="btn btn-primary" @click="saveNote">{{ editing ? 'Update' : 'Save' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const notes = ref([])
const videos = ref([])
const loading = ref(true)
const showAdd = ref(false)
const editing = ref(false)
const form = ref({ id: null, video_id: '', content: '', timestamp: 0 })

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/notes')
    notes.value = data.notes
  } catch (e) { /* empty */ }
  loading.value = false
  try {
    const { data } = await api.get('/playlists/videos/all')
    videos.value = data.videos
  } catch (e) { /* empty */ }
}

const editNote = (n) => {
  editing.value = true
  form.value = { id: n.id, video_id: n.video_id, content: n.content, timestamp: n.timestamp }
  showAdd.value = true
}

const saveNote = async () => {
  if (!form.value.content) { alert('Please write something'); return }
  try {
    if (editing.value) {
      await api.put(`/notes/${form.value.id}`, { content: form.value.content, timestamp: form.value.timestamp })
    } else {
      await api.post('/notes', form.value)
    }
    showAdd.value = false
    editing.value = false
    form.value = { id: null, video_id: '', content: '', timestamp: 0 }
    await load()
  } catch (e) { /* empty */ }
}

const deleteNote = async (id) => {
  if (!confirm('Delete this note?')) return
  try {
    await api.delete(`/notes/${id}`)
    await load()
  } catch (e) { /* empty */ }
}

const formatTime = (s) => {
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${String(sec).padStart(2, '0')}`
}

onMounted(load)
</script>
