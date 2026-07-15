<template>
  <div class="view-container">
    <div class="page-header flex justify-between items-center">
      <div>
        <h1 class="page-title">My Courses</h1>
        <p class="page-subtitle">Browse and enroll in new courses</p>
      </div>
    </div>

    <div class="flex gap-3 mb-4" style="flex-wrap: wrap">
      <input
        v-model="search"
        class="form-input"
        placeholder="Search courses..."
        style="max-width: 300px"
        @input="loadCourses"
      />
      <select v-model="category" class="form-select" style="max-width: 200px" @change="loadCourses">
        <option>All</option>
        <option>Programming</option>
        <option>Data Science</option>
        <option>Web Development</option>
      </select>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="courses.length" class="grid grid-3">
      <div v-for="c in courses" :key="c.id" class="course-card card-hover">
        <div class="course-card-image" :style="{ backgroundImage: `url(${c.thumbnail})` }">
          <span v-if="c.enrolled" class="course-card-badge badge badge-success">Enrolled</span>
        </div>
        <div class="course-card-body">
          <div class="flex gap-2 mb-2">
            <span class="badge badge-primary">{{ c.category }}</span>
            <span class="badge badge-info">{{ c.difficulty }}</span>
          </div>
          <div class="course-card-title">{{ c.title }}</div>
          <div class="course-card-instructor">{{ c.instructor }} · ⭐ {{ c.rating }}</div>
          <p
            class="text-sm text-muted mb-3"
            style="
              display: -webkit-box;
              -webkit-line-clamp: 2;
              line-clamp: 2;
              -webkit-box-orient: vertical;
              overflow: hidden;
            "
          >
            {{ c.description }}
          </p>
          <div class="flex justify-between items-center">
            <span class="text-sm text-muted"
              >{{ c.video_count }} videos · {{ c.duration_hours }}h</span
            >
            <button v-if="!c.enrolled" class="btn btn-primary btn-sm" @click="enroll(c)">
              Enroll
            </button>
            <button v-else class="btn btn-success btn-sm" @click="openCourse(c)">Continue</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">🔍</div>
      <p>No courses found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const courses = ref([])
const loading = ref(true)
const search = ref(route.query.search || '')
const category = ref('All')

const loadCourses = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/courses', {
      params: { search: search.value, category: category.value },
    })
    courses.value = data.courses
  } catch (e) {
    /* empty */
  }
  loading.value = false
}

const enroll = async (c) => {
  try {
    await api.post(`/courses/${c.id}/enroll`)
    c.enrolled = true
  } catch (e) {
    /* empty */
  }
}

const openCourse = (c) => {
  router.push({ path: '/playlists', query: { course: c.id } })
}

onMounted(loadCourses)
watch(
  () => route.query.search,
  (v) => {
    search.value = v || ''
    loadCourses()
  },
)
</script>
