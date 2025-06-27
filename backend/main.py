from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random  # Simulating prediction (replace with actual ML model later)

app = FastAPI()

# Enable CORS so frontend (e.g., React on localhost:3000) can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema for /analyze
class AnalyzeRequest(BaseModel):
    text: str

# Predefined categories for simulation (replace with model prediction later)
POSSIBLE_CATEGORIES = [
    "depression", "anxiety", "stress", "suicidal",
    "relationship", "abuse", "addiction", "normal",
    "bipolar", "personality disorder"
]

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "✅ Backend is running"}

# Main POST endpoint to analyze text
@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")

    # TODO: Replace this random choice with real model prediction
    predicted_label = random.choice(POSSIBLE_CATEGORIES)

    return {"prediction": predicted_label}
