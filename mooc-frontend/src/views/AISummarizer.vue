<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">🤖 AI Summarizer</h1>
      <p class="page-subtitle">Powered by Google Gemini</p>
    </div>

    <div class="ai-container">
      <div class="ai-panel">
        <div class="ai-panel-header">
          <div class="ai-icon">📝</div>
          <h3>Input Content</h3>
        </div>
        <div class="form-group">
          <label class="form-label">Select a video (optional)</label>
          <select v-model="selectedVideo" class="form-select" @change="loadVideoSubtitles">
            <option value="">-- Custom text --</option>
            <option v-for="v in videos" :key="v.id" :value="v.id">{{ v.title }} ({{ v.course_title }})</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Or paste your text</label>
          <textarea v-model="customText" class="form-textarea" rows="10" placeholder="Paste lecture transcript, article, or any content..."></textarea>
        </div>
        <div class="flex gap-2">
          <button class="btn btn-primary" @click="doAction('summarize')" :disabled="loading">📄 Summarize</button>
          <button class="btn btn-secondary" @click="doAction('keypoints')" :disabled="loading">🔑 Key Points</button>
          <button class="btn btn-secondary" @click="doAction('quiz')" :disabled="loading">❓ Generate Quiz</button>
        </div>
      </div>

      <div class="ai-panel">
        <div class="ai-panel-header">
          <div class="ai-icon">✨</div>
          <h3>AI Output</h3>
        </div>
        <div v-if="loading" class="spinner"></div>
        <div v-else-if="output" class="ai-output">{{ output }}</div>
        <div v-else class="ai-output" style="color: var(--text-muted);">AI output will appear here...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const videos = ref([])
const selectedVideo = ref('')
const customText = ref('')
const output = ref('')
const loading = ref(false)

const loadVideos = async () => {
  try {
    const { data } = await api.get('/playlists/videos/all')
    videos.value = data.videos
    if (route.query.video) selectedVideo.value = String(route.query.video)
  } catch (e) { /* empty */ }
}

const loadVideoSubtitles = async () => {
  if (!selectedVideo.value) return
  try {
    const { data } = await api.get(`/subtitles/video/${selectedVideo.value}`)
    customText.value = data.subtitles.map(s => s.content).join(' ')
  } catch (e) { /* empty */ }
}

const doAction = async (action) => {
  if (!customText.value && !selectedVideo.value) {
    alert('Please provide content or select a video')
    return
  }
  loading.value = true
  output.value = ''
  try {
    const payload = { text: customText.value, video_id: selectedVideo.value || null }
    if (action === 'summarize') {
      const { data } = await api.post('/ai/summarize', payload)
      output.value = data.summary
    } else if (action === 'keypoints') {
      const { data } = await api.post('/ai/keypoints', payload)
      output.value = data.keypoints
    } else if (action === 'quiz') {
      const { data } = await api.post('/ai/generate-quiz', { ...payload, num_questions: 5 })
      output.value = data.raw
    }
  } catch (e) {
    output.value = 'Error: ' + (e.response?.data?.error || e.message)
  } finally {
    loading.value = false
  }
}

onMounted(loadVideos)
</script>
