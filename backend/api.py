"""
API REST con FastAPI para conectar frontend con backend
"""

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from orchestrator import JobAssistantOrchestrator
from agents.cv_optimizer_agent import CVOptimizerAgent
from typing import Optional
import shutil
import os

app = FastAPI(title="Job Assistant AI API")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173",
    "https://job-assistant-ai-tzle.vercel.app"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar orquestador (tarda un poco por Ollama)
print("🤖 Inicializando sistema multi-agente...")
orchestrator = JobAssistantOrchestrator()
print("✅ Sistema listo")

# Modelos de datos
class SearchRequest(BaseModel):
    keywords: str
    location: str = "Buenos Aires"

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
def search_jobs(request: SearchRequest):
    """
    Endpoint principal: busca trabajos y optimiza CV
    """
    try:
        results = orchestrator.full_pipeline(
            keywords=request.keywords,
            location=request.location
        )
        return {
            "success": True,
            "analyses": results.get("analyses", []),
            "best_match": results.get("analyses", [{}])[0] if results.get("analyses") else {},
            "cv_optimization": results.get("cv_optimization", {}),
            "total_found": results.get("total_found", 0)
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
        # Validar que sea PDF
        if not file.filename.endswith('.pdf'):
            return {"success": False, "error": "Solo se aceptan archivos PDF"}
        
        # Guardar el archivo
        cv_path = "../data/mi_cv.pdf"
        os.makedirs("../data", exist_ok=True)
        
        with open(cv_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Recargar el CV Optimizer con el nuevo CV
        global orchestrator
        orchestrator.cv_optimizer = CVOptimizerAgent(cv_path=cv_path)
        
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
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
