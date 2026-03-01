"""
Agente 1: Scraper usando Adzuna API - Datos reales de empleos
Registro gratuito en: https://developer.adzuna.com
"""

import requests
import os
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict

class ScraperAgent:
    def __init__(self, app_id: str = None, app_key: str = None):
        # Reemplazá con tus credenciales de developer.adzuna.com
        self.app_id = app_id or os.getenv("ADZUNA_APP_ID")
        self.app_key = app_key or os.getenv("ADZUNA_APP_KEY")
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.country = "br"  # Brasil

    def search_jobs(self, keywords: str, location: str = "Brasil") -> List[Dict]:
        """
        Busca empleos reales usando Adzuna API
        """
        print(f"🔍 Buscando en Adzuna: {keywords} en {location}...")

        # Si no hay credenciales configuradas, usar mock
        if not self.app_id or not self.app_key:
            print("⚠️ Credenciales no configuradas, usando mock")
            return self._get_mock_jobs(keywords)

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
                print(f"⚠️ Status {response.status_code}, usando mock")
                return self._get_mock_jobs(keywords)

            data = response.json()
            results = data.get("results", [])

            if not results:
                print("⚠️ Sin resultados, usando mock")
                return self._get_mock_jobs(keywords)

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

                    salary = ""
                    if salary_min and salary_max:
                        salary = f"${salary_min:,.0f} - ${salary_max:,.0f}"
                    elif salary_min:
                        salary = f"Desde ${salary_min:,.0f}"

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

            print(f"✅ {len(jobs)} ofertas reales de Adzuna Argentina")
            return jobs

        except Exception as e:
            print(f"❌ Error: {e}")
            return self._get_mock_jobs(keywords)

    def _extract_keywords(self, text: str) -> List[str]:
        tech = [
            'react', 'typescript', 'javascript', 'python', 'node.js', 'next.js',
            'vue', 'angular', 'sql', 'postgresql', 'mongodb', 'aws', 'docker',
            'git', 'fastapi', 'django', 'java', 'kotlin', 'swift', 'tailwind'
        ]
        text_lower = text.lower()
        found = [kw for kw in tech if kw in text_lower]
        return found[:5] if found else ['javascript', 'html', 'css']

    def _get_mock_jobs(self, keywords: str) -> List[Dict]:
        return []


if __name__ == "__main__":
    agent = ScraperAgent()
    jobs = agent.search_jobs("Frontend Developer")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        if job.get('salary'):
            print(f"   💰 {job['salary']}")
        print(f"   🔗 {job['link']}")
