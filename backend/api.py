"""
API REST con FastAPI para conectar frontend con backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import JobAssistantOrchestrator
from typing import Optional

app = FastAPI(title="Job Assistant AI API")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vite
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

@app.post("/api/search")
def search_jobs(request: SearchRequest):
    """
    Endpoint principal: busca trabajos y optimiza CV
    """
    try:
        # Ejecutar pipeline completo
        results = orchestrator.full_pipeline(
            keywords=request.keywords,
            location=request.location
        )
        
        # Formatear respuesta para el frontend
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)