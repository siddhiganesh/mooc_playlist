<template>
  <div class="view-container">
    <div class="page-header">
      <h1 class="page-title">❔ Help & Support</h1>
      <p class="page-subtitle">Find answers to common questions</p>
    </div>

    <div class="tabs">
      <div v-for="t in tabs" :key="t" class="tab" :class="{ active: activeTab === t }" @click="activeTab = t">{{ t }}</div>
    </div>

    <div v-if="activeTab === 'FAQ'">
      <div v-for="(item, i) in faqs" :key="i" class="help-section">
        <div class="help-q">❓ {{ item.q }}</div>
        <div class="help-a">{{ item.a }}</div>
      </div>
    </div>

    <div v-else-if="activeTab === 'Contact'">
      <div class="help-section">
        <h3 class="mb-3">Get in touch</h3>
        <div class="grid grid-2">
          <div>
            <div class="text-sm text-muted">📧 Email</div>
            <div class="font-bold">support@learnhub.com</div>
          </div>
          <div>
            <div class="text-sm text-muted">📞 Phone</div>
            <div class="font-bold">+1 (555) 123-4567</div>
          </div>
          <div>
            <div class="text-sm text-muted">💬 Live Chat</div>
            <div class="font-bold">Available 24/7</div>
          </div>
          <div>
            <div class="text-sm text-muted">🌐 Community</div>
            <div class="font-bold">forum.learnhub.com</div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="activeTab === 'Guides'">
      <div v-for="g in guides" :key="g.title" class="help-section">
        <h3>{{ g.title }}</h3>
        <p class="help-a mt-2">{{ g.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tabs = ['FAQ', 'Contact', 'Guides']
const activeTab = ref('FAQ')

const faqs = [
  { q: 'How do I enroll in a course?', a: 'Browse the course catalog from "My Courses", click on a course, and hit the "Enroll" button. You will get instant access to all videos, quizzes, and assignments.' },
  { q: 'Can I download videos for offline viewing?', a: 'Currently, videos stream online only. We are working on offline access for premium subscribers in the next update.' },
  { q: 'How do I get a certificate?', a: 'Complete all videos and quizzes in a course, then visit the Certificates page to generate your certificate. It includes a unique verification code.' },
  { q: 'What is the AI Summarizer?', a: 'Our AI Summarizer uses Google Gemini to generate summaries, key points, and quiz questions from any video transcript or text you provide.' },
  { q: 'How are points calculated?', a: 'You earn points for: watching videos (+5), completing quizzes (+score), earning certificates (+500), and active discussion participation.' },
  { q: 'Can I message other students?', a: 'Yes! Use the Messages section in the sidebar to chat with other learners on the platform.' }
]

const guides = [
  { title: '🚀 Getting Started', content: 'Create your account, complete your profile, and browse our course catalog. We recommend starting with a Beginner course in your area of interest.' },
  { title: '📚 Using Playlists', content: 'Create custom playlists to organize videos by topic. Click the "+ New Playlist" button on the Playlists page to get started.' },
  { title: '🤖 Maximizing AI Tools', content: 'For best results with the AI Summarizer, paste transcripts or articles of at least 200 words. The tool works best with structured educational content.' },
  { title: '🏆 Earning Certificates', content: 'Complete every video in a course, pass quizzes with 70%+, and submit all assignments. Your certificate will be available immediately after completion.' }
]
</script>
