from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
import os
import boto3
import json
import requests
from semantic_search import find_similar_statements

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_ENDPOINT = os.getenv(
    "EMBEDDING_ENDPOINT",
    "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Load mental health tips from S3
s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "mental-health-solver-yatish-0622")
OBJECT_KEY = os.getenv("S3_TIPS_FILE", "mental_health_tips.json")

try:
    s3_response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
    CATEGORIES = json.loads(s3_response["Body"].read())
except Exception as e:
    print(f"⚠️ Error loading knowledge base from S3: {e}")
    CATEGORIES = {}

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

def classify_text_with_gemini(text: str, similar: list) -> str:
    # Construct prompt using RAG context
    similar_text = '\n'.join(
        f'- "{s["statement"].strip()}" (Category: {s["category"]})'
        for s in similar
    )

    prompt = f"""
You are a helpful and compassionate AI mental health assistant.

Given this user message:
"{text}"

And similar expressions:
{similar_text}

Classify the user’s concern into one of these categories:
depression, anxiety, stress, normal, relationship, addiction, abuse, bipolar, personality disorder.

Only return the category name.
"""

    response = model.generate_content(prompt)
    category = response.text.strip().lower()
    return category if category in CATEGORIES else "normal"

@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")

    try:
        # Step 1: Get embedding
        embed_payload = {
            "model": "models/embedding-001",
            "content": {"parts": [{"text": request.text}]}
        }
        embed_response = requests.post(
            f"{EMBEDDING_ENDPOINT}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=embed_payload
        )
        embed_response.raise_for_status()
        query_embedding = embed_response.json()["embedding"]["values"]

        # Step 2: RAG - Semantic Search
        similar_statements = find_similar_statements(query_embedding, top_k=5)

        # Step 3: Classify
        category = classify_text_with_gemini(request.text, similar_statements)
        suggestions = CATEGORIES.get(category, CATEGORIES.get("normal", {}))

        return {
            "prediction": category,
            "tips": suggestions.get("tips", []),
            "books": suggestions.get("books", []),
            "videos": suggestions.get("videos", []),
            "quotes": suggestions.get("quotes", []),
        }

    except Exception as e:
        print(f"❌ Exception during /analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
