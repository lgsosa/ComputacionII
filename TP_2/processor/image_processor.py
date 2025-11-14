import base64
import io
from PIL import Image

def generate_thumbnails_from_bytes(images, size=(120,120)):
    thumbs = []
    for raw in images:
        try:
            img = Image.open(io.BytesIO(raw))
            img.thumbnail(size)
            buff = io.BytesIO()
            img.save(buff, "PNG")
            thumbs.append(base64.b64encode(buff.getvalue()).decode("ascii"))
        except:
            continue
    return thumbs
