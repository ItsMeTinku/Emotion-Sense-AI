"""
gui/main_window.py  —  Full CustomTkinter GUI for EmotionSense AI.
All fixes applied: signup resize, no email field, randomized tips.
"""
from __future__ import annotations
import json, os, tkinter as tk, tkinter.messagebox as mb, tkinter.ttk as ttk
from typing import Optional

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
except ImportError:
    raise SystemExit("Run: pip install customtkinter")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.db_manager import DatabaseManager
from models.emotion_analyzer import EmotionAnalyzer
from voice.voice_handler import VoiceHandler
from analytics import charts
from reports import report_generator
from utils.helpers import get_emoji, get_color, open_file, stress_label

C = {
    "bg":"#0f0e17","panel":"#1a1a2e","sidebar":"#16213e","card":"#1f2b47",
    "accent":"#7c6aff","accent2":"#ff6b6b","text":"#e0e0e0","muted":"#8888aa",
    "success":"#2ECC71","warning":"#F1C40F","danger":"#E74C3C","border":"#2a2a4a",
}
FT  = ("Segoe UI",22,"bold")
FH  = ("Segoe UI",14,"bold")
FB  = ("Segoe UI",11)
FS  = ("Segoe UI",9)
FM  = ("Consolas",10)

