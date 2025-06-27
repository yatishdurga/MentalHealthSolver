import pandas as pd
import re
import nltk
import os
import sys
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split

# Download resources
nltk.download('stopwords')
nltk.download('wordnet')

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "../data/mental_health_data.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../data/cleaned")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(INPUT_PATH):
    print(f"❌ Input file not found at: {INPUT_PATH}")
    sys.exit(1)

# Read data
df = pd.read_csv(INPUT_PATH, names=["text", "label"])

# Swap columns if label looks too long
if df["label"].str.len().mean() > 100:
    print("⚠️ Swapping columns due to label length.")
    df = df.rename(columns={"text": "label", "label": "text"})

# Text cleaner
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

# Apply cleaning
print("🧹 Cleaning data...")
df["text"] = df["text"].apply(clean_text)
df["label"] = df["label"].astype(str).str.strip().str.lower()
df["label"] = df["label"].str.replace(r"[^\w\s]", "", regex=True)

# CATEGORY MAP (expanded)
CATEGORY_MAP = {
    "depression": [
        "depression", "feeling low", "sad", "hopeless", "crying",
        "empty", "numb", "worthless", "useless", "miserable", "exhausted", 
        "drained", "hollow", "broken", "shattered", "defeated", "lost", 
        "trapped", "stuck", "burden", "failure", "pathetic", "disgusting", 
        "horrible", "awful", "terrible", "unhappy", "sobbing", "weeping",
        "tears", "lonely", "isolation", "withdrawn", "disconnected",
        "cant sleep", "cant eat", "cant function", "cant concentrate", 
        "no energy", "no motivation", "no interest", "no hope", "no point",
        "giving up", "not worth it", "avoiding", "hiding", "slump",
        "depressed", "depressing", "down", "blues", "melancholy", "grief",
        "despair", "gloomy", "dark", "heavy", "tired", "fatigued",
        "unmotivated", "apathetic", "indifferent", "detached"
    ],
    "anxiety": [
        "anxiety", "panic", "nervous", "worried",
        "scared", "afraid", "fearful", "terrified", "panicked", "anxious", 
        "restless", "tense", "jittery", "on edge", "paranoid", "uneasy",
        "apprehensive", "distressed", "agitated", "overwhelmed",
        "panic attack", "heart racing", "sweating", "trembling", "shaking", 
        "breathing hard", "breathing fast", "chest pain", "chest tight", 
        "dizzy", "nauseous", "palpitations", "shortness of breath",
        "catastrophizing", "overthinking", "racing thoughts", "cant stop thinking", 
        "worst case", "what if", "something bad", "intrusive thoughts",
        "health anxiety", "hypochondriac", "medical anxiety", "symptoms",
        "disease", "illness", "doctor", "hospital", "tests"
    ],
    "stress": [
        "stress", "overwhelmed", "burnout", 
        "pressured", "rushed", "frazzled", "stretched", "strained", 
        "overloaded", "breaking point", "tension", "pressure", "burden",
        "too much", "cant handle", "falling behind", "struggling", 
        "drowning", "suffocating", "crushing", "exhausting",
        "deadlines", "workload", "responsibilities", "demands", 
        "expectations", "busy", "hectic", "chaotic", "intense",
        "tense", "tight", "wound up", "frustrated", "irritated", 
        "snapping", "short temper", "losing it"
    ],
    "suicidal": [
        "suicide", "ending life", "self-harm",
        "want to die", "wish i was dead", "end my life", "kill myself", 
        "suicidal", "ending it", "not wanting to live", "rather be dead",
        "death", "dying", "disappear", "vanish", "gone", "escape",
        "cutting", "self harm", "self injury", "overdose", "hanging", 
        "jumping", "shooting", "pills", "blade", "razor", "wrist",
        "gun", "rope", "bridge", "building", "cliff",
        "plan", "method", "note", "goodbye", "final", "last time", 
        "end the pain", "peace", "relief", "freedom", "painless",
        "no way out", "cant go on", "give up", "done", "finished",
        "over", "enough", "tired of living", "better off dead"
    ],
    "relationship": [
        "breakup", "relationship", "partner", "divorce",
        "boyfriend", "girlfriend", "husband", "wife", "marriage", 
        "dating", "love", "heartbreak", "betrayal", "cheating", 
        "infidelity", "separation", "split", "ended", "over",
        "rejected", "abandoned", "lonely", "jealous", "hurt", 
        "betrayed", "used", "unloved", "unwanted", "alone",
        "toxic", "abusive", "controlling", "manipulative", 
        "codependent", "distant", "cold", "fighting", "arguing"
    ],
    "abuse": [
        "abuse", "violence", "trauma", "molested",
        "physical abuse", "sexual abuse", "emotional abuse", 
        "verbal abuse", "psychological abuse", "domestic violence",
        "rape", "assault", "attacked", "beaten", "hit", "hurt",
        "ptsd", "flashbacks", "nightmares", "triggered", 
        "dissociation", "panic", "fear", "terror", "helpless",
        "childhood trauma", "family violence", "bullying", 
        "harassment", "intimidation", "threats", "victim", "survivor"
    ],
    "addiction": [
        "addiction", "alcohol", "drugs", "smoking",
        "alcoholic", "drinking", "drunk", "beer", "wine", "vodka",
        "cocaine", "heroin", "meth", "opioids", "pills", "weed", 
        "marijuana", "cannabis", "cigarettes", "nicotine", "vaping",
        "using", "high", "overdose", "withdrawal", "detox", 
        "rehab", "recovery", "relapse", "sober", "clean",
        "dependent", "addicted", "craving", "need", "cant stop",
        "out of control", "destroying", "ruining"
    ],
    "normal": [
        "happy", "fine", "okay", "no problem", "normal",
        "good", "great", "wonderful", "amazing", "fantastic", 
        "excited", "joyful", "content", "peaceful", "calm",
        "relaxed", "comfortable", "satisfied", "pleased",
        "alright", "well", "decent", "regular", "typical", 
        "usual", "ordinary", "everyday", "routine", "standard",
        "fun", "enjoying", "laughing", "smiling", "celebrating",
        "love", "grateful", "thankful", "blessed", "lucky"
    ],
    "bipolar": [
        "bipolar", "manic", "mania", "mood swings", "up and down", 
        "high and low", "elevated", "euphoric", "grandiose", "impulsive", 
        "reckless", "racing thoughts", "hypomanic", "hypomania", 
        "mixed state", "episode", "cycling", "triggered", "stable", 
        "unstable", "rapid cycling", "mood disorder", "psychiatrist", 
        "medication", "med", "mood stabilizer", "antipsychotic",
        "lithium", "lamictal", "seroquel", "abilify", "therapy"
    ],
    "personality disorder": [
        "avpd", "bpd", "personality disorder", "borderline", 
        "avoidant", "social anxiety", "antisocial", "narcissistic",
        "paranoid", "schizoid", "dependent", "obsessive compulsive"
    ]
}

