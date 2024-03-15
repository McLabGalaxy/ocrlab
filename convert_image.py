import re
from PIL import Image
from base64 import b64decode, b64encode
from io import BytesIO


def encode_image(path):
    with open(path, "rb") as f:
        binary = b64encode(f)
    return binary

def decode_image(b64):
    return b64decode(b64)

#image_metadata["image_url"] = "https://example.com/path/to/your/image.png"
image_metadata = {
    "file_name": "example.png",
    "file_type": "PNG",
    "file_size": "1024 KB",
}

def image_to_base64(image: Image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='RGB')
    byte_data = output_buffer.getvalue()
    base64_str = b64encode(byte_data)
    return base64_str

def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img
