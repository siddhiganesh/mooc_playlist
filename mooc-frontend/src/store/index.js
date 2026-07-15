import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),
  actions: {
    async login(credentials) {
      const { data } = await api.post('/auth/login', credentials)
      this.setSession(data.token, data.user)
      return data
    },
    async register(payload) {
      const { data } = await api.post('/auth/register', payload)
      this.setSession(data.token, data.user)
      return data
    },
    async fetchMe() {
      if (!this.token) return null
      try {
        const { data } = await api.get('/auth/me')
        this.user = data
        localStorage.setItem('user', JSON.stringify(data))
        return data
      } catch (e) {
        this.logout()
        return null
      }
    },
    setSession(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
