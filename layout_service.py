from PIL import Image, ImageDraw, ImageFont
import os

EXPORT_DIR = "static"
os.makedirs(EXPORT_DIR, exist_ok=True)


def _get_font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _measure(draw: ImageDraw.ImageDraw, text: str, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h


def render_text_on_image(image_path: str, copy: str) -> str:
    parts = [p.strip() for p in copy.split(".") if p.strip()]
    top_text = parts[0] if parts else copy.strip()
    bottom_text = parts[1] if len(parts) > 1 else ""

    if image_path.startswith("/"):
        image_path = image_path.lstrip("/")

    img = Image.open(image_path).convert("RGB")
    W, H = img.size

    img_rgba = img.convert("RGBA")
    draw = ImageDraw.Draw(img_rgba)

    # thinner bands and inner margins so controls do not overlap
    band_h = int(0.11 * H)
    padding_x = int(0.06 * W)
    margin_y = int(0.015 * H)  

    def draw_outlined_text(x, y, text, font):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=(255, 255, 255))


    top_overlay = Image.new("RGBA", (W, band_h), (0, 0, 0, 235))
    img_rgba.paste(top_overlay, (0, margin_y), top_overlay)

    font_top = _get_font(int(band_h * 0.33))
    w_top, h_top = _measure(draw, top_text, font_top)
    if w_top + 2 * padding_x > W:
        font_top = _get_font(int(band_h * 0.27))
        w_top, h_top = _measure(draw, top_text, font_top)

    x_top = (W - w_top) // 2
    y_top = margin_y + (band_h - h_top) // 2
    draw_outlined_text(x_top, y_top, top_text, font_top)

   
    if bottom_text:
        bottom_overlay = Image.new("RGBA", (W, band_h), (0, 0, 0, 235))
        bottom_y = H - band_h - margin_y
        img_rgba.paste(bottom_overlay, (0, bottom_y), bottom_overlay)

        font_bottom = _get_font(int(band_h * 0.30))
        w_bot, h_bot = _measure(draw, bottom_text, font_bottom)
        if w_bot + 2 * padding_x > W:
            font_bottom = _get_font(int(band_h * 0.25))
            w_bot, h_bot = _measure(draw, bottom_text, font_bottom)

        x_bot = (W - w_bot) // 2
        y_bot = bottom_y + (band_h - h_bot) // 2
        draw_outlined_text(x_bot, y_bot, bottom_text, font_bottom)

    final = img_rgba.convert("RGB")
    filename = "creative_final.png"
    out_path = os.path.join(EXPORT_DIR, filename)
    final.save(out_path, format="PNG")

    return f"/static/{filename}"
