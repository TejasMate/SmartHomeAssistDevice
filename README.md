# SmartHomeAssistDevice

A modern voice-controlled home assistant device that can play music, generate images, create audio, and more. Supports both cloud-based and local language models for enhanced flexibility and privacy.

## Features

- Dual-mode language model support (OpenAI API or local Phi-2 model)
- Voice activation with customizable wake word
- Music playback from YouTube
- Image generation using Stable Diffusion
- Audio generation using Meta's MusicGen
- Speech recognition and text-to-speech capabilities

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   - OpenAI API key (if using OpenAI mode)
   - Replicate API key

## Usage

1. Run the assistant:
   ```bash
   python main.py
   ```
2. Say the wake word (default: "hey")
3. Give a command:
   - "play song [song name]"
   - "generate image [description]"
   - "generate audio [description]"

## Configuration

Adjust settings in `config.py`:
- MODEL_TYPE: Choose between 'openai' (cloud-based) or 'phi2' (local model)
- Wake word
- Audio recording parameters
- Image generation settings
- Logging preferences

For local model setup:
- PHI2_MODEL_PATH: Path to the Phi-2 model (default: 'microsoft/phi-2')
- No API key required for local model mode

## Development

- Uses modern Python practices
- Includes logging for debugging
- Configurable settings
- Error handling
- Multi-threading support

## Requirements

- Python 3.8+
- See requirements.txt for package dependencies