<template>
  <div class="view-container">
    <div v-if="loading" class="spinner"></div>
    <div v-else>
      <div class="profile-header">
        <div class="profile-avatar">{{ (profile.full_name || profile.username || 'U').charAt(0).toUpperCase() }}</div>
        <div>
          <div class="profile-name">{{ profile.full_name || profile.username }}</div>
          <div class="profile-email">@{{ profile.username }} · {{ profile.email }}</div>
          <div class="profile-bio">{{ profile.bio || 'No bio yet' }}</div>
        </div>
      </div>

      <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="card">
          <h3 class="mb-3">Edit Profile</h3>
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input v-model="profile.full_name" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Bio</label>
            <textarea v-model="profile.bio" class="form-textarea" rows="4"></textarea>
          </div>
          <button class="btn btn-primary" @click="save">Save Changes</button>
        </div>

        <div>
          <div class="card mb-3">
            <h3 class="mb-3">Stats</h3>
            <div class="flex gap-4" style="flex-wrap: wrap;">
              <div>
                <div class="text-xl font-bold" style="color: var(--primary);">{{ profile.stats?.courses_enrolled || 0 }}</div>
                <div class="text-sm text-muted">Enrolled</div>
              </div>
              <div>
                <div class="text-xl font-bold" style="color: var(--success);">{{ profile.stats?.certificates || 0 }}</div>
                <div class="text-sm text-muted">Certificates</div>
              </div>
              <div>
                <div class="text-xl font-bold" style="color: var(--warning);">{{ profile.stats?.quizzes_attempted || 0 }}</div>
                <div class="text-sm text-muted">Quizzes</div>
              </div>
              <div>
                <div class="text-xl font-bold" style="color: var(--secondary);">{{ profile.points }}</div>
                <div class="text-sm text-muted">Points</div>
              </div>
            </div>
          </div>

          <div class="card">
            <h3 class="mb-3">Member Since</h3>
            <p>{{ new Date(profile.created_at).toLocaleDateString() }}</p>
            <p class="text-sm text-muted mt-2">Role: {{ profile.role }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const loading = ref(true)
const profile = ref({})

const load = async () => {
  try {
    const { data } = await api.get('/profile')
    profile.value = data
  } catch (e) { /* empty */ }
  loading.value = false
}

const save = async () => {
  try {
    await api.put('/profile', { full_name: profile.value.full_name, bio: profile.value.bio })
    alert('Profile updated!')
  } catch (e) { /* empty */ }
}

onMounted(load)
</script>
