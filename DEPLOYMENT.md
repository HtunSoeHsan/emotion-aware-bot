# Hosting and Deployment Guide 🚀

This guide explains how to deploy the **Emotion-Aware Bot** on your VPS using **Docker**, **Docker Compose**, and **Dokploy**.

---

## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Method 1: Docker Compose Deployment (CLI)](#-method-1-docker-compose-deployment-cli)
3. [Method 2: Dokploy Deployment (Recommended)](#-method-2-dokploy-deployment-recommended)
   - [Option A: Deploy as a Compose Stack (Easiest)](#option-a-deploy-as-a-compose-stack-easiest)
   - [Option B: Deploy as Individual Applications](#option-b-deploy-as-individual-applications)
4. [⚠️ Production Tips (DeepFace Weights & Performance)](#-production-tips-deepface-weights--performance)

---

## 🛠️ Prerequisites

Before starting, ensure your VPS has:
1. **Docker and Docker Compose** installed.
2. **Git** installed.
3. Ports `8000` (Backend) and `4001` (Frontend) open in your VPS firewall (if not using a reverse proxy or Dokploy).

If you don't have Docker installed, run:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

---

## 🐳 Method 1: Docker Compose Deployment (CLI)

This is the fastest command-line method to get both services running together.

### Step 1: Clone the Repository on your VPS
```bash
git clone https://github.com/HtunSoeHsan/emotion-aware-bot.git
cd emotion-aware-bot
```

### Step 2: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
# Groq API Key (Optional but recommended for AI features)
GROQ_API_KEY=your_groq_api_key_here

# External APIs (Optional)
YOUTUBE_API_KEY=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
NEWS_API_KEY=
```

### Step 3: Run the Stack
Start the containers in detached mode:
```bash
docker compose up -d --build
```

### Step 4: Verify Deployment
- **Frontend URL:** `http://<your-vps-ip>:4001`
- **Backend API Docs:** `http://<your-vps-ip>:8000/docs`
- Check logs if needed: `docker compose logs -f`

---

## 🌐 Method 2: Dokploy Deployment (Recommended)

Since you are using **Dokploy**, you can manage builds, domains, environment variables, and automatic SSL directly from the Dokploy GUI.

### Option A: Deploy as a Compose Stack (Easiest)
Deploying via a single Compose stack keeps both services grouped in a private network.

1. Open your **Dokploy** panel.
2. Navigate to your **Project** and click **Create Service** -> **Compose**.
3. Name your stack (e.g., `emotion-aware-bot`).
4. In the **Source** section, select **Git Repository**:
   - **Repository URL:** `https://github.com/HtunSoeHsan/emotion-aware-bot.git` (or your private fork URL).
   - **Branch:** `main`
   - **Compose Path:** `docker-compose.yml`
5. Go to the **Environment** tab of the Compose service and add your environment keys (e.g., `GROQ_API_KEY`).
6. Click **Deploy**.
7. **Expose to Public:**
   - To access the web interface, click on the **frontend** service in your Compose stack settings.
   - Go to **Domains** -> **Add Domain** (e.g., `bot.yourdomain.com`).
   - Dokploy will automatically provision a Let's Encrypt SSL certificate!

---

### Option B: Deploy as Individual Applications
If you want fine-grained control or scaling for each service:

#### 1. Deploy the Backend Application
1. In Dokploy, click **Create Service** -> **Application**.
2. Name it `emotion-bot-backend`.
3. In **Source**, link your Git repository.
4. In **Build Settings**:
   - **Build Type:** `Dockerfile`
   - **Dockerfile Path:** `backend/Dockerfile`
5. In **Environment Variables**, add:
   - `GROQ_API_KEY` = `your-api-key`
   - `HOST` = `0.0.0.0`
   - `PORT` = `8000`
6. In **Ports**, map Port `8000` to `8000`.
7. Click **Deploy**. Note the internal URL (e.g., `http://emotion-bot-backend:8000`).

#### 2. Deploy the Frontend Application
1. Create another **Application** in Dokploy named `emotion-bot-frontend`.
2. Link the same Git repository.
3. In **Build Settings**:
   - **Build Type:** `Dockerfile`
   - **Dockerfile Path:** `frontend/Dockerfile`
4. In **Environment Variables**, add:
   - `BACKEND_URL` = `http://emotion-bot-backend:8000` (Use the internal container name/URL of the backend so traffic stays secure and fast).
5. Add a **Domain** (e.g. `bot.yourdomain.com`) to route traffic to Port `4001`.
6. Click **Deploy**.

---

## ⚠️ Production Tips (DeepFace Weights & Performance)

### 📸 Persisting DeepFace Model Weights
The facial emotion recognition feature (`deepface`) downloads large pre-trained model weights (like VGG-Face) on its first run.
- We have created a volume named `deepface-weights` mapped to `/root/.deepface` in `docker-compose.yml`.
- This ensures that if the container restarts or redeploys, the model weights **are not deleted**, preventing long initialization delays during face analysis requests.

### 💾 RAM Requirements
- Because TensorFlow and DeepFace run in python memory, we recommend a VPS with at least **2 GB RAM**.
