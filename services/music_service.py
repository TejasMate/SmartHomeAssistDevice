from typing import Optional
import os
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor

from .base_service import BaseAIService
from config import AUDIO_FORMAT, AUDIO_QUALITY

class MusicService(BaseAIService):
    """Service for handling music playback and downloads."""
    
    def __init__(self):
        super().__init__()
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': AUDIO_QUALITY,
            }],
        }
    
    def process(self, query: str) -> Optional[str]:
        """Process a music playback request."""
        try:
            self.logger.info(f"Processing music request: {query}")
            with ThreadPoolExecutor() as executor:
                future = executor.submit(self._download_audio, query)
                return future.result()
        except Exception as e:
            self.handle_error(e, f"Error processing music request: {query}")
            return None
    
    def _download_audio(self, query: str) -> Optional[str]:
        """Download audio from YouTube search results."""
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                self.logger.info(f"Searching for: {query}")
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                
                if not info['entries']:
                    self.logger.warning(f"No results found for '{query}'")
                    return None
                
                video_info = info['entries'][0]
                video_url = video_info['webpage_url']
                video_title = video_info['title']
                
                self.logger.info(f"Downloading '{video_title}'")
                ydl.download([video_url])
                
                audio_file = f"{video_title}.{AUDIO_FORMAT}"
                file_path = os.path.join(os.getcwd(), audio_file)
                
                self.logger.info(f"Audio saved to: {file_path}")
                return file_path
        except Exception as e:
            self.handle_error(e, "Error in audio download")
            return None
    
    def _get_required_api_keys(self) -> list[str]:
        """No API keys required for music service."""
        return []