"""
Agente 3: CV Optimizer con RAG
Lee tu CV, lo vectoriza y lo optimiza según cada trabajo
Usa Groq API (Llama 3.2) - gratuito en cloud
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from typing import Dict, List
import os
from dotenv import load_dotenv
load_dotenv()

class CVOptimizerAgent:
    def __init__(self, cv_path: str = "../../data/mi_cv.pdf"):
        print("📄 Inicializando CV Optimizer con Groq...")
        
        self.cv_path = cv_path
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.cv_text = ""
        
        # Cargar CV
        self._load_cv()
        
        print("✅ CV cargado y listo")
    
    def _load_cv(self):
        """
        Carga el CV desde PDF y extrae el texto
        """
        if not os.path.exists(self.cv_path):
            print(f"⚠️ CV no encontrado en {self.cv_path}, usando CV mock...")
            self.cv_text = self._get_mock_cv()
            return
        
        try:
            loader = PyPDFLoader(self.cv_path)
            documents = loader.load()
            self.cv_text = "\n".join([doc.page_content for doc in documents])
            print(f"   📊 CV cargado: {len(self.cv_text)} caracteres")
        except Exception as e:
            print(f"⚠️ Error cargando CV: {e}, usando mock...")
            self.cv_text = self._get_mock_cv()
    
    def load_cv_from_text(self, text: str):
        """
        Carga el CV desde texto directo (para uploads)
        """
        self.cv_text = text
        print(f"✅ CV cargado desde upload: {len(text)} caracteres")
    
    def _get_mock_cv(self) -> str:
        return """
        ANDRÉS VALLARINO
        Frontend Developer
        
        EXPERIENCIA:
        - OpenDevPro (2024-2026): React, TypeScript, Next.js, Redux, Java, Material UI, CI/CD
        - MeVuelo (2023-2024): React, TypeScript, Material UI, APIs terceros
        - Idea Creativa Marketing (2021-2022): React, HTML5, CSS3, Bootstrap, Figma
        
        SKILLS TÉCNICAS:
        - Frontend: React, TypeScript, Next.js, Vite, TailwindCSS, Redux
        - Backend: Node.js, FastAPI, Python
        - Tools: Git, GitHub Actions, CI/CD, Vercel, Railway
        - IA: Arquitectura multi-agente, LangChain, RAG, Prompt Engineering
        
        PROYECTOS:
        - Job Assistant AI: Sistema multi-agente con RAG, FastAPI, Adzuna API
        - Arcana Mística: Multi-agente con Claude API, Serverless Functions
        
        EDUCACIÓN:
        - Certificación IA Generativas (Desafío Latam 2025)
        - Desarrollo Web Full Stack
        """
    
    def optimize_for_job(self, job_analysis: Dict) -> Dict:
        """
        Optimiza el CV según los requisitos del trabajo usando Groq
        """
        job_title = job_analysis.get('job_title', '')
        required_skills = job_analysis.get('tech_skills', [])
        seniority = job_analysis.get('seniority_level', '')
        
        print(f"\n🔧 Optimizando CV para: {job_title}")
        
        # Truncar CV si es muy largo (Groq tiene límite de tokens)
        cv_context = self.cv_text[:3000] if len(self.cv_text) > 3000 else self.cv_text
        
        prompt = f"""Eres un experto en optimización de CVs para tech jobs.

TRABAJO:
- Puesto: {job_title}
- Seniority: {seniority}
- Skills requeridas: {', '.join(required_skills)}

MI CV:
{cv_context}

TAREA:
1. Identificá qué skills del trabajo YA tengo en mi CV
2. Identificá qué skills me faltan
3. Sugerí cómo destacar mi experiencia relevante
4. Recomendá qué agregar o enfatizar

Respondé en español, formato claro y conciso. Máximo 200 palabras."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )
            recommendations = response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Error Groq: {e}")
            recommendations = f"Revisá tu experiencia con {', '.join(required_skills[:3])} para este rol."
        
        cv_lower = self.cv_text.lower()
        matching = [s for s in required_skills if s.lower() in cv_lower]
        missing = [s for s in required_skills if s.lower() not in cv_lower]
        
        return {
            "job_title": job_title,
            "matching_skills": matching,
            "missing_skills": missing,
            "recommendations": recommendations,
            "relevant_experience": cv_context[:200] + "..."
        }


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST: CV OPTIMIZER CON GROQ")
    print("="*60 + "\n")
    
    optimizer = CVOptimizerAgent()
    
    job_analysis = {
        "job_title": "Frontend Developer React",
        "company": "Tech Startup",
        "tech_skills": ["react", "typescript", "next.js", "redux"],
        "seniority_level": "Semi-Senior"
    }
    
    result = optimizer.optimize_for_job(job_analysis)
    
    print(f"\n📋 Optimización para: {result['job_title']}")
    print(f"\n✅ Skills que YA tenés: {', '.join(result['matching_skills'])}")
    print(f"\n❌ Skills que te faltan: {', '.join(result['missing_skills'])}")
    print(f"\n💡 Recomendaciones:\n{result['recommendations']}")