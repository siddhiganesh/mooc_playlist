<template>
  <div class="view-container">
    <div class="dashboard-welcome">
      <h1>Welcome back, {{ user?.full_name || user?.username }}! 👋</h1>
      <p>Ready to continue your learning journey? You're doing great.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon purple">📚</div>
        <div>
          <div class="stat-value">{{ stats.enrolled }}</div>
          <div class="stat-label">Enrolled Courses</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">✅</div>
        <div>
          <div class="stat-value">{{ stats.completed }}</div>
          <div class="stat-label">Completed</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange">🏆</div>
        <div>
          <div class="stat-value">{{ stats.certificates }}</div>
          <div class="stat-label">Certificates</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pink">⭐</div>
        <div>
          <div class="stat-value">{{ user?.points || 0 }}</div>
          <div class="stat-label">Total Points</div>
        </div>
      </div>
    </div>

    <div class="dashboard-row">
      <div>
        <div class="page-header" style="margin-bottom: 16px;">
          <h3 class="page-title" style="font-size: 20px;">Continue Learning</h3>
        </div>
        <div class="grid grid-3" v-if="!loading && myCourses.length">
          <div v-for="c in myCourses.slice(0, 6)" :key="c.id" class="course-card" @click="goToCourse(c.id)">
            <div class="course-card-image" :style="{ backgroundImage: `url(${c.thumbnail})` }"></div>
            <div class="course-card-body">
              <div class="course-card-title">{{ c.title }}</div>
              <div class="course-card-instructor">{{ c.instructor }}</div>
              <div class="progress-bar"><div class="progress-fill" :style="{ width: c.progress + '%' }"></div></div>
              <div class="text-sm text-muted">{{ c.progress.toFixed(0) }}% complete</div>
            </div>
          </div>
        </div>
        <div v-else-if="loading" class="spinner"></div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">📭</div>
          <p>No enrolled courses yet</p>
          <router-link to="/my-courses" class="btn btn-primary mt-3">Browse Courses</router-link>
        </div>
      </div>

      <div>
        <div class="page-header" style="margin-bottom: 16px;">
          <h3 class="page-title" style="font-size: 20px;">Recent Activity</h3>
        </div>
        <div class="card">
          <div v-for="a in activities" :key="a.id" class="activity-item">
            <div class="activity-icon">{{ a.icon }}</div>
            <div class="activity-text">
              <div class="activity-title">{{ a.title }}</div>
              <div class="activity-time">{{ a.time }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { useAuthStore } from '../store'

const router = useRouter()
const auth = useAuthStore()
const user = computed(() => auth.user)
const myCourses = ref([])
const loading = ref(true)

const stats = ref({ enrolled: 0, completed: 0, certificates: 0 })
const activities = [
  { id: 1, icon: '📺', title: 'Watched 3 lessons today', time: '2 hours ago' },
  { id: 2, icon: '📝', title: 'Completed Python Quiz with 90%', time: 'Yesterday' },
  { id: 3, icon: '🏆', title: 'Earned ML Certificate', time: '3 days ago' },
  { id: 4, icon: '💬', title: 'Replied in Discussion Forum', time: '5 days ago' }
]

onMounted(async () => {
  try {
    const { data } = await api.get('/courses/my')
    myCourses.value = data.courses
    stats.value.enrolled = data.courses.length
    stats.value.completed = data.courses.filter(c => c.progress >= 100).length
  } catch (e) { /* empty */ }
  try {
    const { data: certs } = await api.get('/certificates')
    stats.value.certificates = certs.certificates.length
  } catch (e) { /* empty */ }
  loading.value = false
})

const goToCourse = (id) => router.push({ path: '/playlists', query: { course: id } })
</script>
