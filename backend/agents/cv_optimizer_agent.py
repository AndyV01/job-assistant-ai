"""
Agente 3: CV Optimizer con RAG
Lee tu CV, lo vectoriza y lo optimiza según cada trabajo
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Dict, List
import os

class CVOptimizerAgent:
    def __init__(self, cv_path: str = "../../data/mi_cv.pdf"):
        print("📄 Inicializando CV Optimizer con RAG...")
        
        self.cv_path = cv_path
        self.llm = Ollama(model="llama3.2")
        self.embeddings = OllamaEmbeddings(model="llama3.2")
        self.vectorstore = None
        
        # Cargar y vectorizar el CV
        self._load_cv()
        
        print("✅ CV cargado y vectorizado")
    
    def _load_cv(self):
        """
        Carga el CV desde PDF y lo convierte en vectores
        """
        # Verificar que el archivo existe
        if not os.path.exists(self.cv_path):
            print(f"⚠️ CV no encontrado en {self.cv_path}")
            print("📝 Usando CV de ejemplo...")
            # Crear CV mock para testing
            self._create_mock_cv()
            return
        
        # Cargar PDF
        loader = PyPDFLoader(self.cv_path)
        documents = loader.load()
        
        # Dividir en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(documents)
        
        # Crear vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="../../data/vectorstore"
        )
        
        print(f"   📊 CV dividido en {len(chunks)} chunks")
    
    def _create_mock_cv(self):
        """
        Crea un CV mock para testing si no existe el PDF
        """
        from langchain_core.documents import Document
        
        mock_cv_text = """
        ANDRÉS VALLARINO
        Frontend / Full-Stack Developer
        
        EXPERIENCIA:
        - FlexiPaaS (2023-2024): Desarrollo frontend con React, TypeScript, Next.js
        - Trabajé en módulo Flowchart con drag & drop
        - Integración con APIs REST y Spring Boot
        
        SKILLS TÉCNICAS:
        - Frontend: React, TypeScript, Next.js, Vite, TailwindCSS
        - Backend: Node.js, FastAPI, Python
        - Tools: Git, GitHub Actions, CI/CD, Vercel, Netlify
        - IA: Arquitectura multi-agente, LangChain, RAG, Prompt Engineering
        
        PROYECTOS:
        - Arcana Mística: Sistema multi-agente con Claude API
        - Job Assistant: RAG con Llama local
        - E-commerce: React con CI/CD
        
        EDUCACIÓN:
        - Certificación IA Generativa (Desafío Latam 2024)
        - Desarrollo Web Full Stack
        """
        
        doc = Document(page_content=mock_cv_text)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents([doc])
        
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="../../data/vectorstore"
        )
    
    def optimize_for_job(self, job_analysis: Dict) -> Dict:
        """
        Optimiza tu CV según los requisitos del trabajo usando RAG
        
        Args:
            job_analysis: Análisis del trabajo (del Analyzer Agent)
            
        Returns:
            CV optimizado con recomendaciones
        """
        job_title = job_analysis['job_title']
        required_skills = job_analysis['tech_skills']
        
        print(f"\n🔧 Optimizando CV para: {job_title}")
        
        # Buscar en el vectorstore las partes relevantes del CV
        query = f"Experiencia y skills relacionados con: {', '.join(required_skills)}"
        relevant_docs = self.vectorstore.similarity_search(query, k=3)
        
        # Construir contexto
        cv_context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # Generar recomendaciones con LLM
        prompt = f"""
Eres un experto en optimización de CVs para tech jobs.

TRABAJO:
- Puesto: {job_title}
- Skills requeridas: {', '.join(required_skills)}

MI CV (extracto relevante):
{cv_context}

TAREA:
1. Identifica qué skills del trabajo YA tengo en mi CV
2. Identifica qué skills me faltan
3. Sugiere cómo destacar mi experiencia relevante
4. Recomienda qué agregar/enfatizar en el CV

Responde en español, formato claro y conciso.
"""
        
        response = self.llm.invoke(prompt)
        
        optimization = {
            "job_title": job_title,
            "matching_skills": [s for s in required_skills if any(s in cv_context.lower() for s in required_skills)],
            "missing_skills": [s for s in required_skills if s not in cv_context.lower()],
            "recommendations": response,
            "relevant_experience": cv_context[:200] + "..."
        }
        
        return optimization

# Test del agente
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST: CV OPTIMIZER CON RAG")
    print("="*60 + "\n")
    
    # Crear agente
    optimizer = CVOptimizerAgent()
    
    # Job mock para probar
    job_analysis = {
        "job_title": "Frontend Developer React",
        "company": "Tech Startup",
        "tech_skills": ["react", "typescript", "next.js"],
        "seniority_level": "Semi-Senior"
    }
    
    # Optimizar CV
    result = optimizer.optimize_for_job(job_analysis)
    
    # Mostrar resultados
    print(f"\n📋 Optimización para: {result['job_title']}")
    print(f"\n✅ Skills que YA tenés: {', '.join(result['matching_skills'])}")
    print(f"\n❌ Skills que te faltan: {', '.join(result['missing_skills'])}")
    print(f"\n💡 Recomendaciones:\n{result['recommendations']}")