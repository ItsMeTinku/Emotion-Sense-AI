"""
voice/voice_handler.py
=======================
Microphone → Speech-to-Text using SpeechRecognition + PyAudio.
Falls back gracefully when hardware/libraries are unavailable.
"""

import threading
from typing import Callable, Optional


class VoiceHandler:
    """
    Records audio from the default microphone and converts it to text.

    Usage
    -----
    vh = VoiceHandler()
    vh.listen(on_result=lambda text, err: print(text, err))
    """

    def __init__(self):
        self._available = False
        self._recognizer = None
        self._init_recognizer()

    def _init_recognizer(self):
        try:
            import speech_recognition as sr
            self._sr = sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 300
            self._recognizer.pause_threshold = 0.8
            self._available = True
        except ImportError:
            pass

    @property
    def available(self) -> bool:
        return self._available

    # ------------------------------------------------------------------
    def listen(self,
               on_result: Callable[[Optional[str], Optional[str]], None],
               timeout: int = 5):
        """
        Non-blocking listen. Calls on_result(text, error) when done.

        Parameters
        ----------
        on_result : callable(text: str | None, error: str | None)
        timeout   : seconds to wait for speech before giving up
        """
        if not self._available:
            on_result(None, "SpeechRecognition / PyAudio not installed.\n"
                            "Run: pip install speechrecognition pyaudio")
            return

        def _worker():
            sr = self._sr
            try:
                with sr.Microphone() as source:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self._recognizer.listen(source, timeout=timeout,
                                                    phrase_time_limit=15)
                text = self._recognizer.recognize_google(audio)
                on_result(text, None)
            except sr.WaitTimeoutError:
                on_result(None, "No speech detected. Please try again.")
            except sr.UnknownValueError:
                on_result(None, "Could not understand audio. Speak clearly.")
            except sr.RequestError as e:
                on_result(None, f"Google Speech API error: {e}")
            except OSError:
                on_result(None, "Microphone not found or PyAudio not installed.")
            except Exception as e:
                on_result(None, f"Voice error: {e}")

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
