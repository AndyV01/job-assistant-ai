# Job Assistant AI 🚀

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-06B6D4?logo=tailwindcss&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-4B8BBE)
![RAG](https://img.shields.io/badge/RAG-FAISS%20%2B%20Embeddings-00ADD8)
![Groq](https://img.shields.io/badge/Groq-LLM%20Cloud-F55036?logo=groq&logoColor=white)
![LangSmith](https://img.shields.io/badge/LangSmith-Observability-FF6B35)

Asistente de búsqueda laboral potenciado por IA con arquitectura multi-agente. El sistema unifica tres tareas clave en un solo flujo: encontrar ofertas, analizar su ajuste técnico y optimizar el CV para mejorar la postulación.

---

<img width="1673" height="939" alt="Estación de trabajo nocturna con luces de ciudad" src="https://github.com/user-attachments/assets/0b356302-26a3-4bfd-87f2-e31fdcccaa2f" />


## 🌐 Demo en producción

- **Frontend (Vercel):** https://job-assistant-ai-tzle.vercel.app/

---

## 🧩 Problema que resuelve

Buscar trabajo en tecnología suele ser un proceso manual y repetitivo:

- Revisar decenas de vacantes para detectar las que realmente encajan.
- Interpretar requisitos técnicos y seniority en poco tiempo.
- Adaptar el CV para cada oportunidad sin perder consistencia.

**Job Assistant AI** automatiza este pipeline con IA, entregando recomendaciones accionables para postular con mayor precisión.

---

## 🏗️ Arquitectura

```text
┌──────────────────────────────┐
│        Frontend (React)      │
│ Formulario + resultados + UI │
└───────────────┬──────────────┘
                │ HTTP (REST)
                ▼
┌──────────────────────────────┐
│       Backend (FastAPI)      │
│   /api/search (entrypoint)   │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────────────────────────┐
│          JobAssistantOrchestrator                │
│ coordina el flujo extremo a extremo              │
├──────────────────────────────────────────────────┤
│ 1) ScraperAgent  → obtiene ofertas reale         │
│    · Adzuna API  → Brasil                        │
│    · JSearch API → Argentina, Chile, Uruguay     │
│ 2) AnalyzerAgent → LLM + JsonOutputParser        │
│                    (Groq + LangChain)            │
│ 3) CVOptimizerAgent → RAG con FAISS +            │
│                    HuggingFace Embeddings        │
│                    + Groq  (Llama 3.3)           │
└──────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────┐
│ Respuesta final al frontend  │
│ top matches + optimización   │
└──────────────────────────────┘
```

---

## ⚙️ Stack tecnológico

- **Python 3.10+** para lógica de negocio y agentes.
- **FastAPI** para exponer endpoints de alto rendimiento.
- **React + Vite** para una UI ágil y moderna.
- **TailwindCSS** para estilos consistentes y rápidos de iterar.
- **LangChain** para orquestación de componentes de IA.
- **LangGraph** para el grafo de estados multi-agente con memoria persistente.
- **Groq API** para inferencia LLM en cloud (Llama 3 via tool calling).
- **Adzuna API** para obtención de ofertas reales.
- **LangSmith** para observabilidad, tracing y monitoreo del pipeline multi-agente.

---

## 🌎 Cobertura de mercados Latam

El scraper enruta automáticamente según el país seleccionado:

| País | API | Fuente de datos |
|------|-----|----------------|
| 🇧🇷 Brasil | Adzuna API | Ofertas reales del mercado brasileño |
| 🇦🇷 Argentina | JSearch (RapidAPI) | Google for Jobs · LinkedIn · Indeed AR · Jooble |
| 🇨🇱 Chile | JSearch (RapidAPI) | Google for Jobs · LinkedIn · Indeed CL |
| 🇺🇾 Uruguay | JSearch (RapidAPI) | Google for Jobs · LinkedIn · Indeed UY |

El sistema selecciona la API correcta automáticamente — el usuario solo elige el país en el formulario.

---

## 🔭 Observabilidad con LangSmith

El sistema cuenta con **tracing completo** de todo el pipeline multi-agente usando [LangSmith](https://smith.langchain.com).

### Qué se trackea

Cada ejecución del pipeline queda registrada con:

- **Latencia por nodo** — cuánto tarda cada agente de forma aislada.
- **Tokens consumidos** — por llamada al LLM y total del pipeline.
- **Llamadas al LLM** — input y output de cada invocación a Llama 3.3 via Groq.
- **Metadata por request** — keywords, location, user_ip.
- **Tags por entorno** — `api`, `production`, nombre de la location.
- **Errores con contexto** — qué nodo falló, cuántos jobs se encontraron, cuántos análisis se generaron.


## 🚀 Ejecución local

### 1) Clonar repositorio

```bash
git clone <REPO_URL>
cd job-assistant-ai
```

### 2) Backend

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

pip install --upgrade pip
pip install fastapi uvicorn langchain langchain-community langchain-groq groq pypdf beautifulsoup4 requests python-dotenv python-multipart faiss-cpu langsmith
```

Ejecutar API:

```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 3) Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Configurar `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Uso

1. Abre la UI en `http://localhost:5173` (o la demo de Vercel).
2. Ingresa keywords del rol (ej: `Backend Developer`).
3. Define ubicación (ej: `Brasil`).
4. Ejecuta la búsqueda.
5. Revisa:
   - Vacantes ordenadas por match.
   - Skills detectadas por oferta.
   - Recomendaciones de optimización de CV.

### Endpoints principales

- `GET /health` → estado del servicio.
- `POST /api/search` → pipeline completo (scraper + analyzer + optimizer).

Ejemplo de request:

```json
{
  "keywords": "Backend Developer",
  "location": "Argentina"
}
```
---

## 🧠 Orquestador con LangGraph

El orquestador implementa un **StateGraph** con nodos, edges condicionales y memoria persistente:

```text
scraper → analyzer → cv_optimizer → END
    ↓          ↓
  error      error (o retry si match_score < 20)
```

- **Retry logic:** si el score promedio es menor a 20, vuelve a buscar ofertas (máximo 3 intentos).
- **Memoria persistente:** usa `MemorySaver` para mantener el estado entre ejecuciones.
- **Control de errores:** cada nodo tiene su propio manejo de excepciones con edge al nodo `error`.
- **Observabilidad:** cada nodo decorado con `@traceable` para tracing completo en LangSmith.

---

## 📄 CV Optimizer con RAG

El `CVOptimizerAgent` implementa **RAG (Retrieval-Augmented Generation)** real:

1. Carga el CV desde PDF con `PyPDFLoader`.
2. Divide el texto en chunks con `RecursiveCharacterTextSplitter`.
3. En cada análisis, busca los 3 chunks más relevantes para el trabajo.
4. Pasa esos chunks al LLM (Groq Llama 3.3) para generar recomendaciones personalizadas.

---

## ℹ️ Fuente de datos

El sistema enruta automáticamente según el mercado seleccionado:

- **Brasil** → Adzuna API (free tier oficial para Brasil)
- **Argentina, Chile, Uruguay** → JSearch via RapidAPI (Google for Jobs + LinkedIn + Indeed Latam)

Todos los datos son reales y en tiempo real. La demo en Vercel está completamente funcional.

### Arquitectura Completa

El proyecto demuestra:

✅ **Sistema multi-agente funcional** con orquestador  
✅ **LLM con tool calling real** via Groq + LangChain  
✅ **RAG real** con FAISS + embeddings para análisis de CV  
✅ **Memoria persistente** con LangGraph MemorySaver  
✅ **Retry logic y control de errores** con edges condicionales   
✅ **Datos reales** via Adzuna API en local y producción  
✅ **CV Optimizer** con upload de CV en tiempo real  
✅ **Backend Python + FastAPI** deployado en Railway  
✅ **Frontend React** deployado en Vercel  
✅ **Integración end-to-end** completa 

### Roadmap de Scraping 

**APIs implementadas:**

1. **Adzuna API** ✅ Activo — Brasil
2. **JSearch via RapidAPI** ✅ Activo — Argentina, Chile, Uruguay

**Próximas integraciones:**
- LinkedIn Jobs API oficial
- Indeed Publisher API
- Expansión a Colombia, México, Perú

---

## 🎯 Valor del Proyecto

Este proyecto demuestra:

- **Arquitectura de sistemas complejos** con múltiples componentes
- **Integración de IA moderna** ( LLMs, LangChain, LangGraph, RAG )
- **Observabilidad production-grade** con LangSmith tracing
- **Cobertura multi-mercado Latam** con enrutamiento inteligente por país
- **Full-stack deployment** en infraestructura cloud
- **Diseño de APIs RESTful** con FastAPI
- **Frontend moderno** con React + Vite

**La capacidad de construir la arquitectura es más valiosa que el scraper en sí.**

---

## 📌 Uso moderado

Para mantener una experiencia estable y evitar bloqueos en fuentes externas:

- Evita ejecuciones masivas o automatizadas en ráfaga.
- Espera algunos segundos entre búsquedas consecutivas.
- Limita pruebas de carga a entornos controlados.
- El plan gratuito de JSearch permite 200 requests/mes.

---

## 📁 Estructura del proyecto

```bash
job-assistant-ai/
├── backend/
│   ├── agents/
│   │   ├── scraper_agent.py     # Adzuna (Brasil) + JSearch (AR/CL/UY)
│   │   ├── analyzer_agent.py
│   │   └── cv_optimizer_agent.py
│   ├── api.py
│   └── orchestrator.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md
```

## 👤 Autor

**Andres Vallarino**

- GitHub: [@AndyV01](https://github.com/AndyV01)
- Email: andyduffdj25@gmail.com
- Portafolio: https://portfolio-nextjs-nine-lac.vercel.app/

Si te interesa colaborar o proponer mejoras, abre un issue o PR. 🚀