# Flatten map for reverse lookup
TERM_TO_CATEGORY = {}
for category, keywords in CATEGORY_MAP.items():
    for keyword in keywords:
        TERM_TO_CATEGORY[keyword.strip().lower()] = category

def map_to_category(label):
    label = label.lower().strip()
    label = re.sub(r"[^\w\s]", "", label)
    return TERM_TO_CATEGORY.get(label, None)

df["label"] = df["label"].map(map_to_category)

# Drop unmapped
df = df[df["label"].notnull()]

# Filter long/empty
df = df[df["text"].str.strip() != ""]
df = df[df["text"].str.len() <= 4900]

print(f"📊 Data after initial cleaning: {len(df)} rows")
print(f"📊 Label distribution before filtering:")
print(df["label"].value_counts().sort_index())

# IMPROVED: Remove rare labels with stricter minimum
MIN_SAMPLES_PER_LABEL = 10  # Increased from 2 to ensure stable splits
label_counts = df["label"].value_counts()
valid_labels = label_counts[label_counts >= MIN_SAMPLES_PER_LABEL].index
df = df[df["label"].isin(valid_labels)]

print(f"\n📊 After removing labels with < {MIN_SAMPLES_PER_LABEL} samples:")
print(f"📊 Remaining rows: {len(df)}")
print(f"📊 Remaining categories: {df['label'].nunique()}")
print(f"📊 Final label distribution:")
print(df["label"].value_counts().sort_index())

