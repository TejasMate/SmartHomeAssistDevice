from typing import Optional
import speech_recognition as sr

from .base_service import BaseAIService
from config import RECORD_CHUNK, RECORD_FORMAT, RECORD_CHANNELS, RECORD_RATE, RECORD_SECONDS, WAKE_WORD

class SpeechService(BaseAIService):
    """Service for handling speech recognition and wake word detection."""
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
    
    def process(self, audio_data: Optional[sr.AudioData] = None) -> Optional[str]:
        """Process audio data for speech recognition."""
        try:
            if audio_data:
                self.logger.info("Processing provided audio data")
                return self.recognizer.recognize_google(audio_data)
            else:
                self.logger.info("Listening for speech...")
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=RECORD_SECONDS)
                return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.handle_error(e, "Error accessing Google Speech Recognition service")
            return None
        except Exception as e:
            self.handle_error(e, "Unexpected error in speech recognition")
            return None
    
    def listen_for_wake_word(self) -> Optional[str]:
        """Listen for the wake word and return the full transcription if found."""
        try:
            self.logger.info("Listening for wake word...")
            transcription = self.process()
            
            if transcription and WAKE_WORD.lower() in transcription.lower():
                self.logger.info(f"Wake word detected in: {transcription}")
                return transcription
            return None
            
        except Exception as e:
            self.handle_error(e, "Error in wake word detection")
            return None
    
    def remove_wake_word(self, transcription: str) -> str:
        """Remove wake word and other trigger words from transcription."""
        words_to_remove = [WAKE_WORD, "genius"]
        word_list = transcription.split()
        new_word_list = [word for word in word_list if word.lower() not in words_to_remove]
        return " ".join(new_word_list)
    
    def _get_required_api_keys(self) -> list[str]:
        """No API keys required for speech recognition service."""
        return []