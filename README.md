# 🐳 Redis-Flask Visitor Counter Application

A containerized web application built with **Flask (Python)** and **Redis** that tracks and displays page visitor counts on a sleek, dark-themed UI. This repository demonstrates standard multi-container Docker orchestration using `docker-compose`.

---

## ✨ Features

- **Multi-container Architecture**: Sandboxed Flask web app separate from the Redis in-memory store.
- **Robust Redis Connection Handling**: Retries connection up to 5 times with exponential backoff if Redis is busy.
- **Modern Responsive UI**: Dark slate background with dynamic styling and micro-animations.
- **Production-grade alpine base images**: Lightweight, secure container footprint.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Flask
- **Database**: Redis (Alpine)
- **Containerization**: Docker, Docker Compose

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Docker** and **Docker Compose** installed on your system:
- [Docker Desktop for Windows/macOS](https://www.docker.com/products/docker-desktop/)

---

### Running with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/marutigore/docker-counter-app.git
   cd docker-counter-app
   ```

2. **Spin up the containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

4. **Stop the services**:
   ```bash
   docker-compose down
   ```

---

### Running Containers Individually

If you prefer to run the containers manually without docker-compose:

1. **Create a bridge network**:
   ```bash
   docker network create counter-network
   ```

2. **Run the Redis container**:
   ```bash
   docker run -d --name redis --network counter-network redis:alpine
   ```

3. **Build the Flask App image**:
   ```bash
   git clone https://github.com/marutigore/docker-counter-app.git
   cd docker-counter-app
   docker build -t flask-counter-app .
   ```

4. **Run the Flask App container**:
   ```bash
   docker run -d -p 5000:5000 --name web-app --network counter-network -e REDIS_HOST=redis flask-counter-app
   ```
