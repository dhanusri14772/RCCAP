from PIL import Image
from tempfile import NamedTemporaryFile
import os

SIZES = {
    "facebook": (1080, 1920),
    "instagram": (1080, 1350),  
}

EXPORT_DIR = "static"
os.makedirs(EXPORT_DIR, exist_ok=True)

async def export_variants(upload_file) -> dict:
    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        content = await upload_file.read()
        tmp.write(content)
        src_path = tmp.name

    img = Image.open(src_path).convert("RGB")

    links: dict[str, str] = {}
    base_name = os.path.basename(src_path)

    for name, size in SIZES.items():
        resized = img.resize(size, Image.LANCZOS)
        out_name = f"{name}_{base_name}"
        out_path = os.path.join(EXPORT_DIR, out_name)
        resized.save(out_path, format="PNG")
        links[name] = f"/static/{out_name}"

    return links
