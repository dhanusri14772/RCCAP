import cv2
import numpy as np
from tempfile import NamedTemporaryFile

SAFE_TOP = 200
SAFE_BOTTOM = 250

async def run_cv_checks(upload_file) -> dict:
    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        content = await upload_file.read()
        tmp.write(content)
        path = tmp.name

    img = cv2.imread(path)
    if img is None:
        return {
            "passed": False,
            "issues": ["Invalid or unreadable image"],
            "height": 0,
            "width": 0,
        }

    h, w, _ = img.shape
    issues: list[str] = []

    top_band = img[0:SAFE_TOP, :, :]
    bottom_band = img[h - SAFE_BOTTOM : h, :, :]

    if np.mean(top_band) < 250:
        issues.append("Content present in top safe zone")

    if np.mean(bottom_band) < 250:
        issues.append("Content present in bottom safe zone")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "height": int(h),
        "width": int(w),
    }
