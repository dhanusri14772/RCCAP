# RCCAP
RCCAP - Retail Media Creative Compliance Automation Platform
RCCAP Hackathon Demo: AI-powered visual creative builder that enables advertisers to autonomously design, validate, and export professional, guideline-compliant retail media creatives in minutes - eliminating manual processes and expensive agency reliance.

🎯 Problem & Solution
The Challenge: Retail advertisers spend hours (and $$$) on agencies for compliant social creatives from plain packshots.
RCCAP Solution: One-click pipeline → GenAI copy → GenAI styling → Auto-compliant layout → Social-ready video. Demo ready.

🏗️ Architecture
<img width="1598" height="564" alt="image" src="https://github.com/user-attachments/assets/e83d01b8-3800-435c-9797-b05e98dce418" />

🚀 Quick Start 
Backend (FastAPI)
bash
cd BACKEND
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # once only
uvicorn main:app --reload
Live at: http://127.0.0.1:8000

Frontend (React)
bash
cd frontend
npm install
npm start
Live at: http://localhost:3000

🎮 Live Demo Flow
text
1. Promo: "Save 80% on juices!"
2. Brief: "Tesco bold savings banner + fresh citrus"
3. Upload: Juice bottle packshot
4. "Generate Creative" → ✅ Compliant PNG
5. "Generate Video" → ✅ 6s social MP4
Output: Tesco-ready creative + video in <30s.

🔌 API Endpoints
Endpoint	What it does
POST /api/build_creative	Full pipeline: Copy + Image + Layout
POST /api/make_video	PNG → MP4 video export
POST /api/enhance_copy	GenAI copy variants
POST /api/generate_creative	Image styling variants
POST /api/validate	NLP+CV compliance

📁 Modular Services (BACKEND/services/)
text
nlp_service.py          # spaCy text validation
text_genai_service.py   # OpenAI copy enhancement
genai_service.py        # Product image styling
layout_service.py       # Tesco-compliant text bands
video_service.py        # MoviePy MP4 generation

🏆 Key Features
✅ Zero manual design: AI handles copy, styling, layout
✅ Tesco compliance: Automated text bands + validation
✅ Social-ready: 6s MP4 videos with music
✅ Production scale: FastAPI + static asset serving

📊 Tech Stack
FastAPI | React | OpenAI | spaCy | OpenCV | MoviePy | Pillow

💻Developer
Dhanusri.T - Full-stack AI/ML engineer
Final-year AI & Data Science | Python | GenAI | Full-stack

📄 License
MIT License

