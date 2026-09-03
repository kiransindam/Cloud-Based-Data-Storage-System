# ☁️ CloudVault — Cloud Document Storage System

A production-ready, multi-tenant document storage platform built with **FastAPI**, **AWS S3**, and **PostgreSQL**. Solves the real-world problem of secure file storage with expiring shareable links for small teams.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![AWS](https://img.shields.io/badge/AWS-S3-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 🎯 Problem Statement
Small businesses need a secure, affordable way to:
- Store documents in the cloud
- Organize files with tags & search
- Share files via expiring links (no public exposure)
- Enforce per-user isolation & access control

CloudVault delivers this in a self-hostable, scalable package.

## 🏗️ Architecture
```
┌──────────────┐       ┌──────────────┐       ┌──────────┐
│   Client     │──────▶│  FastAPI     │──────▶│  AWS S3  │
│ (Browser/API)│       │  (REST API)  │       │ (Files)  │
└──────────────┘       └──────┬───────┘       └──────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  PostgreSQL  │
                       │  (Metadata)  │
                       └──────────────┘
```

## ✨ Features
- ✅ User registration & JWT authentication
- ✅ File upload with type/size validation
- ✅ S3-backed storage with unique keys
- ✅ Pre-signed download URLs (1-hour expiry)
- ✅ Search by filename or tags
- ✅ Per-user document isolation
- ✅ Dockerized for easy deployment
- ✅ Auto-generated OpenAPI docs (`/docs`)

## 🚀 Quick Start

### 1. Clone & Configure
```bash
git clone https://github.com/YOUR_USERNAME/cloud-vault.git
cd cloud-vault
cp .env.example .env
# Edit .env with your AWS credentials
```

### 2. Run with Docker
```bash
docker-compose up --build
```
API available at: http://localhost:8000/docs

### 3. Local Development (without Docker)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Get JWT token |
| POST | `/api/v1/documents/` | Upload file |
| GET | `/api/v1/documents/` | List user's files |
| GET | `/api/v1/documents/{id}` | Get file + download URL |
| DELETE | `/api/v1/documents/{id}` | Delete file |

## 🧪 Testing
```bash
pytest -v
```

## 🌍 AWS Setup
1. Create S3 bucket (block all public access)
2. Create IAM user with `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`
3. Add credentials to `.env`

## 🔒 Security
- Passwords hashed with bcrypt
- JWT tokens with expiry
- Per-user data isolation enforced at DB level
- Pre-signed URLs (never expose S3 directly)

## 📈 Future Enhancements
- [ ] File versioning
- [ ] Shared folders between users
- [ ] Async file processing (virus scan, OCR)
- [ ] Redis caching layer
- [ ] Kubernetes deployment

## 📄 License
MIT © 2026
