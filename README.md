# 🧠 EmotionSense AI

<div align="center">
  <img src="assets/logo.png" width="150" alt="EmotionSense AI Logo">
  <br>
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI-Powered-orange?style=for-the-badge" alt="AI Powered">
  <img src="https://img.shields.io/badge/UI-CustomTkinter-blueviolet?style=for-the-badge" alt="UI CustomTkinter">
  <img src="https://img.shields.io/badge/Open%20Source-Heart-red?style=for-the-badge" alt="Open Source">
</div>

---

![EmotionSense AI Banner](assets/banner.png)

## 🌟 Overview
**EmotionSense AI** is a state-of-the-art mental wellness monitoring and emotion detection system. It leverages advanced NLP techniques and voice recognition to provide real-time emotional insights, helping users track their mental state and generate detailed wellness reports.

Built with a focus on both performance and user experience, the application features a modern, glassmorphism-inspired UI powered by `CustomTkinter`.

## ✨ Key Features
- 🎭 **Real-time Emotion Analysis**: Analyze text or voice input to detect primary emotions (Joy, Sadness, Anger, Fear, etc.).
- 🎙️ **Voice Recognition**: Integrated speech-to-text for hands-free emotional tracking.
- 📊 **Smart Analytics**: Interactive charts and data visualizations tracking emotional trends over time.
- 📄 **Exportable Reports**: Generate professional PDF or Excel summaries of emotional wellness data.
- 🔒 **Secure Local Database**: All data is stored locally using SQLite for maximum privacy.
- 🎨 **Modern Dark UI**: A sleek, user-friendly interface that feels premium and responsive.

## 🛠️ Tech Stack
- **Frontend**: CustomTkinter (Modern Python GUI)
- **Sentiment Engine**: VADER, TextBlob, NLTK
- **Optional AI**: HuggingFace Transformers (RoBERTa/BERT)
- **Audio**: SpeechRecognition, PyAudio
- **Visualization**: Matplotlib, Pandas
- **Reporting**: ReportLab, OpenPyXL
- **Database**: SQLite3

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Microphone (for voice recognition features)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/EmotionSenseAI.git
   cd EmotionSenseAI
   ```

2. **Set up a virtual environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
```bash
python app.py
```

## 📂 Project Structure
```text
EmotionSenseAI/
├── analytics/         # Data processing and chart generation
├── assets/            # UI images, banners, and icons
├── database/          # SQLite schema and DB managers
├── gui/               # CustomTkinter windows and components
├── models/            # NLP models and emotion wrappers
├── reports/           # PDF and Excel export logic
├── voice/             # Speech-to-text integration
├── app.py             # Main entry point
└── requirements.txt   # Project dependencies
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

# Note
## Contribution

This project was originally developed as a basic emotion recommendation system. My contributions focused on enhancing the application's functionality, user experience, and analytics capabilities.

### Key Contributions

* Developed and improved the frontend interface.
* Expanded the emotion recommendation dataset to provide more diverse and relevant suggestions.
* Enhanced recommendation logic to generate a larger set of personalized tips.
* Implemented emotion history tracking and data persistence.
* Added mood analytics, trend charts, and emotion distribution visualizations.
* Improved emotion analysis by considering historical emotional patterns rather than only the current mood entry.
* Enhanced the overall workflow and user experience of the application.

---
<div align="center">
  Made with ❤️ for Mental Wellness
</div>
