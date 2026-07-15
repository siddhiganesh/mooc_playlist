<div align="center">

# 🎓 LearnHub — MOOC Platform

### A full-stack online learning platform inspired by Coursera, Udemy & NPTEL

[![Vue 3](https://img.shields.io/badge/Vue-3.x-42b883?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)]()

> **Build • Learn • Teach • Certify** — A complete end-to-end MOOC platform with AI-powered learning, video playlists, quizzes, assignments, discussions, leaderboards, and certificates.

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Configuration](#-configuration) • [Running](#-running-the-app) • [Demo Accounts](#-demo-accounts) • [Project Structure](#-project-structure) • [API Reference](#-api-reference) • [Screenshots](#-screenshots) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#-tech-stack)
- [📋 Prerequisites](#-prerequisites)
- [📥 Installation](#-installation)
- [⚙️ Configuration](#-configuration)
- [🚀 Running the App](#-running-the-app)
- [👥 Demo Accounts](#-demo-accounts)
- [📁 Project Structure](#-project-structure)
- [🔌 API Reference](#-api-reference)
- [🤖 AI Features (Gemini)](#-ai-features-gemini)
- [🎨 Design System](#-design-system)
- [📸 Screenshots](#-screenshots)
- [🧪 Testing](#-testing)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)

---

## ✨ Features

<div align="center">

### 🎯 **18 Powerful Modules** • **50+ API Endpoints** • **End-to-End Working**

</div>

<table>
<tr>
<td width="50%">

### 🔐 **Authentication & Profile**
- ✅ Email/password registration & login
- ✅ JWT-based secure authentication
- ✅ Profile management with bio & avatar
- ✅ Password change with bcrypt hashing
- ✅ Persistent sessions via localStorage
- ✅ Auto-logout on token expiry

### 📊 **Dashboard & Analytics**
- ✅ Personalized welcome screen
- ✅ Real-time learning statistics
- ✅ Continue learning section
- ✅ Recent activity timeline
- ✅ Quick stats (enrolled, completed, certs, points)

### 📚 **Course Management**
- ✅ Browse 6+ pre-seeded courses
- ✅ Search by title/keyword
- ✅ Filter by category & difficulty
- ✅ One-click enrollment
- ✅ Track course progress (%)
- ✅ Course detail view with video list

</td>
<td width="50%">

### ▶️ **Video Playlists**
- ✅ Create custom playlists
- ✅ Add/remove videos to playlists
- ✅ Embedded video player
- ✅ Auto-play next video
- ✅ Duration tracking

### 🤖 **AI Summarizer (Gemini)**
- ✅ Generate summaries from transcripts
- ✅ Extract key learning points
- ✅ Auto-generate quiz questions
- ✅ Topic explanation on demand
- ✅ AI chat assistant

### 💬 **Subtitles**
- ✅ Multi-language support
- ✅ Time-stamped display
- ✅ Search within subtitles
- ✅ Click-to-seek (coming soon)

</td>
</tr>
<tr>
<td width="50%">

### 📝 **Assignments & Tests**
- ✅ View enrolled course assignments
- ✅ Submit text/file assignments
- ✅ Auto-track submission status
- ✅ View grades & feedback
- ✅ Comprehensive tests view

### ❓ **Quizzes**
- ✅ Multiple-choice questions
- ✅ Built-in countdown timer
- ✅ Auto-grading with scoring
- ✅ Visual score circle
- ✅ Earn points per correct answer

### 🗒️ **Notes**
- ✅ Per-video timestamped notes
- ✅ Create, edit, delete notes
- ✅ Search & filter
- ✅ Quick note from video player

</td>
<td width="50%">

### 💭 **Discussion Forum**
- ✅ Create posts (course-scoped or general)
- ✅ Nested replies (threaded)
- ✅ Like posts
- ✅ Author info with avatars
- ✅ Course-tagged discussions

### 🏆 **Certificates**
- ✅ Auto-generated on 100% completion
- ✅ Unique verification code
- ✅ Public verification endpoint
- ✅ Beautiful certificate UI
- ✅ +500 bonus points per cert

### 🥇 **Leaderboard**
- ✅ Points-based global ranking
- ✅ Gold/Silver/Bronze top 3
- ✅ Certificates & courses count
- ✅ Highlight current user

</td>
</tr>
<tr>
<td colspan="2">

### ✉️ **Messages** • 👤 **Profile** • ⚙️ **Settings** • ❔ **Help Center**

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:---:|:---:|:---|
| **Frontend Framework** | ![Vue 3](https://img.shields.io/badge/Vue_3-42b883?style=flat-square&logo=vue.js&logoColor=white) | Reactive UI with Composition API |
| **State Management** | ![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=flat-square&logo=pinia&logoColor=black) | Lightweight Vue store |
| **Router** | ![Vue Router](https://img.shields.io/badge/Vue_Router-4-42b883?style=flat-square) | SPA navigation |
| **Build Tool** | ![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white) | Fast HMR dev server |
| **HTTP Client** | ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat-square) | API requests with interceptors |
| **Backend Framework** | ![Flask](https://img.shields.io/badge/Flask-3-000000?style=flat-square&logo=flask&logoColor=white) | Python REST API |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square) | Database abstraction |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Zero-config storage |
| **Auth** | ![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white) | Stateless tokens |
| **Password Hashing** | ![Bcrypt](https://img.shields.io/badge/Bcrypt-3D444F?style=flat-square) | Secure password storage |
| **AI** | ![Gemini](https://img.shields.io/badge/Gemini_Pro-4285F4?style=flat-square&logo=google&logoColor=white) | Summarization & quiz gen |
| **Styling** | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | Modular CSS in one folder |

</div>

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Download |
|:---|:---:|:---|
| **Python** | 3.9+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | Comes with Node.js |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |

**Verify your setup:**

```bash
python --version    # Python 3.9+
node --version      # v18+
npm --version       # 9+
