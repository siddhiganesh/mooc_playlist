<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">❓ Quizzes</h1>
      <p class="page-subtitle">Test your knowledge</p>
    </div>

    <div v-if="!currentQuiz">
      <div v-if="loading" class="spinner"></div>
      <div v-else-if="quizzes.length" class="grid grid-2">
        <div v-for="q in quizzes" :key="q.id" class="card card-hover">
          <span class="badge badge-primary mb-2">{{ q.course_title }}</span>
          <h3 style="font-size: 18px; margin: 8px 0;">{{ q.title }}</h3>
          <p class="text-sm text-muted mb-3">{{ q.description }}</p>
          <div class="flex gap-3 text-sm mb-3">
            <span>❓ {{ q.question_count }} questions</span>
            <span>⏱ {{ Math.floor(q.time_limit / 60) }} min</span>
          </div>
          <button class="btn btn-primary w-full" @click="startQuiz(q)">Start Quiz</button>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="empty-state-icon">❓</div>
        <p>No quizzes available</p>
      </div>
    </div>

    <!-- Quiz in progress -->
    <div v-else-if="!result">
      <div class="flex justify-between items-center mb-3">
        <h2>{{ currentQuiz.title }}</h2>
        <div class="quiz-timer" v-if="!submitted">⏱ {{ formatTime(timeLeft) }}</div>
      </div>
      <div v-for="(q, idx) in currentQuiz.questions" :key="idx" class="question-card">
        <div class="question-text">{{ idx + 1 }}. {{ q.question }}</div>
        <div v-for="(opt, i) in q.options" :key="i" class="option" :class="{ selected: answers[idx] === i }" @click="answers[idx] = i">
          <span style="width:24px; height:24px; border-radius:50%; border:2px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">{{ String.fromCharCode(65 + i) }}</span>
          <span>{{ opt }}</span>
        </div>
      </div>
      <button class="btn btn-primary btn-lg w-full" @click="submitQuiz" :disabled="submitted">Submit Quiz</button>
    </div>

    <!-- Result -->
    <div v-else class="card text-center" style="max-width: 500px; margin: 40px auto;">
      <div class="score-circle" :style="scoreStyle">
        <div class="score-circle-inner">
          <div class="score-value">{{ result.score.toFixed(0) }}%</div>
          <div class="score-label">Score</div>
        </div>
      </div>
      <h2 class="mt-4 mb-2">{{ result.score >= 70 ? '🎉 Great job!' : '💪 Keep practicing!' }}</h2>
      <p class="text-muted mb-4">You got {{ result.correct }} out of {{ result.total }} questions correct.</p>
      <button class="btn btn-primary" @click="reset">Back to Quizzes</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '../services/api'

const quizzes = ref([])
const loading = ref(true)
const currentQuiz = ref(null)
const answers = ref([])
const timeLeft = ref(0)
const submitted = ref(false)
const result = ref(null)
let timer = null

const load = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/quizzes')
    quizzes.value = data.quizzes
  } catch (e) { /* empty */ }
  loading.value = false
}

const startQuiz = async (q) => {
  const { data } = await api.get(`/quizzes/${q.id}`)
  currentQuiz.value = data
  answers.value = new Array(data.questions.length).fill(-1)
  timeLeft.value = data.time_limit
  submitted.value = false
  result.value = null
  startTimer()
}

const startTimer = () => {
  if (timer) clearInterval(timer)
  timer = setInterval(() => {
    if (timeLeft.value > 0) timeLeft.value--
    else submitQuiz()
  }, 1000)
}

const submitQuiz = async () => {
  if (submitted.value) return
  submitted.value = true
  if (timer) clearInterval(timer)
  try {
    const { data } = await api.post(`/quizzes/${currentQuiz.value.id}/submit`, { answers: answers.value })
    result.value = data
  } catch (e) { /* empty */ }
}

const reset = () => {
  currentQuiz.value = null
  result.value = null
  answers.value = []
  if (timer) clearInterval(timer)
}

const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`

const scoreStyle = computed(() => {
  const score = result.value?.score || 0
  const deg = (score / 100) * 360
  const color = score >= 70 ? 'var(--success)' : score >= 50 ? 'var(--warning)' : 'var(--danger)'
  return { background: `conic-gradient(${color} 0deg, ${color} ${deg}deg, var(--border) ${deg}deg)` }
})

onMounted(load)
onUnmounted(() => { if (timer) clearInterval(timer) })
</script>
