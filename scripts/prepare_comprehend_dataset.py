import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split

# One-time downloads
nltk.download('stopwords')
nltk.download('wordnet')

# Load dataset
df = pd.read_csv("data/mental_health_data.csv")

# Clean text
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Apply text cleaning
df['statement'] = df['statement'].apply(clean_text)

# Rename columns
df = df[['statement', 'status']]
df.columns = ['text', 'label']

# 🔥 Remove blank or null labels
df = df[df['label'].notnull()]
df = df[df['label'].astype(str).str.strip() != ""]

# Split into train/test
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

# Save files (no header for Comprehend)
train_df.to_csv("data/comprehend_train.csv", index=False, header=False)
test_df.to_csv("data/comprehend_test.csv", index=False, header=False)

print("✅ Comprehend training and test files created.")
