import os
from tempfile import NamedTemporaryFile
from typing import List

import cv2
import numpy as np
from PIL import Image

EXPORT_DIR = "static"
os.makedirs(EXPORT_DIR, exist_ok=True)


def _save_image(img: np.ndarray, prefix: str) -> str:
    with NamedTemporaryFile(delete=False, suffix=".png", dir=EXPORT_DIR) as tmp:
        Image.fromarray(img).save(tmp.name, format="PNG")
        filename = os.path.basename(tmp.name)
    return f"/static/{filename}"


async def generate_creatives(upload_file, brief: str, num_images: int = 2) -> dict:
    """
    Local 'GenAI-style' creative generator.
    Takes the uploaded image and produces a few stylized ad variants:
    - gradient band for copy
    - slight color shift / blur

    Returns: { "variants": ["/static/..png", ...] }
    """
    content = await upload_file.read()
    np_arr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("Invalid image")

    h, w, _ = img.shape
    variants: List[str] = []

    # 1) Original with top gradient band
    band_height = int(0.2 * h)
    grad = np.linspace(0, 180, band_height).astype(np.uint8)
    grad = np.tile(grad[:, None], (1, w))
    grad = cv2.merge([grad, grad, grad])
    img1 = img.copy()
    img1[0:band_height, :, :] = cv2.addWeighted(
        img1[0:band_height, :, :], 0.4, grad, 0.6, 0
    )
    variants.append(_save_image(img1[..., ::-1], "var1"))  # BGR->RGB

    # 2) Bottom value tile + light blur
    img2 = cv2.GaussianBlur(img, (9, 9), 0)
    tile_h = int(0.25 * h)
    y0 = h - tile_h
    overlay = img2.copy()
    cv2.rectangle(overlay, (0, y0), (w, h), (20, 20, 20), -1)
    img2 = cv2.addWeighted(overlay, 0.5, img2, 0.5, 0)
    variants.append(_save_image(img2[..., ::-1], "var2"))

    # 3) Slight color shift
    img3 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img3[..., 0] = (img3[..., 0] + 10) % 180
    img3 = cv2.cvtColor(img3, cv2.COLOR_HSV2BGR)
    variants.append(_save_image(img3[..., ::-1], "var3"))

    return {"variants": variants[:num_images]}
