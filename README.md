# 🧠 EmotionSense AI
**AI-Powered Emotion Detection & Mental Wellness Monitoring System**

## Quick Start
```bash
pip install -r requirements.txt
python app.py
```

## Features
- 🔍 NLP emotion analysis (VADER / Transformers)
- 🎙️ Voice input via microphone
- 📊 Analytics dashboard with charts
- 📋 Full emotion history log
- 📄 PDF / CSV / Excel export
- 👤 Secure login & signup
- ⚠️ Emergency phrase detection
- 💬 AI wellness tips (randomized each analysis)

## Emotions Detected
Happy · Sad · Angry · Anxious · Stressed · Excited · Fearful · Neutral

## Structure
```
EmotionSenseAI/
├── app.py
├── gui/main_window.py
├── database/db_manager.py
├── models/emotion_analyzer.py
├── analytics/charts.py
├── voice/voice_handler.py
├── reports/report_generator.py
└── utils/helpers.py
```

## Voice Support
```bash
# Windows
pip install pyaudio
# macOS: brew install portaudio && pip install pyaudio
# Linux: sudo apt install portaudio19-dev && pip install pyaudio
```

## Optional: Best Accuracy (HuggingFace)
```bash
pip install transformers torch
```
