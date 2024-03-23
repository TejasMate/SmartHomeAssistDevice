# Configuration settings for SmartHomeAssistDevice

# Model Settings
MODEL_TYPE = 'openai'  # Options: 'openai' or 'phi2'
PHI2_MODEL_PATH = 'microsoft/phi-2'  # Path to the Phi-2 model

# API Keys
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
REPLICATE_API_KEY = "YOUR_REPLICATE_API_KEY"

# Speech Recognition Settings
RECORD_CHUNK = 1024
RECORD_FORMAT = "paInt16"
RECORD_CHANNELS = 1
RECORD_RATE = 44100
RECORD_SECONDS = 5

# Wake Word Settings
WAKE_WORD = "hey"

# Audio Processing Settings
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "192"

# Image Generation Settings
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 320

# Audio Generation Settings
AUDIO_DURATION = 5
AUDIO_TEMPERATURE = 1
AUDIO_MODEL_VERSION = "stereo-large"

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"