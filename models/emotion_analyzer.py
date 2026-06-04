"""
models/emotion_analyzer.py
===========================
Multi-layer NLP emotion detection engine.

Strategy (in order of preference):
  1. HuggingFace transformers — best accuracy, requires torch install
  2. VADER + TextBlob — lightweight fallback, zero GPU needed
  3. Pure keyword scoring  — offline last resort

Detected emotions: Happy, Sad, Angry, Anxious, Stressed,
                   Excited, Fearful, Neutral
"""

import re
import json
import random
from typing import Optional

# ---------------------------------------------------------------------------
# Emotion keyword lexicon (scored 0-1 per match)
# ---------------------------------------------------------------------------
EMOTION_KEYWORDS: dict[str, list[str]] = {
    "Happy":   ["happy", "joyful", "great", "wonderful", "fantastic", "cheerful",
                "delighted", "pleased", "glad", "content", "love", "grateful",
                "blessed", "awesome", "amazing", "good", "fine", "smile"],
    "Sad":     ["sad", "depressed", "unhappy", "miserable", "sorrow", "grief",
                "cry", "tears", "heartbroken", "down", "gloomy", "hopeless",
                "lonely", "worthless", "empty", "broken", "numb"],
    "Angry":   ["angry", "furious", "rage", "mad", "annoyed", "irritated",
                "frustrated", "hate", "disgusted", "outraged", "fed up"],
    "Anxious": ["anxious", "anxiety", "nervous", "worried", "panic", "dread",
                "apprehensive", "uneasy", "tense", "restless", "overthinking"],
    "Stressed":["stressed", "stress", "overwhelmed", "burnout", "pressure",
                "exhausted", "overloaded", "deadline", "swamped", "drained"],
    "Excited": ["excited", "thrilled", "ecstatic", "pumped", "enthusiastic",
                "eager", "hyped", "anticipate", "can't wait", "energized"],
    "Fearful": ["scared", "afraid", "fear", "terrified", "horror", "phobia",
                "frightened", "dread", "nightmare", "unsafe", "threatened"],
}

EMERGENCY_PHRASES = [
    "want to die", "kill myself", "end my life", "hate my life",
    "hurt myself", "no reason to live", "give up on life",
    "want to disappear", "take my own life",
]

