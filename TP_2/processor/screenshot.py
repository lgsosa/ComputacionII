import base64
import io
from PIL import Image, ImageDraw

def generate_screenshot_placeholder(url):
    img = Image.new("RGB", (800, 450), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), f"Screenshot\n{url}", fill=(255, 255, 255))
    buff = io.BytesIO()
    img.save(buff, "PNG")
    return base64.b64encode(buff.getvalue()).decode("ascii")
