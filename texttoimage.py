import replicate
import requests
from PIL import Image
from io import BytesIO

# Set up the Replicate client
replicate_client = replicate.Client(api_token="r8_DC8evZ0uZiGvSshdQWLWY0PEqR9D2fT2FvN3v")

def main(prompt):

    # Run the model and generate the image
    output = replicate_client.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
        input={"prompt": prompt, "width": 512, "height": 320}
    )

    # Get the URL of the generated image
    image_url = output[0]

    # Download the image
    response = requests.get(image_url)

    # Open the image
    image = Image.open(BytesIO(response.content))

    # Save the image to a file
    image.save("generated_image.png")

    print("Image generated and saved successfully!")
    
    
if __name__ == "__main__":
    # Define the input text for image generation
    prompt = "monkey playing football with humans"
    main(prompt)