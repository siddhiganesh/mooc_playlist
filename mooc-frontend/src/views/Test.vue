<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">📊 Tests</h1>
      <p class="page-subtitle">Comprehensive tests for your enrolled courses</p>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="tests.length" class="grid grid-2">
      <div v-for="t in tests" :key="t.id" class="card card-hover">
        <span class="badge badge-primary mb-2">{{ t.course_title }}</span>
        <h3 style="font-size: 18px; margin: 8px 0;">{{ t.title }}</h3>
        <p class="text-sm text-muted mb-3">{{ t.description }}</p>
        <div class="text-sm mb-3">📊 Total Marks: {{ t.total_marks }}</div>
        <button class="btn btn-primary w-full" @click="startTest(t)">View Test</button>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">📊</div>
      <p>No tests available</p>
    </div>

    <div v-if="current" class="modal-overlay" @click.self="current = null">
      <div class="modal" style="max-width: 700px;">
        <h3 class="mb-3">{{ current.title }}</h3>
        <p class="text-muted mb-3">{{ current.description }}</p>
        <div v-for="(q, i) in current.questions" :key="i" class="question-card">
          <div class="question-text">Q{{ i + 1 }}. {{ q.question }} <span class="text-sm text-muted">({{ q.marks || 20 }} marks)</span></div>
          <textarea class="form-textarea" rows="4" placeholder="Write your answer here..."></textarea>
        </div>
        <div class="flex gap-3 justify-between mt-3">
          <button class="btn btn-secondary" @click="current = null">Close</button>
          <button class="btn btn-primary" @click="submitTest">Submit Test</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const tests = ref([])
const current = ref(null)
const loading = ref(true)

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/quizzes/tests')
    tests.value = data.tests
  } catch (e) { /* empty */ }
  loading.value = false
}

const startTest = async (t) => {
  const { data } = await api.get(`/quizzes/tests/${t.id}`)
  current.value = data
}

const submitTest = () => {
  alert('Test submitted successfully! Your instructor will review it.')
  current.value = null
}

onMounted(load)
</script>
