import http.client
import io
import typing
import urllib.request
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
import matplotlib.pyplot as plt

#following 2 functions are image displaying functions
def display_image(image: PIL_Image, max_width: int = 600, max_height: int = 350) -> None:
    image_width, image_height = image.size
    if max_width < image_width or max_height < image_height:
        image = PIL_ImageOps.contain(image, (max_width, max_height))
    display_image_compressed(image)

def display_image_compressed(pil_image: PIL_Image) -> None:
    image_io = io.BytesIO()
    pil_image.save(image_io, "jpeg", quality=80, optimize=True)
    image_bytes = image_io.getvalue()
    plt.imshow(PIL_Image.open(io.BytesIO(image_bytes)))
    plt.show()


#Following 2 functions are image loading functions
def get_image_bytes_from_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        if response.headers["Content-Type"] not in ("image/png", "image/jpeg"):
            raise Exception("Image can only be in PNG or JPEG format")
        image_bytes = response.read()
    return image_bytes

def load_image_from_url(image_url: str) -> PIL_Image:
    image_bytes = get_image_bytes_from_url(image_url)
    return PIL_Image.open(io.BytesIO(image_bytes))

def print_multimodal_prompt(contents: list):

    """
    Given contents that would be sent to Gemini,
    output the full multimodal prompt for ease of readability.
    """
    for content in contents:
        if isinstance(content, PIL_Image.Image):
            display_image(content)

        else:
            print(content)
