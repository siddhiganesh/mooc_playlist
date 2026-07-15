<template>
  <div class="view-container">
    <div class="chat-layout">
      <div class="chat-sidebar">
        <div style="padding: 14px; border-bottom: 1px solid var(--border);">
          <h3>Messages</h3>
        </div>
        <div v-if="conversations.length === 0 && users.length === 0" class="empty-state" style="padding: 40px 20px;">
          <div class="empty-state-icon">✉️</div>
          <p>No conversations yet</p>
        </div>
        <div v-for="c in conversations" :key="c.other_user.id" class="chat-conv-item" :class="{ active: activeUserId === c.other_user.id }" @click="openConv(c)">
          <div class="chat-avatar">{{ c.other_user.username.charAt(0).toUpperCase() }}</div>
          <div class="chat-conv-info">
            <div class="chat-conv-name">{{ c.other_user.full_name || c.other_user.username }}</div>
            <div class="chat-conv-last">{{ c.last_message?.content || 'No messages yet' }}</div>
          </div>
          <span v-if="c.unread" class="chat-badge">{{ c.unread }}</span>
        </div>
      </div>

      <div class="chat-main">
        <div v-if="!activeUserId" class="empty-state" style="margin: auto;">
          <div class="empty-state-icon">💬</div>
          <p>Select a conversation or start a new one</p>
          <div class="mt-4" style="max-width: 400px;">
            <select v-model="newUserId" class="form-select mb-3">
              <option value="">-- New conversation with --</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.full_name || u.username }}</option>
            </select>
            <button class="btn btn-primary w-full" @click="startNew" :disabled="!newUserId">Start</button>
          </div>
        </div>
        <template v-else>
          <div class="chat-header">
            <div class="chat-avatar">{{ activeUser?.username?.charAt(0).toUpperCase() }}</div>
            <div>
              <div class="font-bold">{{ activeUser?.full_name || activeUser?.username }}</div>
            </div>
          </div>
          <div class="chat-messages" ref="messagesRef">
            <div v-for="m in messages" :key="m.id" class="msg-bubble" :class="m.sender_id === myId ? 'msg-mine' : 'msg-them'">
              {{ m.content }}
              <div class="msg-time">{{ new Date(m.created_at).toLocaleTimeString() }}</div>
            </div>
          </div>
          <div class="chat-input-area">
            <input v-model="newMessage" class="chat-input" placeholder="Type a message..." @keyup.enter="sendMessage" />
            <button class="btn btn-primary" @click="sendMessage">Send</button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../store'

const auth = useAuthStore()
const myId = computed(() => auth.user?.id)

const conversations = ref([])
const users = ref([])
const activeUserId = ref(null)
const activeUser = ref(null)
const messages = ref([])
const newMessage = ref('')
const newUserId = ref('')
const messagesRef = ref(null)

const load = async () => {
  try {
    const { data } = await api.get('/messages/conversations')
    conversations.value = data.conversations
  } catch (e) { /* empty */ }
  try {
    const { data } = await api.get('/messages/users')
    users.value = data.users
  } catch (e) { /* empty */ }
}

const openConv = async (c) => {
  activeUserId.value = c.other_user.id
  activeUser.value = c.other_user
  const { data } = await api.get(`/messages/with/${c.other_user.id}`)
  messages.value = data.messages
  await nextTick()
  if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight
}

const startNew = async () => {
  if (!newUserId.value) return
  const u = users.value.find(x => x.id === Number(newUserId.value))
  if (u) {
    activeUserId.value = u.id
    activeUser.value = u
    messages.value = []
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  try {
    const { data } = await api.post('/messages', { receiver_id: activeUserId.value, content: newMessage.value })
    messages.value.push(data)
    newMessage.value = ''
    await nextTick()
    if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    await load()
  } catch (e) { /* empty */ }
}

onMounted(load)
</script>
