<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">🏆 Certificates</h1>
      <p class="page-subtitle">Your earned certificates and achievements</p>
    </div>

    <div v-if="loading" class="spinner"></div>
    <div v-else-if="certs.length" class="grid grid-2">
      <div v-for="c in certs" :key="c.id" class="certificate-card">
        <div style="font-size: 14px; letter-spacing: 2px; color: #92400e;">CERTIFICATE OF COMPLETION</div>
        <div class="cert-title">LearnHub</div>
        <div style="color: var(--text-secondary);">This is to certify that</div>
        <div class="cert-name">{{ auth.user?.full_name || auth.user?.username }}</div>
        <div style="color: var(--text-secondary);">has successfully completed</div>
        <div class="cert-course">{{ c.course_title }}</div>
        <div class="flex gap-3 justify-between items-center" style="margin-top: 20px;">
          <div class="text-sm">
            <div class="font-bold">Instructor</div>
            <div>{{ c.instructor }}</div>
          </div>
          <div class="text-sm">
            <div class="font-bold">Issued</div>
            <div>{{ new Date(c.issued_at).toLocaleDateString() }}</div>
          </div>
        </div>
        <div class="cert-code mt-3">Code: {{ c.certificate_code }}</div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">🏆</div>
      <p>Complete courses to earn certificates!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../store'

const auth = useAuthStore()
const certs = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/certificates')
    certs.value = data.certificates
  } catch (e) { /* empty */ }
  loading.value = false
})
</script>
