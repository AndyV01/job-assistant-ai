# Job Assistant AI 🚀

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-06B6D4?logo=tailwindcss&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-7B61FF)
![Llama%203.2](https://img.shields.io/badge/Llama%203.2-Local%20LLM-orange)

Asistente de búsqueda laboral potenciado por IA con arquitectura multi-agente. El sistema unifica tres tareas clave en un solo flujo: encontrar ofertas, analizar su ajuste técnico y optimizar el CV para mejorar la postulación.

---

## 🌐 Demo en producción

- **Frontend (Vercel):** https://job-assistant-ai-tzle.vercel.app/
- **Backend (Railway):** https://railway.com/project/55b3b547-1c61-470f-a50f-9065e409406e

> Nota: el enlace de Railway corresponde al proyecto desplegado. Si deseas exponer una URL pública de API en el README, agrega el dominio final del servicio (por ejemplo `https://<tu-servicio>.up.railway.app`).

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
┌───────────────────────────────────────────────────┐
│          JobAssistantOrchestrator                │
│ coordina el flujo extremo a extremo              │
├───────────────────────────────────────────────────┤
│ 1) ScraperAgent  → obtiene ofertas               │
│ 2) AnalyzerAgent → extrae skills + seniority +   │
│                    calcula match score            │
│ 3) CVOptimizerAgent (RAG) → consulta CV          │
│    vectorizado en Chroma + Llama 3.2             │
└───────────────────────────────────────────────────┘
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
- **ChromaDB** como vector store del CV.
- **Ollama + Llama 3.2** para inferencia local.

---

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
pip install fastapi uvicorn langchain langchain-community chromadb pypdf beautifulsoup4 requests
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
3. Define ubicación (ej: `Buenos Aires`).
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
  "location": "Buenos Aires"
}
```

---

## 📌 Uso moderado

Para mantener una experiencia estable y evitar bloqueos en fuentes externas:

- Evita ejecuciones masivas o automatizadas en ráfaga.
- Espera algunos segundos entre búsquedas consecutivas.
- Limita pruebas de carga a entornos controlados.
- Si integras nuevas fuentes de scraping, respeta términos de uso y robots.txt cuando aplique.

---

## 📁 Estructura del proyecto

```bash
job-assistant-ai/
├── backend/
│   ├── agents/
│   │   ├── scraper_agent.py
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
├── data/
│   └── mi_cv.pdf
└── README.md
```

---

## 🛣️ Roadmap

- [ ] Integrar más fuentes laborales con normalización robusta de datos.
- [ ] Mejorar scoring por seniority, experiencia y skills críticas.
- [ ] Agregar persistencia de histórico de búsquedas y postulaciones.
- [ ] Incorporar autenticación y soporte multiusuario.
- [ ] Extender recomendaciones con plan de upskilling.

---

## 👤 Autor

**Andy Vallarino**

- GitHub: [@andyduffdj25](https://github.com/andyduffdj25)
- Email: andyduffdj25@gmail.com
- Portafolio: https://portfolio-nextjs-nine-lac.vercel.app/

Si te interesa colaborar o proponer mejoras, abre un issue o PR. 🚀
