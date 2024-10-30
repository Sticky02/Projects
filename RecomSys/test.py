import google.generativeai as genai
import os
import requests
from PIL import Image
from io import BytesIO

# Set your API key
os.environ["API_KEY"] = 'AIzaSyAM9tXVESdkxk9bvRSImLDmTE78TLLdtx8'
genai.configure(api_key=os.environ["API_KEY"])

# Load an image from a URL
url = "https://storage.googleapis.com/github-repo/img/gemini/retail-recommendations/rooms/spacejoy-c0JoR_-2x3E-unsplash.jpg"  # Replace with your image URL
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Alternatively, load an image from your local device
# img = Image.open("C:\\path\\to\\your\\image.jpg")  # Replace with your local image path

# Create a prompt that includes text and the image
prompt = "What is happening in this image?"

# Use the Gemini model that supports image input
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate content using both the prompt and the image
response = model.generate_content([prompt, img])

# Print the response
print(response.text)