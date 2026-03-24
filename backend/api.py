"""
API REST con FastAPI para conectar frontend con backend
"""

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from langsmith import traceable
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from backend.orchestrator import app as langgraph_app, cv_optimizer
import shutil
import os

load_dotenv()

app = FastAPI(title="Job Assistant AI API")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://job-assistant-ai-6g1q.onrender.com",
        "https://job-assistant-ai-tzle.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🤖 Inicializando sistema multi-agente con LangGraph...")
print("✅ Sistema listo")

# Modelos de datos
class SearchRequest(BaseModel):
    keywords: str
    location: str = "Brasil"

@app.get("/")
def root():
    return {
        "message": "Job Assistant AI API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.options("/api/search")
async def options_search(request: Request):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "https://job-assistant-ai-tzle.vercel.app",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@app.post("/api/search")
@traceable(
    name="API - Search Jobs Request",
    tags=["api", "production"],
    metadata={"endpoint": "/api/search"}
)
def search_jobs(request: SearchRequest,  req: Request):
    """
    Endpoint principal: busca trabajos y optimiza CV
    """
    try:
        keywords = request.keywords.strip()
        location = request.location.strip() or "Brasil"

        if not keywords:
            return {
                "success": False,
                "error": "Debes ingresar al menos una palabra clave para buscar empleos."
            }

        thread_id = req.client.host

        results = langgraph_app.invoke(
            {
            "keywords": keywords,
            "location": location,
            "jobs": [],
            "analyses": [],
            "cv_optimization": {},
            "error": "",
            "intentos": 0,
        },
        config={
            "configurable": {"thread_id": thread_id},
             "run_name": f"search-{keywords}-{location}",
                "tags": ["api", location.lower()],
                "metadata": {
                    "keywords": keywords,
                    "location": location,
                    "user_ip": thread_id
                }
            }
        )

        if results.get("error"):
            return {
                "success": False,
                "error": results["error"]
            }

        analyses = results.get("analyses", [])

        return {
            "success": True,
            "analyses": analyses,
            "best_match": analyses[0] if analyses else {},
            "cv_optimization": results.get("cv_optimization", {}),
            "total_found": len(analyses)
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Sube y procesa un CV en PDF
    """
    try:
        filename = file.filename or ""
        if not filename.lower().endswith('.pdf'):
            return {"success": False, "error": "Solo se aceptan archivos PDF"}

        cv_path = "/tmp/mi_cv.pdf"

        with open(cv_path, "wb") as buffer:
          shutil.copyfileobj(file.file, buffer)

        # convertir a texto
        reader = PdfReader(cv_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        text = text.strip()
        if not text:
            text = (
                "CV subido sin texto extraíble. "
                "Es posible que el PDF sea una imagen escaneada."
            )

        if cv_optimizer is None:
            return {
                "success": False,
                "error": "El optimizador de CV no está inicializado en el backend."
            }

        cv_optimizer.load_cv_from_text(text)

        return {
            "success": True,
            "message": "CV cargado exitosamente"
        }

    except Exception as e:
        print(f"❌ Error subiendo CV: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
