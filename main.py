from typing import Optional
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.nlp_service import run_nlp_checks
from services.cv_service import run_cv_checks
from services.export_service import export_variants
from services.text_genai_service import enhance_copy
from services.genai_service import generate_creatives
from services.layout_service import render_text_on_image
from services.video_service import create_video_from_image

app = FastAPI(title="RCCAP Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/build_creative")
async def build_creative(
    ad_copy: str = Form(...),
    brief: str = Form(...),
    image: UploadFile = File(...),
):
    """
    One‑shot pipeline:
    - Enhance copy (GenAI text module)
    - Generate a styled variant (GenAI image module)
    - Render chosen copy onto the variant (layout engine)
    Returns final creative URL + copy used + alternatives.
    """
    enhanced = enhance_copy(ad_copy, brief)
    options = enhanced.get("options", [ad_copy])

    if len(options) >= 3:
        chosen_copy = options[2]
    elif len(options) >= 1:
        chosen_copy = options[0]
    else:
        chosen_copy = ad_copy

    gen = await generate_creatives(image, brief, num_images=1)
    variant_url = gen["variants"][0]        
    variant_path = variant_url.lstrip("/")  

    final_url = render_text_on_image(variant_path, chosen_copy)

    return {
        "image_url": final_url,
        "copy_used": chosen_copy,
        "alternatives": options,
    }

@app.post("/api/make_video")
async def make_video():
    """
    Takes the latest generated creative_final.png and turns it into
    a short MP4 teaser with background music.
    """
    image_path = "static/creative_final.png"
    if not os.path.exists(image_path):
        return {"error": "No creative_final.png found. Generate a creative first."}

    video_url = create_video_from_image(image_path)
    return {"video_url": video_url}

@app.post("/api/enhance_copy")
async def api_enhance_copy(
    ad_copy: str = Form(...),
    brief: str = Form(""),
):
    result = enhance_copy(ad_copy, brief)
    return result

@app.post("/api/generate_creative")
async def api_generate_creative(
    brief: str = Form(...),
    image: UploadFile = File(...),
    n: int = Form(2),
):
    result = await generate_creatives(image, brief, num_images=n)
    return result
@app.post("/api/validate")
async def validate_creative(
    ad_copy: str = Form(...),
    image: UploadFile = File(...),
):
    nlp_result = run_nlp_checks(ad_copy)
    cv_result = await run_cv_checks(image)
    return {"nlp": nlp_result, "cv": cv_result}
@app.post("/api/export")
async def export_creative(image: UploadFile = File(...)):
    links = await export_variants(image)
    return {"links": links}
