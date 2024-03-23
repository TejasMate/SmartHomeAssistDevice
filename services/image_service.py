from typing import Optional
import os
import replicate
from PIL import Image
from io import BytesIO
import requests
import fcntl
import mmap

from .base_service import BaseAIService
from config import IMAGE_WIDTH, IMAGE_HEIGHT

class ImageService(BaseAIService):
    """Service for handling image generation using Stable Diffusion."""
    
    def __init__(self):
        super().__init__()
        if self.validate_api_keys():
            self.client = replicate.Client(api_token=EnvironmentManager.get_api_key('REPLICATE_API_KEY'))
    
    def process(self, query: str) -> Optional[str]:
        """Process an image generation request."""
        try:
            self.logger.info(f"Processing image generation request: {query}")
            output = self.client.run(
                "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
                input={
                    "prompt": query,
                    "width": IMAGE_WIDTH,
                    "height": IMAGE_HEIGHT
                }
            )
            
            if not output:
                self.logger.warning("No image generated")
                return None
                
            image_url = output[0]
            return self._save_image(image_url, query)
            
        except Exception as e:
            self.handle_error(e, f"Error processing image request: {query}")
            return None
    
    def _save_image(self, image_url: str, prompt: str) -> Optional[str]:
        """Download and save the generated image."""
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # Create images directory if it doesn't exist
            if not os.path.exists('images'):
                os.makedirs('images')
            
            # Create a filename from the prompt
            filename = f"images/{prompt[:30].replace(' ', '_')}.png"
            image.save(filename)
            
            self.logger.info(f"Image saved to: {filename}")
            return filename
            
        except Exception as e:
            self.handle_error(e, "Error saving image")
            return None
    
    def _get_required_api_keys(self) -> list[str]:
        """Return list of required API keys for the service."""
        return ['REPLICATE_API_KEY']

    def display_on_pi(self, image_path: str) -> bool:
        """Display the generated image on Raspberry Pi display using framebuffer."""
        try:
            # Open the framebuffer device
            fb = open('/dev/fb0', 'rb+') 
            
            # Get screen info
            screen_info = fcntl.ioctl(fb, 0x4600, bytes([0] * 160))
            
            # Open and resize image to match screen resolution
            with Image.open(image_path) as img:
                # Assuming 1920x1080 resolution, adjust if needed
                img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                pixels = img.tobytes()
                
                # Write to framebuffer
                fb.seek(0)
                fb.write(pixels)
                fb.close()
                
            self.logger.info(f"Image displayed successfully on Pi display: {image_path}")
            return True
            
        except Exception as e:
            self.handle_error(e, "Error displaying image on Pi")
            return False