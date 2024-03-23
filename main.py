import pyttsx3

from services.speech_service import SpeechService
from services.model_service import ModelService
from config import MODEL_TYPE

class SmartAssistant:
    def __init__(self):
        self.speech_service = SpeechService()
        self.model_service = ModelService()
        self.engine = pyttsx3.init()
    
    def speak_response(self, text):
        """Speak the response using text-to-speech."""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def run(self):
        """Main loop for the assistant."""
        while True:
            print(f"Say 'Genius' to start recording your question... (Using {MODEL_TYPE} model)")
            
            # Listen for wake word
            transcription = self.speech_service.listen_for_wake_word()
            if not transcription:
                continue
            
            # Get user's question
            print("Say your question...")
            question = self.speech_service.process()
            if not question:
                continue
            
            # Remove wake word if present
            question = self.speech_service.remove_wake_word(question)
            print(f"You said: {question}")
            
            # Generate and speak response
            response = self.model_service.process(question)
            if response:
                print(f"AI Response: {response}")
                self.speak_response(response)

def main():
    assistant = SmartAssistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
        
