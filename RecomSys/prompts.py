from image_loader import load_image_from_url, print_multimodal_prompt
import os
import google.generativeai as genai

os.environ["API_KEY"] = 'AIzaSyAM9tXVESdkxk9bvRSImLDmTE78TLLdtx8'
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")


# urls for room images
room_image_url = "https://storage.googleapis.com/github-repo/img/gemini/retail-recommendations/rooms/spacejoy-c0JoR_-2x3E-unsplash.jpg"

try:
    room_image = load_image_from_url(room_image_url)
except Exception as e:
    print(f"Error loading image: {e}")

prompt = "Describe what's visible in this room and the overall atmosphere:"
prompt2 = "and recommend a type of chair that would fit in it"
contents = [prompt, room_image, prompt2]


responses = model.generate_content(contents)


print("-------Prompt--------")
print_multimodal_prompt(contents)

print("\n-------Response--------")
for response in responses:
    print(response.text, end="")