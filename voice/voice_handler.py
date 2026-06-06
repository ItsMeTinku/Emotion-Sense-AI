"""
voice/voice_handler.py — Speech-to-text with graceful fallback.
"""
import threading
from typing import Callable, Optional

class VoiceHandler:
    def __init__(self):
        self._available = False
        self._recognizer = None
        self._sr = None
        self._init()

    def _init(self):
        try:
            import speech_recognition as sr
            self._sr = sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 300
            self._recognizer.pause_threshold  = 0.8
            self._available = True
        except ImportError:
            pass

    @property
    def available(self): return self._available

    def listen(self, on_result: Callable, timeout: int = 5):
        if not self._available:
            on_result(None, "Install: pip install speechrecognition pyaudio"); return
        def _worker():
            sr = self._sr
            try:
                with sr.Microphone() as source:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                text = self._recognizer.recognize_google(audio)
                on_result(text, None)
            except sr.WaitTimeoutError: on_result(None, "No speech detected. Try again.")
            except sr.UnknownValueError: on_result(None, "Could not understand. Speak clearly.")
            except sr.RequestError as e: on_result(None, f"API error: {e}")
            except OSError: on_result(None, "Microphone not found or PyAudio not installed.")
            except Exception as e: on_result(None, f"Voice error: {e}")
        threading.Thread(target=_worker, daemon=True).start()
