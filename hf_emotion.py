
from transformers import pipeline

# Load the Hugging Face emotion classifier once
emotion_pipeline = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

def detect_mood(text):
    result = emotion_pipeline(text)[0]  # predicted label
    return result['label']
