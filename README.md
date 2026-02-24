# Job Assistant AI

Asistente inteligente para potenciar la búsqueda laboral mediante inteligencia artificial, con un enfoque backend en Python y arquitectura preparada para crecer por etapas.

## 🧭 Descripción general

**Job Assistant AI** es un proyecto en fase inicial orientado a construir un asistente que ayude a personas en búsqueda de empleo a tomar mejores decisiones, automatizar tareas repetitivas y mejorar la calidad de sus postulaciones.

Actualmente, el repositorio contiene una base de backend con componentes tempranos de orquestación y agentes. El objetivo es evolucionar de un prototipo técnico a una plataforma robusta y modular.

## 🎯 Objetivos del proyecto

- Centralizar funcionalidades de asistencia laboral en un único backend.
- Incorporar capacidades de IA para análisis y recomendación contextual.
- Facilitar la automatización de tareas como recopilación y análisis de información.
- Diseñar una arquitectura escalable para futuras integraciones (APIs externas, panel web, métricas y más).
- Mantener buenas prácticas de desarrollo para favorecer mantenibilidad y colaboración.

## 🚧 Estado actual del proyecto

> **Estado:** En desarrollo temprano (MVP técnico en construcción).

Este proyecto aún no está listo para producción. La estructura y funcionalidades pueden cambiar con frecuencia mientras se valida la dirección técnica y funcional.

## 🧰 Tecnologías utilizadas

Base tecnológica actual:

- **Python** (núcleo del backend)
- Estructura inicial basada en agentes y orquestación

Tecnologías candidatas para próximas etapas (sujetas a decisión):

- Framework API (por ejemplo, FastAPI)
- Persistencia de datos (por ejemplo, PostgreSQL)
- Contenerización y despliegue (Docker / CI/CD)

## 🗂️ Estructura actual del proyecto

Estructura mínima existente en esta etapa:

```bash
job-assistant-ai/
├── backend/
│   ├── agents/
│   │   ├── analyzer_agent.py
│   │   └── scraper_agent.py
│   └── orchestrator.py
└── README.md
```

> Esta estructura es provisional y crecerá conforme se incorporen módulos de API, configuración, pruebas y documentación técnica adicional.

## ✅ Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python **3.10+**
- `pip` actualizado
- Git

Opcional recomendado:

- `venv` (entorno virtual)

## ⚙️ Instalación paso a paso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/<tu-usuario>/job-assistant-ai.git
   ```

2. Entrar en la carpeta del proyecto:

   ```bash
   cd job-assistant-ai
   ```

3. (Opcional) Crear y activar entorno virtual.

4. Instalar dependencias cuando el archivo de requisitos esté disponible:

   ```bash
   pip install -r requirements.txt
   ```

> Si `requirements.txt` aún no existe en tu versión local, continúa con la configuración base y agrega dependencias según necesidad del módulo que vayas a trabajar.

## 🐍 Configuración de entorno virtual

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 🔐 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto para manejar configuración sensible.

Ejemplo mínimo:

```env
# Entorno
ENV=development

# Configuración de logs
LOG_LEVEL=INFO

# Claves de servicios externos (ejemplos)
OPENAI_API_KEY=tu_api_key_aqui
JOBS_API_BASE_URL=https://api.ejemplo.com
```

> No subas tu archivo `.env` al repositorio. Usa un `.env.example` para compartir variables requeridas sin exponer secretos.

## ▶️ Cómo ejecutar el proyecto

Dado el estado actual (fase temprana), el backend puede ejecutarse de forma manual desde el módulo principal:

```bash
python backend/orchestrator.py
```

Si más adelante se incorpora un framework API, esta sección se actualizará con comandos de ejecución por entorno (dev/staging/prod).

## 🛣️ Roadmap / Próximas funcionalidades

- [ ] Definir interfaz de servicio (CLI o API REST) para consumo externo.
- [ ] Estandarizar configuración del proyecto (`requirements.txt` / `pyproject.toml`).
- [ ] Incorporar pruebas automatizadas (unitarias e integración).
- [ ] Agregar validaciones de calidad (lint, format, type checking).
- [ ] Integrar fuentes de ofertas laborales y enriquecimiento de datos.
- [ ] Implementar recomendaciones personalizadas para CV, perfil y postulaciones.
- [ ] Documentar arquitectura técnica y decisiones de diseño (ADR).

## 🤝 Contribuciones

Las contribuciones son bienvenidas, especialmente en esta etapa temprana.

Flujo sugerido:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio (`feature/nombre-cambio`).
3. Realiza commits claros y pequeños.
4. Abre un Pull Request con contexto técnico y alcance.

Buenas prácticas recomendadas:

- Mantener consistencia de estilo en Python.
- Incluir documentación junto con cambios funcionales.
- Añadir o actualizar pruebas cuando aplique.

## 📄 Licencia

Pendiente de definición.

Hasta que se agregue un archivo `LICENSE`, todos los derechos quedan reservados por el autor del repositorio.
