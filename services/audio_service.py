from typing import Optional
import os
import replicate

from .base_service import BaseAIService
from config import AUDIO_DURATION, AUDIO_TEMPERATURE, AUDIO_MODEL_VERSION

class AudioService(BaseAIService):
    """Service for handling audio generation using Meta's MusicGen."""
    
    def __init__(self):
        super().__init__()
        if self.validate_api_keys():
            self.client = replicate.Client(api_token=EnvironmentManager.get_api_key('REPLICATE_API_KEY'))
    
    def process(self, query: str) -> Optional[str]:
        """Process an audio generation request."""
        try:
            self.logger.info(f"Processing audio generation request: {query}")
            output = self.client.run(
                "meta/musicgen:b05b1dff1d8c6dc63d14b0cdb42135378dcb87f6373b0d3d341ede46e59e2b38",
                input={
                    "prompt": query,
                    "duration": AUDIO_DURATION,
                    "temperature": AUDIO_TEMPERATURE,
                    "model_version": AUDIO_MODEL_VERSION,
                    "output_format": "wav",
                    "continuation": False,
                    "continuation_start": 0,
                    "multi_band_diffusion": False,
                    "normalization_strategy": "peak",
                    "classifier_free_guidance": 3
                }
            )
            
            if not output:
                self.logger.warning("No audio generated")
                return None
                
            # Create audio directory if it doesn't exist
            if not os.path.exists('audio'):
                os.makedirs('audio')
            
            # Save the audio file
            filename = f"audio/{query[:30].replace(' ', '_')}.wav"
            with open(filename, 'wb') as f:
                f.write(output)
            
            self.logger.info(f"Audio saved to: {filename}")
            return filename
            
        except Exception as e:
            self.handle_error(e, f"Error processing audio request: {query}")
            return None
    
    def _get_required_api_keys(self) -> list[str]:
        """Return list of required API keys for the service."""
        return ['REPLICATE_API_KEY']