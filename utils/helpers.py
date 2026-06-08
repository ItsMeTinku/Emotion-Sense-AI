"""
utils/helpers.py
Shared utilities for EmotionSense AI.
"""

import os
import subprocess
import sys

EMOTION_EMOJI = {
    "Happy":    "😊",
    "Sad":      "😢",
    "Angry":    "😠",
    "Anxious":  "😰",
    "Stressed": "😖",
    "Excited":  "🤩",
    "Fearful":  "😱",
    "Neutral":  "😐",
}

EMOTION_GRADIENT = {
    "Happy":    ("#FFD700", "#FFA500"),
    "Sad":      ("#4A90D9", "#2C3E7A"),
    "Angry":    ("#E74C3C", "#8B0000"),
    "Anxious":  ("#F39C12", "#B7770D"),
    "Stressed": ("#E67E22", "#B5540D"),
    "Excited":  ("#2ECC71", "#1A8A4A"),
    "Fearful":  ("#9B59B6", "#5B2C6F"),
    "Neutral":  ("#95A5A6", "#4D5656"),
}


def get_emoji(emotion: str) -> str:
    return EMOTION_EMOJI.get(emotion, "🔵")


def get_color(emotion: str) -> tuple:
    return EMOTION_GRADIENT.get(emotion, ("#7c6aff", "#4a3a99"))


def open_file(path: str):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def stress_label(level: float) -> tuple:
    if level < 25:
        return "Low 🟢", "#2ECC71"
    elif level < 50:
        return "Moderate 🟡", "#F1C40F"
    elif level < 75:
        return "High 🟠", "#E67E22"
    else:
        return "Critical 🔴", "#E74C3C"
