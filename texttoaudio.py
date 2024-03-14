import replicate
import requests
from PIL import Image
from io import BytesIO

# Set up the Replicate client
replicate_client = replicate.Client(api_token="r8_DC8evZ0uZiGvSshdQWLWY0PEqR9D2fT2FvN3v")





def main(prompt):
    
    output = replicate_client.run(
        "meta/musicgen:b05b1dff1d8c6dc63d14b0cdb42135378dcb87f6373b0d3d341ede46e59e2b38",
        input={
            "top_k": 250,
            "top_p": 0,
            "prompt": prompt,
            "duration": 5,
            "temperature": 1,
            "continuation": False,
            "model_version": "stereo-large",
            "output_format": "wav",
            "continuation_start": 0,
            "multi_band_diffusion": False,
            "normalization_strategy": "peak",
            "classifier_free_guidance": 3
        }
    )
    print(output)
    
    
if __name__ == "__main__":
    prompt = "Edo25 major g melodies that sound triumphant and cinematic. Leading up to a crescendo that resolves in a 9th harmonic"

    main(prompt)