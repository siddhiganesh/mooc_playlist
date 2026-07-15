<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">📝 Assignments</h1>
      <p class="page-subtitle">View and submit your course assignments</p>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="assignments.length" class="grid grid-2">
      <div v-for="a in assignments" :key="a.id" class="card card-hover">
        <div class="flex justify-between items-center mb-3">
          <span class="badge badge-primary">{{ a.course_title }}</span>
          <span v-if="a.submitted" class="badge badge-success">Submitted</span>
          <span v-else class="badge badge-warning">Pending</span>
        </div>
        <h3 style="font-size: 18px; margin-bottom: 8px;">{{ a.title }}</h3>
        <p class="text-sm text-muted mb-3">{{ a.description }}</p>
        <div class="flex justify-between text-sm mb-3">
          <span>📅 Due: {{ formatDate(a.due_date) }}</span>
          <span>📊 Total: {{ a.total_marks }}</span>
        </div>
        <div v-if="a.grade !== null && a.grade !== undefined" class="mb-3">
          <span class="badge badge-info">Grade: {{ a.grade }}/{{ a.total_marks }}</span>
        </div>
        <button v-if="!a.submitted" class="btn btn-primary w-full" @click="openSubmit(a)">Submit</button>
        <button v-else class="btn btn-secondary w-full" @click="viewSubmission(a)">View Submission</button>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">📝</div>
      <p>No assignments yet</p>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3 class="mb-3">Submit: {{ current.title }}</h3>
        <div class="form-group">
          <label class="form-label">Your submission</label>
          <textarea v-model="submissionContent" class="form-textarea" rows="8" placeholder="Type your answer or paste a link..."></textarea>
        </div>
        <div class="flex gap-3 justify-between">
          <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
          <button class="btn btn-primary" @click="submitAssignment">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const assignments = ref([])
const loading = ref(true)
const showModal = ref(false)
const current = ref({})
const submissionContent = ref('')

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/assignments')
    assignments.value = data.assignments
  } catch (e) { /* empty */ }
  loading.value = false
}

const openSubmit = (a) => {
  current.value = a
  submissionContent.value = ''
  showModal.value = true
}

const submitAssignment = async () => {
  if (!submissionContent.value.trim()) { alert('Please enter content'); return }
  try {
    await api.post(`/assignments/${current.value.id}/submit`, { content: submissionContent.value })
    showModal.value = false
    await load()
  } catch (e) { /* empty */ }
}

const viewSubmission = async (a) => {
  try {
    const { data } = await api.get(`/assignments/${a.id}`)
    alert(`Your submission:\n\n${data.submission.content}\n\nGrade: ${data.submission.grade || 'Not graded yet'}`)
  } catch (e) { /* empty */ }
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString() : 'No due date'

onMounted(load)
</script>
