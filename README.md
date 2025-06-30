# 🧠 Mental Health Solver — AI-Powered Assistant using AWS Lambda & Gemini

An AI-powered mental health assistant that uses Google Gemini, semantic search (RAG), and AWS Lambda to deliver personalized support, books, videos, and motivation to users based on their mental well-being inputs.

---

## 🏗️ Architecture Overview


---

## ⚙️ Tech Stack & AWS Services

| Layer        | Technologies Used                                     |
|--------------|--------------------------------------------------------|
| Frontend     | React.js, Bootstrap, Axios                            |
| Backend      | FastAPI, Google Gemini API, FAISS-style semantic search |
| ML/NLP       | Gemini 1.5 Flash, Embedding API                       |
| AWS Services | Lambda (core logic), API Gateway (trigger), S3 (data), CloudWatch (logs), IAM (roles/policies) |

---

## 🚀 Features

- ✅ Text classification into mental health categories (e.g., anxiety, depression)
- ✅ Semantic similarity search using vector embeddings
- ✅ RAG-style prompts powered by Gemini
- ✅ Personalized tips, books, videos, quotes
- ✅ Fully serverless deployment using AWS Lambda
- ✅ React-based frontend UI

---

## 📁 Folder Structure


---

## 🛠️ Setup Instructions

### 1. 🧠 Gemini API Setup
- Get your Gemini API key from [Google AI Studio](https://makersuite.google.com).
- Add to `.env`:
  ```env
  GEMINI_API_KEY=your_api_key
  EMBEDDING_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent


Deploy Backend on AWS Lambda
Go to AWS Lambda → Create Function → Use existing role

Upload lambda-deploy.zip via S3

Set Lambda handler: main.lambda_handler

Add environment variables for:

GEMINI_API_KEY

EMBEDDING_ENDPOINT

S3_BUCKET_NAME

S3_TIPS_FILE

Connect API Gateway (POST trigger)


Deploy Frontend on AWS Amplify

cd frontend/
npm install
npm run build



Tools & Services Used
AWS Lambda – Serverless backend

API Gateway – HTTP trigger for Lambda

Amazon S3 – Stores vector store & mental health JSON data

Google Gemini – Embedding + Content generation

React.js – Frontend UI

FastAPI – Local development backend

CloudWatch – Logs and monitoring


Future Enhancements
🔒 JWT-based user authentication

🧠 Fine-tuned Gemini models

📊 Real-time analytics dashboard

💬 Chatbot integration with memory
