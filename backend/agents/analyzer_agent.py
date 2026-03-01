"""
Agente 2: Analyzer - Analiza ofertas laborales con LLM real
Usa Groq (Llama 3.3) via LangChain con tools para extraer
skills, seniority y calcular match score
"""

import os
import json
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


# ─── Tools del agente ────────────────────────────────────────────────────────

@tool
def extract_tech_skills(job_description: str) -> str:
    """Extrae las tecnologías y skills técnicas mencionadas en una descripción de trabajo."""
    tech_keywords = [
        "react", "typescript", "javascript", "python", "node.js", "next.js",
        "vue", "angular", "sql", "mongodb", "postgresql", "aws", "docker",
        "kubernetes", "git", "ci/cd", "fastapi", "django", "flask", "tailwind",
        "redux", "graphql", "java", "kotlin", "swift", "go", "rust", "php",
        "laravel", "spring", "nestjs", "express", "prisma", "supabase", "firebase",
        "vercel", "railway", "heroku", "azure", "gcp", "terraform", "ansible"
    ]
    found = [skill for skill in tech_keywords if skill.lower() in job_description.lower()]
    return json.dumps(found)


@tool
def detect_seniority_level(job_title: str, job_description: str) -> str:
    """Detecta el nivel de seniority requerido para una posición."""
    title_lower = job_title.lower()
    desc_lower = job_description.lower()

    if any(w in title_lower for w in ['senior', 'sr.', ' sr ']):
        return "Senior"
    elif any(w in title_lower for w in ['junior', 'jr.', ' jr ']):
        return "Junior"
    elif any(w in title_lower for w in ['semi', 'ssr', 'pleno', 'mid']):
        return "Semi-Senior"
    elif any(w in title_lower for w in ['lead', 'principal', 'staff']):
        return "Lead/Principal"
    elif any(w in desc_lower for w in ['5+ years', '6+ years', '5+ años', '6+ años']):
        return "Senior"
    elif any(w in desc_lower for w in ['3+ years', '4+ years', '3+ años', '4+ años']):
        return "Semi-Senior"
    else:
        return "Semi-Senior"


@tool
def calculate_match_score(tech_skills_json: str, seniority: str) -> str:
    """Calcula un score de match del 0 al 100 basado en las skills encontradas y el seniority."""
    try:
        skills = json.loads(tech_skills_json)
    except Exception:
        skills = []

    base_score = min(len(skills) * 12, 70)

    seniority_bonus = {
        "Junior": 15,
        "Semi-Senior": 20,
        "Senior": 10,
        "Lead/Principal": 5
    }
    bonus = seniority_bonus.get(seniority, 10)
    score = min(base_score + bonus, 100)
    return str(score)


# ─── Agente ──────────────────────────────────────────────────────────────────

class AnalyzerAgent:
    def __init__(self):
        print("🧠 Inicializando Analyzer Agent con Groq LLM...")

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",
            temperature=0
        )

        self.tools = [extract_tech_skills, detect_seniority_level, calculate_match_score]

        system_prompt = """Eres un agente experto en análisis de ofertas laborales tech.
Usá las tools disponibles para analizar la oferta y luego respondé ÚNICAMENTE con un JSON válido, sin texto adicional, sin explicaciones, solo el JSON:
{
  "tech_skills": ["skill1", "skill2"],
  "seniority_level": "Junior|Semi-Senior|Senior|Lead/Principal",
  "match_score": 75,
  "experience_required": "3+ años"
}"""

        self.agent = create_react_agent(self.llm, self.tools, prompt=system_prompt)

        print("✅ Analyzer Agent listo")

    def analyze_job(self, job: Dict) -> Dict:
        """
        Analiza una oferta laboral usando el agente LLM con tools
        """
        title = job.get('title', '')
        description = job.get('description', '')
        requirements = job.get('requirements', [])

        input_text = f"""
Título: {title}
Descripción: {description}
Requisitos: {', '.join(requirements) if requirements else 'No especificados'}
"""

        try:
            result = self.agent.invoke({"messages": [("human", input_text)]})
            output = result["messages"][-1].content
            
            analysis_data = json.loads(output)

            # Limpiar posibles backticks de markdown
            output = output.strip().replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(output)
        

            return {
                "job_title": title,
                "company": job.get('company', ''),
                "tech_skills": analysis_data.get("tech_skills", []),
                "soft_skills": [],
                "experience_required": analysis_data.get("experience_required", "No especificado"),
                "seniority_level": analysis_data.get("seniority_level", "Semi-Senior"),
                "match_score": int(analysis_data.get("match_score", 0)),
                "link": job.get('link', ''),
                "description": description
            }

        except Exception as e:
            print(f"⚠️ Error COMPLETO: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_analyze(job)

    def _fallback_analyze(self, job: Dict) -> Dict:
        """Fallback simple si el LLM falla"""
        description = job.get('description', '').lower()
        tech_keywords = ["react", "typescript", "javascript", "python", "node.js", "next.js", "vue", "angular"]
        found_skills = [s for s in tech_keywords if s in description]

        return {
            "job_title": job.get('title', ''),
            "company": job.get('company', ''),
            "tech_skills": found_skills,
            "soft_skills": [],
            "experience_required": "No especificado",
            "seniority_level": "Semi-Senior",
            "match_score": len(found_skills) * 10,
            "link": job.get('link', ''),
            "description": job.get('description', '')
        }

    def analyze_multiple(self, jobs: List[Dict]) -> List[Dict]:
        """Analiza múltiples ofertas"""
        analyses = []
        for job in jobs:
            print(f"   🔍 Analizando: {job.get('title', 'Sin título')}")
            analysis = self.analyze_job(job)
            analyses.append(analysis)
        return analyses


# ─── Test ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from scraper_agent import ScraperAgent

    scraper = ScraperAgent()
    jobs = scraper.search_jobs("Frontend Developer")

    analyzer = AnalyzerAgent()
    analyses = analyzer.analyze_multiple(jobs[:3])  # Solo 3 para el test

    print("\n" + "="*60)
    print("ANÁLISIS CON LLM REAL")
    print("="*60)

    for analysis in analyses:
        print(f"\n📋 {analysis['job_title']} - {analysis['company']}")
        print(f"   🎯 Nivel: {analysis['seniority_level']}")
        print(f"   ⏱  Experiencia: {analysis['experience_required']}")
        print(f"   💻 Skills: {', '.join(analysis['tech_skills'])}")
        print(f"   ⭐ Match Score: {analysis['match_score']}/100")