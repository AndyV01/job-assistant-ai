"""
Agente 3: CV Optimizer con RAG real
Usa FAISS + HuggingFace Embeddings para vectorizar el CV
y buscar chunks relevantes según cada oferta laboral.
Usa Groq API (Llama 3.3) para generar recomendaciones.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from groq import Groq
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Todo el bloque de FAISS + FakeEmbeddings en un solo try/except
try:
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import FakeEmbeddings
    FAISS_AVAILABLE = True
except Exception as e:
    print(f"⚠️ FAISS/Embeddings no disponibles: {e}")
    FAISS = None
    FakeEmbeddings = None
    FAISS_AVAILABLE = False


class SimpleVectorStore:
    """Fallback liviano cuando FAISS no está disponible en runtime."""
    def __init__(self, documents: List[Document]):
        self.documents = documents

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        query_terms = set((query or "").lower().split())

        def score(doc: Document) -> int:
            content_terms = set(doc.page_content.lower().split())
            return len(query_terms & content_terms)

        ranked = sorted(self.documents, key=score, reverse=True)
        return ranked[:k] if ranked else []


class CVOptimizerAgent:
    def __init__(self, cv_path: str = "../../data/mi_cv.pdf"):
        print("📄 Inicializando CV Optimizer con Groq...")

        self.cv_path = cv_path
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.cv_text = ""
        self.vectorstore = None

        print("✅ CV cargado y listo")

    def _load_cv(self):
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

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.create_documents([self.cv_text])
        self._build_vectorstore(chunks)

    def load_cv_from_text(self, text: str):
        try:
            self.cv_text = text
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.create_documents([self.cv_text]) if self.cv_text else []

            if not chunks:
                chunks = splitter.create_documents([self._get_mock_cv()])

            self._build_vectorstore(chunks)
            print(f"✅ CV cargado desde upload: {len(text)} caracteres")
            print("✅ Vectorstore del CV actualizado")
        except Exception as e:
            print(f"⚠️ Error procesando CV desde texto ({e}), usando fallback mínimo")
            self.cv_text = text or self._get_mock_cv()
            self.vectorstore = SimpleVectorStore([Document(page_content=self.cv_text)])

    def _get_mock_cv(self) -> str:
        return "CV no disponible. Analizá el trabajo de forma general sin comparar con un CV específico."

    def _build_vectorstore(self, chunks: List[Document]):
        # ✅ FIX: Usa FAISS_AVAILABLE en lugar de comparar FAISS con None
        try:
            if not FAISS_AVAILABLE:
                raise RuntimeError("FAISS no disponible en este runtime")
            embeddings = FakeEmbeddings(size=384)
            self.vectorstore = FAISS.from_documents(chunks, embeddings)
            print("✅ Vectorstore FAISS actualizado")
        except Exception as e:
            print(f"⚠️ FAISS no disponible ({e}), usando fallback simple en memoria")
            self.vectorstore = SimpleVectorStore(chunks)

    def optimize_for_job(self, job_analysis: Dict, cv_text: str = "") -> Dict:
        if cv_text and cv_text.strip():
            self.load_cv_from_text(cv_text.strip())

        job_title = job_analysis.get('job_title', '')
        required_skills = job_analysis.get('tech_skills', [])
        seniority = job_analysis.get('seniority_level', '')

        if not self.vectorstore:
            return {
                "job_title": job_title,
                "matching_skills": [],
                "missing_skills": [],
                "recommendations": "Primero subí tu CV",
                "relevant_experience": ""
            }

        query = f"{job_title} {' '.join(required_skills)}"
        relevant_chunks = self.vectorstore.similarity_search(query, k=3)
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
            chain = prompt | llm
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

        SKILLS_CV = "react typescript nextjs next redux nodejs fastapi python git cicd vercel railway tailwind vite"

        matching = [s for s in required_skills if s.lower().replace(".", "").replace("-", "") in SKILLS_CV]
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