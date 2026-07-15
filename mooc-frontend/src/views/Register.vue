<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-logo">
        <div class="auth-logo-icon">✨</div>
        <h1 class="auth-title">Create Account</h1>
        <p class="auth-subtitle">Start your learning journey today</p>
      </div>

      <form class="auth-form" @submit.prevent="handleRegister">
        <div v-if="error" class="auth-error">{{ error }}</div>
        <div class="form-group">
          <label class="form-label">Full Name</label>
          <input v-model="form.full_name" class="form-input" placeholder="John Doe" required />
        </div>
        <div class="form-group">
          <label class="form-label">Username</label>
          <input v-model="form.username" class="form-input" placeholder="johndoe" required />
        </div>
        <div class="form-group">
          <label class="form-label">Email</label>
          <input v-model="form.email" type="email" class="form-input" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input v-model="form.password" type="password" class="form-input" placeholder="••••••••" required minlength="6" />
        </div>
        <div class="form-group">
          <label class="form-label">Bio (optional)</label>
          <textarea v-model="form.bio" class="form-textarea" placeholder="Tell us about yourself..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg w-full" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="auth-switch">
        Already have an account? <router-link to="/login">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ full_name: '', username: '', email: '', password: '', bio: '' })
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  loading.value = true
  try {
    const response = await auth.register(form)
    router.push('/dashboard')
  } catch (e) {
    if (e.response) {
      error.value = `Server error ${e.response.status}: ${JSON.stringify(e.response.data)}`
    } else if (e.request) {
      error.value = `Cannot reach server. Is Flask running on port 5000?`
    } else {
      error.value = `Error: ${e.message}`
    }
  } finally {
    loading.value = false
  }
}
</script>