# IMPROVED: Safer train-test split
def safe_train_test_split(df, test_size=0.2, random_state=42):
    """
    Perform train-test split ensuring all labels appear in both sets
    """
    try:
        # Try stratified split first
        train_df, test_df = train_test_split(
            df, 
            test_size=test_size, 
            stratify=df["label"], 
            random_state=random_state
        )
        
        # Verify all labels are in both sets
        train_labels = set(train_df['label'].unique())
        test_labels = set(test_df['label'].unique())
        
        if train_labels == test_labels:
            print("✅ Stratified split successful - all labels in both sets")
            return train_df, test_df
        else:
            print("⚠️ Stratified split failed - falling back to manual split")
            raise ValueError("Label mismatch")
            
    except (ValueError, Exception) as e:
        print(f"⚠️ Stratified split failed: {e}")
        print("🔄 Using manual split to ensure label consistency...")
        
        # Manual split ensuring each label appears in both sets
        train_dfs = []
        test_dfs = []
        
        for label in df['label'].unique():
            label_data = df[df['label'] == label].copy()
            n_samples = len(label_data)
            
            # Ensure at least 1 sample in test, rest in train
            n_test = max(1, int(n_samples * test_size))
            n_train = n_samples - n_test
            
            # Shuffle and split
            label_data = label_data.sample(frac=1, random_state=random_state).reset_index(drop=True)
            
            train_dfs.append(label_data.iloc[:n_train])
            test_dfs.append(label_data.iloc[n_train:n_train+n_test])
        
        train_df = pd.concat(train_dfs, ignore_index=True)
        test_df = pd.concat(test_dfs, ignore_index=True)
        
        # Shuffle the final datasets
        train_df = train_df.sample(frac=1, random_state=random_state).reset_index(drop=True)
        test_df = test_df.sample(frac=1, random_state=random_state).reset_index(drop=True)
        
        print("✅ Manual split completed - all labels guaranteed in both sets")
        return train_df, test_df

# Perform the safe split
if len(df) == 0:
    print("❌ No data remaining after filtering!")
    sys.exit(1)

train_df, test_df = safe_train_test_split(df, test_size=0.2, random_state=42)

# Final verification
train_labels = set(train_df['label'].unique())
test_labels = set(test_df['label'].unique())

print(f"\n🔍 Final verification:")
print(f"📊 Training samples: {len(train_df)}")
print(f"📊 Test samples: {len(test_df)}")
print(f"📊 Training labels: {len(train_labels)}")
print(f"📊 Test labels: {len(test_labels)}")
print(f"📊 Labels in train but not test: {train_labels - test_labels}")
print(f"📊 Labels in test but not train: {test_labels - train_labels}")

if test_labels - train_labels:
    print("❌ ERROR: Test set contains labels not in training set!")
    sys.exit(1)

if len(test_df) == 0:
    print("❌ ERROR: Test set is empty!")
    sys.exit(1)

# Verify minimum samples per label in both sets
print(f"\n📊 Training set label distribution:")
train_label_counts = train_df['label'].value_counts().sort_index()
print(train_label_counts)

print(f"\n📊 Test set label distribution:")
test_label_counts = test_df['label'].value_counts().sort_index()
print(test_label_counts)

# Save files
train_output_path = os.path.join(OUTPUT_DIR, "comprehend_train.csv")
test_output_path = os.path.join(OUTPUT_DIR, "comprehend_test.csv")

train_df.to_csv(train_output_path, index=False, header=False)
test_df.to_csv(test_output_path, index=False, header=False)

print(f"\n✅ Files saved successfully:")
print(f"📁 Training: {train_output_path}")
print(f"📁 Test: {test_output_path}")
print(f"\n🎯 Success! Data is ready for Amazon Comprehend training.")

# Additional validation - peek at first few lines
print(f"\n👀 Sample training data:")
print(train_df.head(3).to_string(index=False))
print(f"\n👀 Sample test data:")
print(test_df.head(3).to_string(index=False))