WELLNESS_TIPS: dict[str, list[str]] = {
    "Happy":    [
        "Keep spreading positivity — it's contagious! 🌟",
        "Channel this energy into something creative. 🎨",
        "Share your happiness with someone who needs it today. 💛",
        "Write down what made you happy — revisit it on harder days. 📓",
        "Use this good mood to tackle something you've been avoiding. 🚀",
    ],
    "Sad":      [
        "It's okay to feel sad. Take it one breath at a time. 🌬️",
        "Consider talking to a trusted friend or counsellor. 💬",
        "A short walk outside can help lift your mood. 🚶",
        "Put on your favourite music and let yourself feel it. 🎵",
        "Write your feelings down — journalling helps process sadness. ✍️",
        "Drink some water, eat something warm. Small self-care matters. 🍵",
        "Remember: this feeling is temporary. You've survived hard days before. 💙",
    ],
    "Angry":    [
        "Try box breathing: inhale 4s → hold 4s → exhale 4s → hold 4s. 🧘",
        "Write down what made you angry — it helps release the charge. ✍️",
        "Step outside for 5 minutes before responding to anything. 🌿",
        "Physical movement like a brisk walk burns off anger energy. 🏃",
        "Ask yourself: will this matter in 5 years? 🔭",
        "Splash cold water on your face — it activates the calming reflex. 💧",
    ],
    "Anxious":  [
        "Ground yourself: name 5 things you can see right now. 👀",
        "Progressive muscle relaxation — tense each muscle group then release. 💪",
        "Anxiety is your brain trying to protect you. Thank it, then breathe. 🧠",
        "Write your worries down and ask: is this within my control? 📋",
        "Try 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s. 😮‍💨",
        "Limit caffeine today — it amplifies anxiety significantly. ☕",
        "Call or text someone you trust right now. 📱",
    ],
    "Stressed": [
        "Break your workload into smaller, timed chunks (Pomodoro: 25 min on, 5 off). ⏱️",
        "Even a 10-minute break dramatically reduces cortisol. ☕",
        "Write a priority list — stress often comes from feeling out of control. 📝",
        "Stretch your neck and shoulders — stress lives in the body too. 🤸",
        "Say no to one thing today. Boundaries reduce stress. 🚫",
        "Take 3 deep slow breaths right now before doing anything else. 🌬️",
        "Remember: you don't have to solve everything today. 🗓️",
    ],
    "Excited":  [
        "Use this excitement to tackle a goal you've delayed! 🚀",
        "Channel it into planning something meaningful. 📋",
        "Share your excitement — enthusiasm is infectious! 🎉",
        "Write down what's exciting you so you can revisit this feeling. 📓",
        "Excited energy is perfect for creative work. 🎨",
    ],
    "Fearful":  [
        "Acknowledge your fear — it's a signal, not a verdict. 🔦",
        "Speak to someone you trust about what's worrying you. 🤝",
        "Ask yourself: what's the realistic worst case? Can I handle it? 🧩",
        "Fear shrinks when you take one small action toward it. 👣",
        "Slow your breathing — fear accelerates it, calm reverses it. 😮‍💨",
        "Write the fear down. Named fears feel less powerful. ✍️",
    ],
    "Neutral":  [
        "A calm mind is a powerful mind. 🧠",
        "Try mindful journalling to explore your inner state. 📓",
        "This is a great time to set an intention for the rest of your day. 🎯",
        "Use this steady energy for focused, deep work. 💻",
        "Check in with someone you haven't spoken to in a while. 📱",
    ],
}


