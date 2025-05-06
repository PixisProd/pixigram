# 🪐 Pixigram
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-⚡_Fast_and_Modern-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-🧪_ORM_Tool-CB3032?logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-⚗_Migrations-4B8BBE)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-🐘_Relational_DB-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-🔴_In--Memory_DB-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-🐳_Containers-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-🌐_Proxy-009639?logo=nginx&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-🔐_Auth_Tokens-000000?logo=jsonwebtokens&logoColor=white)

## 📖 Description
Pixigram — **very fast room-based chat** built with **WebSockets**, **FastAPI**, and **Redis**. It features a **user and role management system**, **JWT token-based authentication**, and comes with both a frontend and a backend. All services are easily started with Docker **Compose**, and **Nginx** is used for reverse proxying and serving static files.

### 🔥 Highlights
⚡ Fully asynchronous architecture for high performance  
🔐 JWT-based authentication and security layer  
🧩 Role-based access control (RBAC) — user and admin roles   
💬 Chat system powered by WebSockets and Redis  
🚀 Redis for lightning-fast chat performance  
🧪 SQLAlchemy + Alembic for database management  
🐘 PostgreSQL as the primary relational database  
📦 One-command build and startup via Docker Compose  
🌐 Reverse proxy & static file serving handled by Nginx  

---

## 🔧 Features
- Real-time communication using WebSockets
- Room-based chat system powered by Redis
  - Create & join rooms
  - Automatic room moderation system
  - Very fast data operations
- Fully asynchronous
- Authentication and security system
- RBAC system (user, admin)
- Docker Compose to easily bring up the entire application with one command
- PostgreSQL database with SQLAlchemy ORM and Alembic migrations
- Nginx for reverse proxy and static file serving.

---

## 🛠 Technologies
- **Languages**: Python, JavaScript
- **Authorization**: JWT tokens
- **Backend**: FastAPI, WebSockets, Redis
- **Connection manager**: Redis
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Reverse Proxy**: Nginx
- **Frontend**: Vanilla JS+HTML+CSS 
- **Containerization**: Docker, Docker Compose 

---

# ⚙ How to setup and run

## 📦 Preparation
1. **Clone the repository to your local machine:**
```
git clone https://github.com/PixisProd/pixigram.git
cd pixigram
```
2. **Download and install Docker:**  
   - Visit [the official Docker page](https://www.docker.com/).
   - Make sure the Docker daemon is running
     
---

## 🚀 Launch
1. First, create a `.env` file by copying `.env.example`.  
*You can also customize additional parameters such as `JWT_SECRET_KEY`, etc.*

2. **Now run the project:**  
```
docker-compose up --build
```
The project will be available at [http://localhost:8080](http://localhost:8080)

---

## 📝 License

This project is licensed under the [MIT License](./LICENSE).

---

# 🌌 Conclusion
Thank you for checking out **Pixigram**!  
If you find the project helpful or inspiring, feel free to ⭐️ star it and share your thoughts. 

_✨ Crafted to build knowledge._
