<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">💭 Discussion Forum</h1>
      <p class="page-subtitle">Ask questions and help peers</p>
    </div>

    <div class="card mb-4">
      <h3 class="mb-3">Create a new post</h3>
      <div class="form-group">
        <select v-model="newPost.course_id" class="form-select">
          <option value="">-- Select course (optional) --</option>
          <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option>
        </select>
      </div>
      <textarea v-model="newPost.content" class="form-textarea" rows="3" placeholder="Share your thoughts or ask a question..."></textarea>
      <button class="btn btn-primary mt-3" @click="createPost">Post</button>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="posts.length">
      <div v-for="p in posts" :key="p.id" class="discussion-post">
        <div class="post-header">
          <div class="post-avatar">{{ p.username.charAt(0).toUpperCase() }}</div>
          <div class="post-meta">
            <div class="post-author">{{ p.full_name || p.username }}</div>
            <div class="post-time">{{ formatDate(p.created_at) }} · {{ p.course_title || 'General' }}</div>
          </div>
        </div>
        <div class="post-content">{{ p.content }}</div>
        <div class="post-actions">
          <span class="post-action" @click="likePost(p)">👍 {{ p.likes }}</span>
          <span class="post-action" @click="openPost(p)">💬 {{ p.reply_count }} replies</span>
        </div>

        <div v-if="openPostId === p.id" class="replies-section">
          <div v-for="r in replies" :key="r.id" class="reply">
            <div class="flex items-center gap-2 mb-2">
              <div class="post-avatar" style="width: 28px; height: 28px; font-size: 12px;">{{ r.username.charAt(0).toUpperCase() }}</div>
              <strong class="text-sm">{{ r.full_name || r.username }}</strong>
              <span class="text-sm text-muted">{{ formatDate(r.created_at) }}</span>
            </div>
            <div class="text-sm">{{ r.content }}</div>
          </div>
          <div class="flex gap-2 mt-3">
            <input v-model="replyContent" class="form-input" placeholder="Write a reply..." @keyup.enter="postReply(p)" />
            <button class="btn btn-primary" @click="postReply(p)">Reply</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">💭</div>
      <p>No discussions yet. Be the first to post!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const posts = ref([])
const courses = ref([])
const loading = ref(true)
const newPost = ref({ course_id: '', content: '' })
const openPostId = ref(null)
const replies = ref([])
const replyContent = ref('')

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/discussion')
    posts.value = data.posts
  } catch (e) { /* empty */ }
  loading.value = false
  try {
    const { data } = await api.get('/courses/my')
    courses.value = data.courses
  } catch (e) { /* empty */ }
}

const createPost = async () => {
  if (!newPost.value.content) return
  try {
    await api.post('/discussion', { content: newPost.value.content, course_id: newPost.value.course_id || null })
    newPost.value = { course_id: '', content: '' }
    await load()
  } catch (e) { /* empty */ }
}

const openPost = async (p) => {
  openPostId.value = openPostId.value === p.id ? null : p.id
  if (openPostId.value) {
    const { data } = await api.get(`/discussion/${p.id}`)
    replies.value = data.replies
  }
}

const postReply = async (p) => {
  if (!replyContent.value) return
  try {
    await api.post('/discussion', { content: replyContent.value, parent_id: p.id })
    replyContent.value = ''
    const { data } = await api.get(`/discussion/${p.id}`)
    replies.value = data.replies
    await load()
  } catch (e) { /* empty */ }
}

const likePost = async (p) => {
  try {
    await api.post(`/discussion/${p.id}/like`)
    p.likes++
  } catch (e) { /* empty */ }
}

const formatDate = (d) => new Date(d).toLocaleString()

onMounted(load)
</script>
