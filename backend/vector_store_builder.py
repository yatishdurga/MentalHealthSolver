import json
import os
import pickle
import requests
from dotenv import load_dotenv
from tqdm import tqdm

# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Constants
INPUT_FILE = "/Users/yatishdurgaappanapalli/Desktop/Mental Health Solver/mental_health_knowledge.json"
OUTPUT_FILE = "vector_store.pkl"
EMBEDDING_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"

# Load dataset
with open(INPUT_FILE, "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format") from e

# Flatten data if it's a dict of category → [statements]
if isinstance(data, dict):
    flat_data = []
    for category, statements in data.items():
        for statement in statements:
            flat_data.append({
                "category": category,
                "statement": statement
            })
    data = flat_data

# Validate format
if not isinstance(data, list) or not all(isinstance(entry, dict) for entry in data):
    raise TypeError("Expected a list of dictionaries in the JSON file.")

# Load or initialize vector store
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "rb") as f:
        vector_store = pickle.load(f)
        processed_statements = {entry["statement"] for entry in vector_store}
        print(f"✅ Resuming from {len(vector_store)} previously saved embeddings.")
else:
    vector_store = []
    processed_statements = set()
    print("🆕 Starting fresh vector embedding...")

# Generate embeddings
for item in tqdm(data, desc="Generating embeddings"):
    category = str(item.get("category", "")).strip().lower()
    statement = str(item.get("statement", "")).strip()

    if not category or not statement or statement in processed_statements:
        continue

    full_text = f"{category}: {statement}"
    payload = {
        "model": "models/embedding-001",
        "content": {
            "parts": [{"text": full_text}]
        }
    }

    try:
        response = requests.post(
            f"{EMBEDDING_ENDPOINT}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        embedding = response.json()["embedding"]["values"]

        vector_store.append({
            "category": category,
            "statement": statement,
            "embedding": embedding
        })

        processed_statements.add(statement)

        # Save checkpoint every 500 entries
        if len(vector_store) % 500 == 0:
            with open(OUTPUT_FILE, "wb") as f:
                pickle.dump(vector_store, f)
            print(f"💾 Checkpoint saved at {len(vector_store)} vectors.")

    except requests.RequestException as e:
        print(f"❌ Failed to embed: {full_text}")
        print(response.text if 'response' in locals() else str(e))

# Final save
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(vector_store, f)

print(f"✅ Vector store saved: {OUTPUT_FILE}")
