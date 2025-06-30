import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("backend/mental_health_data.csv")

# Drop rows where 'status' or 'statement' is missing
df = df.dropna(subset=["status", "statement"])

# Convert to list of dictionaries for RAG compatibility
formatted_data = []

for _, row in df.iterrows():
    category = str(row["status"]).strip().lower()
    statement = str(row["statement"]).strip()

    # Skip empty entries just in case
    if category and statement:
        formatted_data.append({
            "category": category,
            "statement": statement
        })

# Save to JSON
with open("mental_health_knowledge.json", "w") as f:
    json.dump(formatted_data, f, indent=2)

print("✅ Dataset preprocessing complete. File saved as mental_health_knowledge.json.")
