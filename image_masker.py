from PIL import Image
import requests


def mask_image(image_url):
    orig_image = Image.open(requests.get(
        image_url, stream=True).raw).convert("RGBA")
    image = orig_image.copy()
    data = image.getdata()
    new_data = []
    for item in data:
        # If pixel is not transparent
        if item[3] > 0:
            new_data.append((0, 0, 0, 255))  # Black
        else:
            new_data.append((255, 255, 255, 255))  # White
    image.putdata(new_data)
    return image, orig_image
