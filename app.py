"""
EmotionSense AI — Main Entry Point
====================================
AI-Powered Emotion Detection and Mental Wellness Monitoring System

Run this file to launch the application:
    python app.py
"""

import sys
import os

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from gui.main_window import EmotionSenseApp


def main():
    """Initialize database and launch the GUI application."""
    # Auto-create / migrate the SQLite database
    db = DatabaseManager()
    db.initialize()

    # Launch the main application window
    app = EmotionSenseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
