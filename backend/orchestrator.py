"""
Orquestador con LangGraph 
"""

from langgraph.graph import StateGraph, END 
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List, Dict
from backend.agents.scraper_agent import ScraperAgent
from backend.agents.analyzer_agent import AnalyzerAgent
from backend.agents.cv_optimizer_agent import CVOptimizerAgent
# metricas y debuggear agentes
from langsmith import traceable
import os
from dotenv import load_dotenv

load_dotenv()

# state y agentes
class JobAssistantState(TypedDict):
    keywords: str
    location: str
    jobs: List[Dict]
    analyses: List[Dict]
    cv_optimization: Dict
    error: str
    intentos: int
    cv_text: str

scraper = ScraperAgent()
analyzer = AnalyzerAgent()
cv_optimizer = CVOptimizerAgent()


# nodos
@traceable(name="Scraper - Buscar ofertas")
def nodo_scraper(state: JobAssistantState):
    print("PASO 1: Buscando ofertas...")
    try:
        jobs = scraper.search_jobs(
            state["keywords"],
            state["location"]
        )
        return {"jobs": jobs, "error": "", "intentos": state["intentos"] + 1}
    except Exception as e:
        from langsmith import get_current_run_tree
        run = get_current_run_tree()
        if run:
            run.add_metadata({
                "error_type": type(e).__name__,
                "error_message": str(e),
                "keywords": state["keywords"],
                "location": state["location"]
            })
            run.add_tags(["scraper-error"])
        return {"jobs": [], "error": str(e), "intentos": state["intentos"] + 1}


@traceable(name="Analyzer - Analizar ofertas")
def nodo_analyzer(state: JobAssistantState):
    print("PASO 2: Analizando ofertas...")
    try:
        analyses = analyzer.analyze_multiple(state["jobs"])
        return {"analyses": analyses, "error": ""}
    except Exception as e:
        from langsmith import get_current_run_tree
        run = get_current_run_tree()
        if run:
            run.add_metadata({
                "error_type": type(e).__name__,
                "error_message": str(e),
                "jobs_recibidos": len(state.get("jobs", []))
            })
            run.add_tags(["analyzer-error"])
        return {"analyses": [], "error": str(e)}


@traceable(name="Analyzer - Analizar ofertas")
def nodo_cv_optimizer(state: JobAssistantState):
    print("PASO 3: Optimizando CV...")
    try:
        mejor_trabajo = sorted(
            state["analyses"],
            key=lambda x: x["match_score"],
            reverse=True
        )[0]
        cv = cv_optimizer.optimize_for_job(
            mejor_trabajo,
            state.get("cv_text", "")
        )    
        return {"cv_optimization": cv, "error": ""}
    except Exception as e:
        from langsmith import get_current_run_tree
        run = get_current_run_tree()
        if run:
            run.add_metadata({
                "error_type": type(e).__name__,
                "error_message": str(e),
                "analyses_disponibles": len(state.get("analyses", []))
            })
            run.add_tags(["cv-optimizer-error"])
        return {"cv_optimization": {}, "error": str(e)}


@traceable(
    name="Error Handler - Pipeline Failed",
    tags=["error"]
)
def nodo_error(state: JobAssistantState):
    from langsmith import get_current_run_tree
    
    error_msg = state.get("error", "Error desconocido")
    intentos = state.get("intentos", 0)
    jobs_encontrados = len(state.get("jobs", []))
    analyses_generados = len(state.get("analyses", []))
    
    print(f"❌ Error en el pipeline: {error_msg}")
    
    # Contexto completo del error para LangSmith
    run = get_current_run_tree()
    if run:
        run.add_metadata({
            "error_message": error_msg,
            "intentos_realizados": intentos,
            "jobs_encontrados": jobs_encontrados,
            "analyses_generados": analyses_generados,
            "keywords": state.get("keywords", ""),
            "location": state.get("location", ""),
            "fallo_en": "scraper" if not jobs_encontrados else "analyzer" if not analyses_generados else "cv_optimizer"
        })
        run.add_tags(["pipeline-error", f"intentos-{intentos}"])
    
    return state


# edges condicionales
def decidir_tras_scraper(state: JobAssistantState):
    if state["error"] or not state["jobs"]:
        return "error"
    return "analyzer"


def decidir_tras_analyzer(state: JobAssistantState):
    if state["error"] or not state["analyses"]:
        return "error"
    promedio = sum(a["match_score"] for a in state["analyses"]) / len(state["analyses"])
    
    # Máximo 3 intentos para evitar loop infinito
    if promedio < 20 and state["intentos"] < 3:
        return "scraper"  
    
    return "cv_optimizer"


# grafo
grafo = StateGraph(JobAssistantState)

# Agregás los nodos
grafo.add_node("scraper", nodo_scraper)
grafo.add_node("analyzer", nodo_analyzer)
grafo.add_node("cv_optimizer", nodo_cv_optimizer)
grafo.add_node("error", nodo_error)

# Por dónde empieza
grafo.set_entry_point("scraper")

# Conectás los nodos con edges condicionales
grafo.add_conditional_edges("scraper", decidir_tras_scraper)
grafo.add_conditional_edges("analyzer", decidir_tras_analyzer)

# Edges fijos
grafo.add_edge("cv_optimizer", END)
grafo.add_edge("error", END)
 
# memoria persistente 
checkpointer = checkpointer = MemorySaver()
# Compilás el grafo
app = grafo.compile(checkpointer=checkpointer)


# ejecución
if __name__ == "__main__":
    resultado = app.invoke(
        {
        "keywords": "Frontend Developer",
        "location": "Buenos Aires",
        "jobs": [],
        "analyses": [],
        "cv_optimization": {},
        "error": "",
        "intentos": 0
    },
    config={
        "configurable": {"thread_id": "test_local"},
        "run_name": "test-local-run",
        "tags": ["local", "test"]
    }
    )

    if resultado["error"]:
        print(f"Pipeline terminó con error: {resultado['error']}")
    else:
        print("\n" + "="*60)
        print("📋 TOP 3 MEJORES MATCHES")
        print("="*60)

        for i, analysis in enumerate(resultado["analyses"][:3], 1):
            print(f"\n🏆 #{i} - {analysis['job_title']}")
            print(f"   🏢 {analysis['company']}")
            print(f"   ⭐ Match: {analysis['match_score']}/100")
            print(f"   💻 Skills: {', '.join(analysis['tech_skills'][:3])}")

        opt = resultado["cv_optimization"]
        