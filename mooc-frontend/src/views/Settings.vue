<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">⚙️ Settings</h1>
      <p class="page-subtitle">Manage your account preferences</p>
    </div>

    <div class="card mb-3">
      <h3 class="mb-3">Change Password</h3>
      <div class="form-group">
        <label class="form-label">Current Password</label>
        <input v-model="pw.old" type="password" class="form-input" />
      </div>
      <div class="form-group">
        <label class="form-label">New Password</label>
        <input v-model="pw.new" type="password" class="form-input" />
      </div>
      <button class="btn btn-primary" @click="changePassword">Update Password</button>
    </div>

    <div class="card mb-3">
      <h3 class="mb-3">Notifications</h3>
      <div class="setting-row">
        <div class="setting-info">
          <h4>Email Notifications</h4>
          <p>Receive emails about new courses and updates</p>
        </div>
        <label class="toggle">
          <input type="checkbox" v-model="settings.email" />
          <span class="toggle-slider"></span>
        </label>
      </div>
      <div class="setting-row">
        <div class="setting-info">
          <h4>Discussion Replies</h4>
          <p>Notify me when someone replies to my post</p>
        </div>
        <label class="toggle">
          <input type="checkbox" v-model="settings.replies" />
          <span class="toggle-slider"></span>
        </label>
      </div>
      <div class="setting-row">
        <div class="setting-info">
          <h4>Assignment Reminders</h4>
          <p>Remind me before assignments are due</p>
        </div>
        <label class="toggle">
          <input type="checkbox" v-model="settings.assignments" />
          <span class="toggle-slider"></span>
        </label>
      </div>
    </div>

    <div class="card">
      <h3 class="mb-3">Preferences</h3>
      <div class="setting-row">
        <div class="setting-info">
          <h4>Playback Speed</h4>
          <p>Default speed for video playback</p>
        </div>
        <select v-model="settings.speed" class="form-select" style="width: 120px;">
          <option>0.75</option><option>1</option><option>1.25</option><option>1.5</option><option>2</option>
        </select>
      </div>
      <div class="setting-row">
        <div class="setting-info">
          <h4>Subtitle Language</h4>
          <p>Default subtitle language</p>
        </div>
        <select v-model="settings.lang" class="form-select" style="width: 150px;">
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="hi">Hindi</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const pw = ref({ old: '', new: '' })
const settings = ref({
  email: true,
  replies: true,
  assignments: true,
  speed: '1',
  lang: 'en'
})

const changePassword = async () => {
  if (!pw.value.old || !pw.value.new) { alert('Please fill all fields'); return }
  try {
    const api = (await import('../services/api')).default
    await api.put('/profile/password', { old_password: pw.value.old, new_password: pw.value.new })
    alert('Password updated!')
    pw.value = { old: '', new: '' }
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update password')
  }
}
</script>