class EmotionAnalyzer:
    """
    Analyzes text and returns emotion scores, primary emotion,
    confidence, stress level, and wellness tips.
    """

    def __init__(self):
        self._transformers_pipe = None
        self._vader = None
        self._load_models()

    # ------------------------------------------------------------------
    # Model loading (graceful degradation)
    # ------------------------------------------------------------------
    def _load_models(self):
        # 1. Try HuggingFace transformers (emotion model)
        try:
            from transformers import pipeline
            self._transformers_pipe = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,
            )
            print("[EmotionAnalyzer] Using HuggingFace transformers.")
            return
        except Exception:
            pass

        # 2. Try VADER
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            import nltk
            try:
                nltk.data.find("tokenizers/punkt")
            except LookupError:
                nltk.download("punkt", quiet=True)
                nltk.download("stopwords", quiet=True)
            self._vader = SentimentIntensityAnalyzer()
            print("[EmotionAnalyzer] Using VADER + keyword scoring.")
            return
        except Exception:
            pass

        # 3. Pure keyword fallback
        print("[EmotionAnalyzer] Using pure keyword scoring (offline mode).")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def analyze(self, text: str) -> dict:
        """
        Returns:
            {
              "primary_emotion": str,
              "confidence": float (0-100),
              "stress_level": float (0-100),
              "scores": {emotion: float, ...},
              "tips": [str, ...],
              "is_emergency": bool,
              "emergency_message": str,
            }
        """
        text_clean = text.strip()
        is_emergency = self._check_emergency(text_clean)

        if self._transformers_pipe:
            scores = self._run_transformers(text_clean)
        elif self._vader:
            scores = self._run_vader_plus_keywords(text_clean)
        else:
            scores = self._run_keywords_only(text_clean)

        # Normalize to percentages
        total = sum(scores.values()) or 1
        scores_pct = {k: round(v / total * 100, 1) for k, v in scores.items()}

        primary = max(scores_pct, key=scores_pct.get)
        confidence = scores_pct[primary]
        stress_level = self._compute_stress(scores_pct)
        all_tips = WELLNESS_TIPS.get(primary, WELLNESS_TIPS["Neutral"])
        tips = random.sample(all_tips, min(2, len(all_tips)))

        return {
            "primary_emotion": primary,
            "confidence": confidence,
            "stress_level": stress_level,
            "scores": scores_pct,
            "scores_json": json.dumps(scores_pct),
            "tips": tips,
            "is_emergency": is_emergency,
            "emergency_message": self._emergency_message() if is_emergency else "",
        }

    # ------------------------------------------------------------------
    # Backend implementations
    # ------------------------------------------------------------------
    def _run_transformers(self, text: str) -> dict[str, float]:
        """Map HuggingFace model labels → our 8 categories."""
        HF_MAP = {
            "joy":      "Happy",
            "love":     "Happy",
            "surprise": "Excited",
            "anger":    "Angry",
            "disgust":  "Angry",
            "sadness":  "Sad",
            "fear":     "Fearful",
            "neutral":  "Neutral",
        }
        raw = self._transformers_pipe(text[:512])[0]   # list of {label, score}
        scores: dict[str, float] = {e: 0.0 for e in EMOTION_KEYWORDS}
        scores["Neutral"] = 0.0
        for item in raw:
            label = item["label"].lower()
            target = HF_MAP.get(label, "Neutral")
            scores[target] = scores.get(target, 0.0) + item["score"]
        return scores

    def _run_vader_plus_keywords(self, text: str) -> dict[str, float]:
        """VADER polarity blended with keyword frequency."""
        vs = self._vader.polarity_scores(text)
        # VADER compound: +1 very positive, -1 very negative
        compound = vs["compound"]

        kw_scores = self._run_keywords_only(text)

        # Boost Happy/Sad/Angry using compound score
        if compound >= 0.2:
            kw_scores["Happy"] = kw_scores.get("Happy", 0) + compound * 2
        elif compound <= -0.2:
            kw_scores["Sad"] = kw_scores.get("Sad", 0) + abs(compound) * 1.5
            kw_scores["Angry"] = kw_scores.get("Angry", 0) + abs(compound) * 0.8

        # Ensure at least a tiny Neutral baseline
        kw_scores.setdefault("Neutral", 0.1)
        return kw_scores

    def _run_keywords_only(self, text: str) -> dict[str, float]:
        """Score each emotion category by keyword hits."""
        words = set(re.findall(r"\b\w+\b", text.lower()))
        scores: dict[str, float] = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw in words or kw in text.lower())
            scores[emotion] = float(hits)
        scores["Neutral"] = max(0.1, 1.0 - min(sum(scores.values()), 5) / 5)
        return scores

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _compute_stress(scores_pct: dict[str, float]) -> float:
        """Stress proxy: weighted sum of negative emotions."""
        STRESS_WEIGHTS = {
            "Stressed": 1.0, "Anxious": 0.9, "Fearful": 0.8,
            "Sad": 0.7, "Angry": 0.6,
        }
        raw = sum(scores_pct.get(e, 0) * w for e, w in STRESS_WEIGHTS.items())
        # Normalize to 0-100
        return round(min(raw / max(sum(STRESS_WEIGHTS.values()), 1), 100), 1)

    @staticmethod
    def _check_emergency(text: str) -> bool:
        t = text.lower()
        return any(phrase in t for phrase in EMERGENCY_PHRASES)

    @staticmethod
    def _emergency_message() -> str:
        return (
            "⚠️  We noticed some concerning thoughts in your message.\n\n"
            "You are not alone. Please reach out:\n"
            "  • iCall (India): 9152987821\n"
            "  • Vandrevala Foundation: 1860-2662-345\n"
            "  • NIMHANS helpline: 080-46110007\n\n"
            "Talking to someone you trust can make a real difference. 💙"
        )
