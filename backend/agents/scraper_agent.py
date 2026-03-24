"""
Agente 1: Scraper usando Adzuna API (Brasil) y JSearch API (Argentina, Chile, Uruguay)
"""

import requests
import os
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict


class ScraperAgent:
    def __init__(self, app_id: str = None, app_key: str = None):
        self.app_id = app_id or os.getenv("ADZUNA_APP_ID")
        self.app_key = app_key or os.getenv("ADZUNA_APP_KEY")
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.country = "br"  # Brasil es free con adzuna api

    def search_jobs(self, keywords: str, location: str) -> List[Dict]:
        """
        Busca empleos reales.
        Adzuna para Brasil, JSearch para Argentina, Chile y Uruguay.
        """
        print(f"🔍 Buscando: {keywords} en {location}...")

        paises_adzuna = ["brasil", "brazil"]
        paises_jsearch = ["argentina", "chile", "uruguay"]
        location_lower = location.lower()

        if location_lower in paises_adzuna:
            if self.app_id and self.app_key:
                jobs = self._search_adzuna(keywords, location)
                if jobs:
                    return jobs

        if location_lower in paises_jsearch or location_lower not in paises_adzuna:
            jobs = self._search_jsearch(keywords, location)
            if jobs:
                return jobs

        print("⚠️ Sin resultados en APIs")
        return self._get_mock_jobs(keywords)

    def _search_adzuna(self, keywords: str, location: str) -> List[Dict]:
        """
        Busca empleos usando Adzuna API — solo Brasil (free tier)
        """
        print(f"🔍 Buscando en Adzuna: {keywords} en {location}...")

        if not self.app_id or not self.app_key:
            print("⚠️ Credenciales Adzuna no configuradas")
            return []

        try:
            url = f"{self.base_url}/{self.country}/search/1"
            params = {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "what": keywords,
                "results_per_page": 15,
                "content-type": "application/json"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"⚠️ Adzuna status {response.status_code}")
                return []

            data = response.json()
            results = data.get("results", [])

            if not results:
                print("⚠️ Adzuna sin resultados")
                return []

            jobs = []
            for job in results:
                try:
                    description = job.get("description", "")
                    title = job.get("title", "Sin título")
                    company = job.get("company", {}).get("display_name", "Empresa Confidencial")
                    job_location = job.get("location", {}).get("display_name", location)
                    link = job.get("redirect_url", "https://adzuna.com")
                    salary_min = job.get("salary_min")
                    salary_max = job.get("salary_max")

                    salary = self._format_salary(salary_min, salary_max)

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "link": link,
                        "description": description[:250],
                        "salary": salary,
                        "requirements": self._extract_keywords(title + " " + description)
                    })

                except Exception:
                    continue

            print(f"✅ {len(jobs)} ofertas reales de Adzuna Brasil")
            return jobs

        except Exception as e:
            print(f"❌ Error Adzuna: {e}")
            return []

    def _search_jsearch(self, keywords: str, location: str) -> List[Dict]:
        """
        Busca empleos usando JSearch API (RapidAPI)
        Cubre Argentina, Chile, Uruguay y toda Latam
        """
        print(f"🔍 Buscando en JSearch: {keywords} en {location}...")

        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not rapidapi_key:
            print("⚠️ RAPIDAPI_KEY no configurada")
            return []
        country_codes = {
         "argentina": "ar",
         "chile": "cl",
         "uruguay": "uy",
         "brasil": "br",
         "brazil": "br"
}
        country_code = country_codes.get(location.lower(), "ar")
        try:
            url = "https://jsearch.p.rapidapi.com/search"
            headers = {
                "X-RapidAPI-Key": rapidapi_key,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            params = {
                "query": f"{keywords} {location}",
                "page": "1",
                "num_pages": "1",
                "date_posted": "all",
                "country": country_code,
                "language": "es"
            }

            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code != 200:
                print(f"⚠️ JSearch status {response.status_code}")
                return []

            data = response.json()
            results = data.get("data", [])

            if not results:
                print("⚠️ JSearch sin resultados")
                return []

            jobs = []
            for job in results:
                try:
                    title = str(job.get("job_title") or "Sin título")
                    company = str(job.get("employer_name") or "Empresa Confidencial")
                    location_name = str(job.get("job_city") or job.get("job_country") or location)
                    description = str(job.get("job_description") or "")[:250]
                    link = job.get("job_apply_link") or job.get("job_google_link", "")
                    salary_min = job.get("job_min_salary")
                    salary_max = job.get("job_max_salary")

                    salary = self._format_salary(salary_min, salary_max)

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location_name,
                        "link": link,
                        "description": description,
                        "salary": salary,
                        "requirements": self._extract_keywords(title + " " + description)
                    })

                except Exception:
                    continue

            if not jobs:
                print("⚠️ JSearch devolvió resultados, pero no se pudieron parsear ofertas válidas")
                return []

            print(f"✅ {len(jobs)} ofertas encontradas via JSearch")
            return jobs

        except Exception as e:
            print(f"❌ Error JSearch: {e}")
            return []

    def _extract_keywords(self, text: str) -> List[str]:
        tech = [
            'react', 'typescript', 'javascript', 'python', 'node.js', 'next.js',
            'vue', 'angular', 'sql', 'postgresql', 'mongodb', 'aws', 'docker',
            'git', 'fastapi', 'django', 'java', 'kotlin', 'swift', 'tailwind'
        ]
        text_lower = text.lower()
        found = [kw for kw in tech if kw in text_lower]
        return found[:5] if found else ['javascript', 'html', 'css']

    def _format_salary(self, salary_min, salary_max) -> str:
        def _to_float(value):
            try:
                if value is None:
                    return None
                if isinstance(value, (int, float)):
                    return float(value)
                if isinstance(value, str):
                    cleaned = value.replace(",", "").replace("$", "").strip()
                    return float(cleaned) if cleaned else None
                return None
            except (TypeError, ValueError):
                return None

        min_value = _to_float(salary_min)
        max_value = _to_float(salary_max)

        if min_value and max_value:
            return f"${min_value:,.0f} - ${max_value:,.0f}"
        if min_value:
            return f"Desde ${min_value:,.0f}"
        return ""

    def _get_mock_jobs(self, keywords: str) -> List[Dict]:
        kw = keywords.strip() or "Frontend Developer"
        return [
            {
                "title": f"{kw} - React",
                "company": "Startup LATAM (Mock)",
                "location": "Remoto",
                "link": "https://example.com/jobs/frontend-react",
                "description": "Buscamos perfil frontend con React, TypeScript, testing y trabajo con APIs REST.",
                "salary": "",
                "requirements": ["react", "typescript", "javascript", "git", "api"]
            },
            {
                "title": f"{kw} - Next.js",
                "company": "Producto SaaS (Mock)",
                "location": "Argentina",
                "link": "https://example.com/jobs/frontend-nextjs",
                "description": "Rol frontend para construir interfaces con Next.js, Tailwind y buenas prácticas de UX.",
                "salary": "",
                "requirements": ["next.js", "react", "tailwind", "typescript", "ux"]
            },
            {
                "title": f"{kw} - Fullstack JS",
                "company": "Consultora Tech (Mock)",
                "location": "Híbrido",
                "link": "https://example.com/jobs/fullstack-js",
                "description": "Proyecto fullstack con Node.js, React y MongoDB. Valoramos CI/CD y comunicación.",
                "salary": "",
                "requirements": ["node.js", "react", "mongodb", "ci/cd", "javascript"]
            }
        ]


if __name__ == "__main__":
    agent = ScraperAgent()
    jobs = agent.search_jobs("Frontend Developer", "Argentina")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        if job.get('salary'):
            print(f"   💰 {job['salary']}")
        print(f"   🔗 {job['link']}")
