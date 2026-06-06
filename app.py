"""
EmotionSense AI — Entry Point
==============================
Run with:  python app.py
"""

import os
import sys

# Suppress TensorFlow noise (if transformers/torch installed)
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from gui.main_window import EmotionSenseApp


def main():
    db = DatabaseManager()
    db.initialize()
    app = EmotionSenseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
