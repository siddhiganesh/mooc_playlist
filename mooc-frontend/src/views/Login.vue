<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-logo">
        <div class="auth-logo-icon">🎓</div>
        <h1 class="auth-title">Welcome Back</h1>
        <p class="auth-subtitle">Sign in to continue learning</p>
      </div>

      <form class="auth-form" @submit.prevent="handleLogin">
        <div v-if="error" class="auth-error">{{ error }}</div>
        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input v-model="email" type="email" class="form-input" placeholder="you@example.com" required />
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-input" placeholder="••••••••" required />
        </div>
        <button type="submit" class="btn btn-primary btn-lg w-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="auth-switch">
        Don't have an account? <router-link to="/register">Sign up</router-link>
      </p>

      <div class="auth-demo">
        <strong>Demo accounts:</strong><br />
        Student: student@mooc.com / password123<br />
        Admin: admin@mooc.com / password123
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'

const router = useRouter()
const auth = useAuthStore()
const email = ref('siddhi@gmail.com')
const password = ref('siddhi')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    await auth.login({ email: email.value, password: password.value })
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
