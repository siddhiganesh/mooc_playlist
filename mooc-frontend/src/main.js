import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'
import './assets/styles/sidebar.css'
import './assets/styles/auth.css'
import './assets/styles/dashboard.css'
import './assets/styles/views.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
