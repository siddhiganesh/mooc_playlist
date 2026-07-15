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

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/learnhub-mooc.git
cd learnhub-mooc
```

Or download the ZIP and extract it manually.

### 2️⃣ Backend Setup (Flask + Python)

```bash
# Navigate to backend folder
cd backend

# Create a Python virtual environment (isolates dependencies)
python -m venv venv

# Activate the virtual environment
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# You should now see (venv) at the start of your terminal prompt

# Install all Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**What gets installed:**
- `Flask` — web framework
- `Flask-SQLAlchemy` — ORM
- `Flask-JWT-Extended` — JWT auth
- `Flask-Bcrypt` — password hashing
- `Flask-CORS` — cross-origin support
- `google-generativeai` — Gemini SDK
- `python-dotenv` — env file loader

### 3️⃣ Frontend Setup (Vue 3 + Vite)

Open a **new terminal** (keep the backend one running later):

```bash
# Navigate to frontend folder
cd frontend

# Install all Node dependencies
npm install

# If you get peer dependency warnings, this is usually safe:
npm install --legacy-peer-deps
```

**What gets installed:**
- `vue` + `vue-router` — UI framework
- `pinia` — state management
- `axios` — HTTP client
- `vite` + `@vitejs/plugin-vue` — build tools

### 4️⃣ Environment Configuration

**Backend** — edit `backend/.env`:

```env
SECRET_KEY=change-this-to-a-random-string
JWT_SECRET_KEY=change-this-too
DATABASE_URI=sqlite:///mooc_platform.db
GEMINI_API_KEY=your-gemini-api-key-from-aistudio
UPLOAD_FOLDER=uploads
```

> 💡 **Get a Gemini key (free):** [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
>
> 🔒 The app works without it — AI features will show a graceful fallback message.

**Frontend** — `frontend/.env` (already created):

```env
VITE_API_BASE=/api
```

### 5️⃣ First Run (Auto Database Setup)

The database is **automatically created and seeded** on first run — no manual migration needed. You'll see this in the terminal:

```
* Running on http://127.0.0.1:5000
* Database initialized
* Seed data loaded
```

### 6️⃣ Verify Installation

Test the backend:

```bash
curl http://localhost:5000/api/health
```

Expected response:

```json
{"status":"ok"}
```

### 7️⃣ Launch the App

**Terminal 1 — Backend:**
```bash
cd backend
venv\Scripts\activate    # Windows
python app.py
```
✅ Running on http://localhost:5000

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```
✅ Running on http://localhost:5173

### 8️⃣ Open in Browser

Visit 👉 **http://localhost:5173**

Login with:
- 📧 `student@mooc.com` / 🔑 `password123`
- 📧 `admin@mooc.com` / 🔑 `password123`

🎉 **You're all set!**

