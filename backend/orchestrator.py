"""
Orquestador con LangGraph - Reemplaza el orchestrator.py anterior
"""

# PARTE 1 - imports
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from agents.scraper_agent import ScraperAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.cv_optimizer_agent import CVOptimizerAgent


# PARTE 2 - state y agentes
class JobAssistantState(TypedDict):
    keywords: str
    location: str
    jobs: List[Dict]
    analyses: List[Dict]
    cv_optimization: Dict
    error: str

scraper = ScraperAgent()
analyzer = AnalyzerAgent()
cv_optimizer = CVOptimizerAgent()


# PARTE 3 - nodos
def nodo_scraper(state: JobAssistantState):
    print("📍 PASO 1: Buscando ofertas...")
    try:
        jobs = scraper.search_jobs(
            state["keywords"],
            state["location"]
        )
        return {"jobs": jobs, "error": ""}
    except Exception as e:
        return {"jobs": [], "error": str(e)}


def nodo_analyzer(state: JobAssistantState):
    print("📊 PASO 2: Analizando ofertas...")
    try:
        analyses = analyzer.analyze_multiple(state["jobs"])
        return {"analyses": analyses, "error": ""}
    except Exception as e:
        return {"analyses": [], "error": str(e)}


def nodo_cv_optimizer(state: JobAssistantState):
    print("🔧 PASO 3: Optimizando CV...")
    try:
        mejor_trabajo = sorted(
            state["analyses"],
            key=lambda x: x["match_score"],
            reverse=True
        )[0]
        cv = cv_optimizer.optimize_for_job(mejor_trabajo)
        return {"cv_optimization": cv, "error": ""}
    except Exception as e:
        return {"cv_optimization": {}, "error": str(e)}


def nodo_error(state: JobAssistantState):
    print(f"❌ Error en el pipeline: {state['error']}")
    return state


# PARTE 4 - edges condicionales
def decidir_tras_scraper(state: JobAssistantState):
    if state["error"] or not state["jobs"]:
        return "error"
    return "analyzer"


def decidir_tras_analyzer(state: JobAssistantState):
    if state["error"] or not state["analyses"]:
        return "error"
    return "cv_optimizer"


# PARTE 5 - grafo
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

# Compilás el grafo
app = grafo.compile()


# PARTE 6 - ejecución
if __name__ == "__main__":
    resultado = app.invoke({
        "keywords": "Frontend Developer",
        "location": "Buenos Aires",
        "jobs": [],
        "analyses": [],
        "cv_optimization": {},
        "error": ""
    })

    if resultado["error"]:
        print(f"\n❌ Pipeline terminó con error: {resultado['error']}")
    else:
        print("\n" + "="*60)
        print("📋 TOP 3 MEJORES MATCHES")
        print("="*60)

        for i, analysis in enumerate(resultado["analyses"][:3], 1):
            print(f"\n🏆 #{i} - {analysis['job_title']}")
            print(f"   🏢 {analysis['company']}")
            print(f"   ⭐ Match: {analysis['match_score']}/100")
            print(f"   💻 Skills: {', '.join(analysis['tech_skills'][:3])}")

        print("\n" + "="*60)
        print("💡 OPTIMIZACIÓN DE CV")
        print("="*60)

        opt = resultado["cv_optimization"]
        print(f"\n🎯 Trabajo: {opt['job_title']}")
        print(f"\n✅ Skills que tenés: {', '.join(opt['matching_skills'])}")
        print(f"\n❌ Skills faltantes: {', '.join(opt['missing_skills']) if opt['missing_skills'] else 'Ninguna'}")
        print(f"\n{opt['recommendations'][:500]}...")