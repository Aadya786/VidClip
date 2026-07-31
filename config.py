import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 60
MAX_OUTPUT_CLIPS = 3

WEIGHT_HEATMAP = 0.40
WEIGHT_AUDIO_ENERGY = 0.25
WEIGHT_LLM_SCORE = 0.35

FALLBACK_KEYWORDS = [
    "insane", "unbelievable", "secret", "crazy", "funny", 
    "mistake", "never", "always", "best", "worst", "why", "cool",
    "passion", "work", "focus", "push", "persist", "idea"
]
