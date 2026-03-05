"""
Agente 3: CV Optimizer con RAG real
Usa FAISS + HuggingFace Embeddings para vectorizar el CV
y buscar chunks relevantes según cada oferta laboral.
Usa Groq API (Llama 3.3) para generar recomendaciones.
"""

from langchain_community.document_loaders import PyPDFLoader #lee el PDF
from langchain_text_splitters import RecursiveCharacterTextSplitter #divide en chunks
from langchain_community.embeddings import FakeEmbeddings #vectoriza gratis
from langchain_community.vectorstores import FAISS #guarda los vectores en memora
from langchain_core.prompts import ChatPromptTemplate #arma el prompt de forma estructurada
from langchain_groq import ChatGroq #conecta con Groq LLM

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
        self.vectorstore = None #FASS con los chunks
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
        else:
            try:
                loader = PyPDFLoader(self.cv_path)
                documents = loader.load()
                self.cv_text = "\n".join([doc.page_content for doc in documents])
                print(f"   📊 CV cargado: {len(self.cv_text)} caracteres")
            except Exception as e:
                print(f"⚠️ Error cargando CV: {e}, usando mock...")
                self.cv_text = self._get_mock_cv()
        splitter = RecursiveCharacterTextSplitter (
        chunk_size=500,
        chunk_overlap=50
         )
        chunks = splitter.create_documents([self.cv_text])

        embeddings = FakeEmbeddings(size=384)

        self.vectorstore = FAISS.from_documents(chunks, embeddings)
        print("✅ RAG inicializado con FAISS")
    
    def load_cv_from_text(self, text: str):
        """
        Carga el CV desde texto directo (para uploads)
        """
        self.cv_text = text
        print(f"✅ CV cargado desde upload: {len(text)} caracteres")
    
    def _get_mock_cv(self) -> str:
        return "CV no disponible. Analizá el trabajo de forma general sin comparar con un CV específico."
    
    def optimize_for_job(self, job_analysis: Dict) -> Dict:
        """
        Optimiza el CV según los requisitos del trabajo usando Groq
        """
        job_title = job_analysis.get('job_title', '')
        required_skills = job_analysis.get('tech_skills', [])
        seniority = job_analysis.get('seniority_level', '')
        
        
       # RAG - busca solo los chunks relevantes del CV para este trabajo
        query = f"{job_title} {' '.join(required_skills)}"
        relevant_chunks = self.vectorstore.similarity_search(query, k=3)  # ← trae los 3 chunks más relevantes
        cv_context = "\n".join([chunk.page_content for chunk in relevant_chunks])
        
        prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en optimización de CVs para tech jobs. Respondé siempre en español, formato claro y conciso. Máximo 200 palabras."),
    ("human", """
TRABAJO:
- Puesto: {job_title}
- Seniority: {seniority}
- Skills requeridas: {required_skills}

MI CV (partes relevantes):
{cv_context}

TAREA:
1. Identificá qué skills del trabajo YA tengo en mi CV
2. Identificá qué skills me faltan
3. Sugerí cómo destacar mi experiencia relevante
4. Recomendá qué agregar o enfatizar
""")
])

        try:
            llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile"
            )
            chain = prompt | llm  # ← conecta prompt con LLM
            response = chain.invoke({
               "job_title": job_title,
               "seniority": seniority,
               "required_skills": ', '.join(required_skills),
               "cv_context": cv_context
            })
            recommendations = response.content 
        except Exception as e:
            print(f"⚠️ Error Groq: {e}")
            recommendations = f"Revisá tu experiencia con {', '.join(required_skills[:3])} para este rol."
        
        
        # Skills del CV para el matching
        SKILLS_CV = "react typescript nextjs next redux nodejs fastapi python git cicd vercel railway tailwind vite"

        matching = [s for s in required_skills if s.lower().replace(".", "").replace("-", "") 
         in SKILLS_CV]
        missing = [s for s in required_skills if s not in matching]
        
        return {
            "job_title": job_title,
            "matching_skills": matching,
            "missing_skills": missing,
            "recommendations": recommendations,
            "relevant_experience": cv_context[:200] + "..."
        }


if __name__ == "__main__":
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