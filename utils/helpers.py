"""
utils/helpers.py
================
Shared utility functions used across EmotionSense AI.
"""

import os
import subprocess
import sys
from datetime import datetime


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


def get_color(emotion: str) -> tuple[str, str]:
    """Return (primary_hex, dark_hex) for the emotion."""
    return EMOTION_GRADIENT.get(emotion, ("#7c6aff", "#4a3a99"))


def format_datetime(dt_str: str) -> str:
    """Format stored timestamp string for display."""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return dt_str


def open_file(path: str):
    """Open a file with the OS default application."""
    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def stress_label(level: float) -> tuple[str, str]:
    """Return (label, color) for a stress level value (0-100)."""
    if level < 25:
        return "Low 🟢", "#2ECC71"
    elif level < 50:
        return "Moderate 🟡", "#F1C40F"
    elif level < 75:
        return "High 🟠", "#E67E22"
    else:
        return "Critical 🔴", "#E74C3C"
