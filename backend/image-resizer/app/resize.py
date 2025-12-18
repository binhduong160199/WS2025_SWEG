from io import BytesIO
from PIL import Image


def make_thumbnail(image_bytes: bytes, max_width: int = 600, quality: int = 70) -> bytes:
    """
    Create a reduced-size JPEG thumbnail while keeping aspect ratio.
    - max_width: target maximum width
    - quality: JPEG quality (smaller -> faster)
    Returns: JPEG bytes
    """
    with Image.open(BytesIO(image_bytes)) as img:
        img = img.convert("RGB")  # ensure JPEG compatible

        w, h = img.size
        if w <= max_width:
            new_w, new_h = w, h
        else:
            ratio = max_width / float(w)
            new_w = max_width
            new_h = int(h * ratio)

        resized = img.resize((new_w, new_h))

        out = BytesIO()
        resized.save(out, format="JPEG", quality=quality, optimize=True)
        return out.getvalue()