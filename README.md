#  EmotionSense AI
### AI-Powered Emotion Detection & Mental Wellness Monitoring System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![NLP](https://img.shields.io/badge/NLP-VADER%20%7C%20TextBlob%20%7C%20Transformers-purple)

> *Your personal AI companion for mental wellness tracking and emotion awareness.*

</div>

---

##  Overview

**EmotionSense AI** is a full-stack desktop application that uses Natural Language Processing (NLP) to detect emotions from text and voice input, track mood over time, visualize emotional patterns, and provide actionable mental wellness recommendations.

This project was built as an advanced final-year Computer Science project demonstrating expertise in:
- Applied NLP & AI
- Desktop GUI engineering
- Database design
- Data visualization
- Software architecture

---

##  Features

| Feature | Description |
|---|---|
|  **AI Emotion Analysis** | Multi-layer NLP engine using VADER, TextBlob, and optionally HuggingFace Transformers |
|  **Voice Input** | Speak your feelings — speech-to-text via Google Speech API |
|  **Analytics Dashboard** | Emotion frequency, stress trends, and weekly mood charts |
|  **History Log** | Full searchable record of all past analyses |
|  **PDF / CSV / Excel Reports** | One-click professional report generation |
|  **User Authentication** | Secure signup/login with SHA-256 password hashing |
|  **Emergency Detection** | Detects crisis language and surfaces helpline information |
|  **AI Chatbot Tips** | Context-aware wellness suggestions after each analysis |
|  **Dark Mode UI** | Modern dark-themed interface built with CustomTkinter |

---

##  Project Structure

```
EmotionSenseAI/
│
├── app.py                    # Entry point — run this
│
├── gui/
│   ├── __init__.py
│   └── main_window.py        # Full CustomTkinter GUI
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py         # SQLite ORM layer
│   └── emotionsense.db       # Auto-created on first run
│
├── models/
│   ├── __init__.py
│   └── emotion_analyzer.py   # NLP emotion engine
│
├── analytics/
│   ├── __init__.py
│   └── charts.py             # Matplotlib chart builders
│
├── voice/
│   ├── __init__.py
│   └── voice_handler.py      # SpeechRecognition wrapper
│
├── reports/
│   ├── __init__.py
│   ├── report_generator.py   # PDF / CSV / Excel export
│   └── output/               # Generated reports saved here
│
├── utils/
│   ├── __init__.py
│   └── helpers.py            # Shared utilities
│
├── requirements.txt
└── README.md
```

---

##  Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/EmotionSenseAI.git
cd EmotionSenseAI

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data (one-time)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 5. Run the app
python app.py
```

### PyAudio (voice support)

```bash
# Windows
pip install pyaudio

# macOS
brew install portaudio && pip install pyaudio

# Linux (Ubuntu/Debian)
sudo apt install portaudio19-dev && pip install pyaudio
```

### Optional: HuggingFace Transformers (best accuracy)

```bash
pip install transformers torch
# Downloads ~500 MB model on first run
```

---

##  How the NLP Engine Works

The emotion analysis uses a **3-tier fallback strategy**:

```
Tier 1: HuggingFace Transformers
    └── distilroberta-base emotion model
    └── Best accuracy, requires torch installation

Tier 2: VADER + Keyword Scoring
    └── Compound sentiment blended with keyword hits
    └── Fast, lightweight, no GPU needed

Tier 3: Pure Keyword Scoring
    └── Fully offline, zero dependencies
    └── Good for basic use cases
```

**Emotions detected:** Happy · Sad · Angry · Anxious · Stressed · Excited · Fearful · Neutral

Each result includes:
- Primary emotion + confidence %
- Stress level (0–100)
- All emotion scores
- Personalized wellness tips
- Emergency detection for crisis phrases

---

##  Emergency Detection

If the system detects phrases associated with self-harm or crisis thoughts:
- An alert dialog is shown immediately
- Indian mental health helpline numbers are displayed
- The user is encouraged to reach out to trusted people

---

## 📈 Technologies Used

| Category | Technology |
|---|---|
| GUI | CustomTkinter, Tkinter |
| NLP | VADER, TextBlob, NLTK, HuggingFace Transformers |
| Database | SQLite3 |
| Charts | Matplotlib |
| Voice | SpeechRecognition, PyAudio |
| Reports | ReportLab, Pandas, OpenPyXL |
| Security | SHA-256 password hashing |

---

##  Future Improvements

- [ ] Facial expression emotion detection (OpenCV + DeepFace)
- [ ] Real-time wearable integration (heart rate → stress)
- [ ] Cloud sync & multi-device support
- [ ] Mobile companion app
- [ ] GPT-4 powered conversational therapy chatbot
- [ ] Mood prediction & proactive nudges
- [ ] Dark/Light theme switch
- [ ] Multi-language support

---

<div align="center">
Made with ❤️ for mental wellness awareness<br>
<i>EmotionSense AI — Know your mind, grow your life.</i>
</div>

<div align="center">
<i>Thanks for reading ❤️</i>
</div>    
