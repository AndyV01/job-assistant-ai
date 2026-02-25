# Job Assistant AI 🚀

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-06B6D4?logo=tailwindcss&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-7B61FF)
![Llama%203.2](https://img.shields.io/badge/Llama%203.2-Local%20LLM-orange)

Asistente de búsqueda laboral potenciado por IA con **arquitectura multi-agente**. El sistema centraliza tres tareas críticas en un único flujo: encontrar ofertas, analizarlas por skills y optimizar el CV para maximizar el match.

---

## 🧩 Problema que resuelve

Buscar trabajo en tecnología suele implicar procesos manuales y repetitivos:

- Revisar muchas ofertas para identificar cuáles realmente encajan.
- Interpretar requisitos técnicos y de seniority de forma rápida.
- Ajustar el CV para cada oportunidad sin perder consistencia.

**Job Assistant AI** resuelve ese cuello de botella automatizando el pipeline completo con IA local (sin costos por API), entregando recomendaciones accionables para postular con mayor precisión.

---

## 🖼️ Screenshot del frontend

> Captura del frontend: se incluye en la PR cuando el entorno permite levantar Vite/Playwright. En este repositorio no se versionan imágenes binarias para mantener las PRs livianas y compatibles con la política de revisión.

---

## 🏗️ Arquitectura del sistema

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
│    vectorizado en Chroma + Llama 3.2 local       │
└───────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────┐
│ Respuesta final al frontend  │
│ top matches + optimización   │
└──────────────────────────────┘
```

---

## ⚙️ Tech Stack (y por qué se usa)

- **Python 3.10+**: lenguaje principal para backend, agentes y lógica de IA.
- **FastAPI**: capa API de alto rendimiento para conectar frontend y pipeline multi-agente.
- **React + Vite**: interfaz moderna, rápida y orientada a iteración de producto.
- **TailwindCSS**: construcción de UI ágil y consistente.
- **LangChain**: utilidades para flujo de RAG y composición con LLMs.
- **ChromaDB**: almacenamiento vectorial del CV para búsqueda semántica.
- **Ollama + Llama 3.2 local**: inferencia local para reducir costos y dependencia de proveedores externos.

---

## 🚀 Instalación paso a paso

## 1) Clonar el repositorio

```bash
git clone <REPO_URL>
cd job-assistant-ai
```

## 2) Backend (FastAPI + agentes)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

pip install --upgrade pip
pip install fastapi uvicorn langchain langchain-community chromadb pypdf beautifulsoup4 requests
```

> Si usas Ollama local, asegúrate de tener disponible el modelo `llama3.2`.

Ejecutar backend:

```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

## 3) Frontend (React + Vite)

En otra terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Variables recomendadas para frontend (`frontend/.env`):

```env
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Cómo usar el sistema

1. Abrir la UI en `http://localhost:5173`.
2. Escribir **keywords** del rol (ej: `Frontend Developer`).
3. Elegir ubicación (ej: `Buenos Aires`).
4. Ejecutar búsqueda.
5. Revisar:
   - Top oportunidades ordenadas por match.
   - Skills detectadas por oferta.
   - Recomendaciones de optimización de CV para el mejor match.

También puedes consultar el backend:

- `GET /health` → estado del servicio.
- `POST /api/search` → pipeline completo (scraper + analyzer + cv optimizer).

Ejemplo de request:

```json
{
  "keywords": "Frontend Developer",
  "location": "Buenos Aires"
}
```

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

- [ ] Integrar scraping real sobre fuentes laborales (con políticas anti-bloqueo y normalización de datos).
- [ ] Mejorar modelo de scoring (ponderación por seniority, experiencia y skills críticas).
- [ ] Despliegue cloud (backend + frontend + vectorstore persistente).
- [ ] Autenticación y soporte multi-usuario (perfiles y CVs independientes).
- [ ] Historial de postulaciones y tracking de progreso.
- [ ] Evaluación automática de brechas de skills y plan de upskilling.

---

## 💡 ¿Por qué este proyecto?

Este proyecto demuestra capacidades técnicas muy valoradas en equipos de ingeniería aplicada a IA:

- Diseño de **arquitectura multi-agente** con responsabilidades claras.
- Integración end-to-end de **frontend + API + pipeline de IA**.
- Implementación de **RAG local** para reducir costos y controlar datos.
- Orquestación de componentes con foco en **producto real**, no solo demo aislada.
- Base sólida para evolucionar a SaaS de empleabilidad con personalización.

En términos de recruiting técnico, evidencia skills en backend, IA aplicada, arquitectura y delivery de producto.

---

## 👤 Autor y contacto

**Andy Duff**

- GitHub: [@andyduffdj25](https://github.com/andyduffdj25)
- Email: andyduffdj25@gmail.com

---

Si te interesa colaborar o proponer mejoras, abre un issue o PR 🚀
