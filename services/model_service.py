from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import openai

from .base_service import BaseAIService
from utils.environment import EnvironmentManager
from config import MODEL_TYPE, PHI2_MODEL_PATH

class ModelService(BaseAIService):
    """Service for handling both local and cloud-based language models."""
    
    def __init__(self):
        super().__init__()
        self.model_type = MODEL_TYPE
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the appropriate model based on configuration."""
        if self.model_type == 'phi2':
            try:
                self.logger.info("Initializing local Phi-2 model...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    PHI2_MODEL_PATH,
                    torch_dtype=torch.float32,
                    device_map='auto'
                )
                self.tokenizer = AutoTokenizer.from_pretrained(PHI2_MODEL_PATH)
                self.logger.info("Local Phi-2 model initialized successfully")
            except Exception as e:
                self.handle_error(e, "Error initializing local Phi-2 model")
                raise RuntimeError("Failed to initialize local model. Please check model path and system resources.")
        elif self.model_type == 'openai':
            try:
                self.logger.info("Initializing online GPT-3 mode...")
                openai.api_key = EnvironmentManager.get_api_key('OPENAI_API_KEY')
                if not openai.api_key:
                    raise ValueError("OpenAI API key not found in environment")
                self.logger.info("Online GPT-3 mode initialized successfully")
            except Exception as e:
                self.handle_error(e, "Error initializing OpenAI configuration")
                raise RuntimeError("Failed to initialize online mode. Please check your API key and internet connection.")
    
    def process(self, prompt: str) -> Optional[str]:
        """Process the prompt using the selected model."""
        try:
            if self.model_type == 'phi2':
                return self._generate_local_response(prompt)
            else:
                return self._generate_openai_response(prompt)
        except Exception as e:
            self.handle_error(e, f"Error generating response with {self.model_type}")
            return None
    
    def _generate_local_response(self, prompt: str) -> str:
        """Generate response using local Phi-2 model."""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=200,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
    
    def _generate_openai_response(self, prompt: str) -> str:
        """Generate response using OpenAI's GPT-3 API."""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            self.logger.error(f"Error generating response from GPT-3: {str(e)}")
            raise RuntimeError("Failed to generate response from online GPT-3. Please check your internet connection.")
    
    def _get_required_api_keys(self) -> list[str]:
        """Return required API keys based on model type."""
        return ['OPENAI_API_KEY'] if self.model_type == 'openai' else []