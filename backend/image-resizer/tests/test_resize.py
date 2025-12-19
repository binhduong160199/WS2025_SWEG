import importlib.util
import os
from io import BytesIO
from PIL import Image

# --------------------------------------------------
# Load resize.py by file path (NO package import)
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "app")
)
RESIZE_PATH = os.path.join(BASE_DIR, "resize.py")

spec = importlib.util.spec_from_file_location("resize", RESIZE_PATH)
resize = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resize)

make_thumbnail = resize.make_thumbnail


def _make_test_png(width=1200, height=800) -> bytes:
    img = Image.new("RGB", (width, height))
    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def test_make_thumbnail_resizes_to_max_width():
    src = _make_test_png(1200, 800)
    thumb = make_thumbnail(src, max_width=600, quality=70)

    img = Image.open(BytesIO(thumb))
    w, h = img.size

    assert w == 600
    assert h == 400  # keeps aspect ratio


def test_make_thumbnail_keeps_small_images_same_width():
    src = _make_test_png(400, 300)
    thumb = make_thumbnail(src, max_width=600, quality=70)

    img = Image.open(BytesIO(thumb))
    w, h = img.size

    assert w == 400
    assert h == 300