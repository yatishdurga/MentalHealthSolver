from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random  # Simulating prediction (replace with actual ML model later)

app = FastAPI()

# Enable CORS so frontend (e.g., React on localhost:5174) can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # more secure than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class AnalyzeRequest(BaseModel):
    text: str

# Dummy categories for simulation
POSSIBLE_CATEGORIES = [
    "depression", "anxiety", "stress", "suicidal",
    "relationship", "abuse", "addiction", "normal",
    "bipolar", "personality disorder"
]

@app.get("/")
def health_check():
    return {"status": "✅ Backend is running"}

@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")
    
    # Simulated prediction logic
    predicted_label = random.choice(POSSIBLE_CATEGORIES)
    return {"prediction": predicted_label}
