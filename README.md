# 🏨 Smart Hotel Reservation System – AI Powered

## 📌 Overview

The Smart Hotel Reservation System is an end-to-end AI-driven booking platform that combines:

Hotel Reservation Management

Machine Learning-based Fraud Detection (LightGBM + Random Forest)

User Identity Verification with OCR & Document Scanning

Intelligent AI Agent for customer support (chatbot + email agent)

Automation with Docker, Jenkins, and Apache Airflow

This project simulates a real-world hotel booking SaaS where customers can book rooms, upload identity documents, and interact with an AI assistant. The backend ensures fraud prevention, automation, and seamless user experience.

⚡ Features
🔹 Backend (FastAPI + PostgreSQL)

REST API endpoints for hotel bookings & user authentication

Integration with PostgreSQL for booking & user data

Fraud detection pipeline powered by LightGBM and Random Forest models

Document OCR using Tesseract to extract details from uploaded IDs

🔹 Machine Learning & AI

Fraud Detection ML Pipeline

Predicts whether a booking is fraudulent or valid

Models: LightGBM + Random Forest with feature engineering

## AI Agent System

Email Agent → Sends verification & confirmation emails to users

Fraud Detection Agent → Flags suspicious users

Chatbot Agent → Recommends offers & deals to VIP customers

## 🔹 Frontend (React + Tailwind)

Booking form with data entry + document upload

Real-time feedback on booking validation

Interactive dashboard for booking status and recommendations

## 🔹 Automation & Deployment

Dockerized microservices (Backend, Frontend, Database, OCR Service)

CI/CD with Jenkins for automated testing & deployment

Apache Airflow pipelines for ML model training, retraining, and monitoring

## 🛠️ Tech Stack

Backend: FastAPI, Python, psycopg2

Frontend: React, TailwindCSS

Database: PostgreSQL + Cloud Storage (Google Cloud for images)

Machine Learning: scikit-learn, LightGBM, pickle

OCR: Tesseract, Pillow

AI Agents: LangChain / AutoGen (for chatbot & email workflow)

## DevOps: Docker, Jenkins, Apache Airflow

📂 Project Structure
``` bash
hotel_booking_pipeline/
│── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entrypoint
│ │ ├── api.py # Endpoints
│ │ ├── ml_pipeline.py # Fraud detection ML pipeline
│ │ ├── ocr_service.py # OCR extraction module
│ │ ├── email_agent.py # Email automation
│ │ └── chatbot_agent.py # AI chatbot
│ ├── models/
│ │ ├── lightgbm_model.pkl
│ │ └── random_forest.pkl
│ ├── scripts/
│ │ ├── retrain_model.py # Airflow retraining script
│ │ └── docker_build.sh
│ └── tests/
│
│── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── components/BookForm.jsx
│ │ ├── components/OCRUpload.jsx
│ │ └── components/Chatbot.jsx
│ └── public/
│
│── docker-compose.yml
│── airflow_dags/
│ └── model_retrain_dag.py
│── README.md

🚀 Quick Start
1️⃣ Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

2️⃣ Frontend (React)
cd frontend
npm install
npm start

3️⃣ Dockerized Setup
docker-compose up --build

4️⃣ Airflow (Model Retraining)
airflow dags trigger model_retrain_dag

🔮 Future Enhancements

Add multi-language support in chatbot

Integrate Stripe/PayPal payment system

Improve fraud detection using Deep Learning models

Deploy to Kubernetes cluster on GCP/AWS

📧 Contact

For inquiries or collaboration:
📩 engmohamedelshrbeny@gmail.com
