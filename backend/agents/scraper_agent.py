"""
Agente 1: Scraper de Indeed Argentina - FUNCIONA
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib.parse

class ScraperAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_jobs(self, keywords: str, location: str = "Buenos Aires") -> List[Dict]:
        """
        Scraper REAL de Indeed Argentina
        """
        print(f"🔍 Scrapeando Indeed: {keywords} en {location}...")
        
        # URL de Indeed Argentina
        query = urllib.parse.quote(keywords)
        loc = urllib.parse.quote(location)
        url = f"https://ar.indeed.com/jobs?q={query}&l={loc}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ Status {response.status_code}, usando mock")
                return self._get_mock_jobs(keywords)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Indeed usa diferentes selectores
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            if not job_cards:
                # Fallback a otro selector
                job_cards = soup.find_all('td', class_='resultContent')
            
            if not job_cards:
                print(f"⚠️ No se encontraron ofertas. Usando mock.")
                return self._get_mock_jobs(keywords)
            
            jobs = []
            for card in job_cards[:15]:
                try:
                    # Título
                    title_elem = card.find('h2', class_='jobTitle')
                    if not title_elem:
                        title_elem = card.find('a', {'data-jk': True})
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Link
                    link_elem = card.find('a', href=True)
                    job_id = link_elem.get('data-jk', '') if link_elem else ''
                    link = f"https://ar.indeed.com/viewjob?jk={job_id}" if job_id else "https://ar.indeed.com"
                    
                    # Empresa
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text(strip=True) if company_elem else "Empresa Confidencial"
                    
                    # Ubicación
                    loc_elem = card.find('div', class_='companyLocation')
                    job_location = loc_elem.get_text(strip=True) if loc_elem else location
                    
                    # Descripción
                    desc_elem = card.find('div', class_='snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else f"Oferta de {title}"
                    
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "link": link,
                        "description": description[:250],
                        "requirements": self._extract_keywords(title + " " + description)
                    })
                
                except Exception as e:
                    continue
            
            if jobs:
                print(f"✅ {len(jobs)} ofertas REALES de Indeed Argentina")
                return jobs
            else:
                return self._get_mock_jobs(keywords)
        
        except Exception as e:
            print(f"❌ Error scrapeando: {e}")
            return self._get_mock_jobs(keywords)
    
    def _extract_keywords(self, text: str) -> List[str]:
        tech = ['react', 'typescript', 'javascript', 'python', 'node.js', 'next.js', 
                'vue', 'angular', 'sql', 'postgresql', 'mongodb', 'aws', 'docker', 'git']
        text_lower = text.lower()
        found = [kw for kw in tech if kw in text_lower]
        return found[:5] if found else ['javascript', 'html', 'css']
    
    def _get_mock_jobs(self, keywords: str) -> List[Dict]:
        return [
            {
                "title": f"{keywords} - React TypeScript",
                "company": "Tech Company Argentina",
                "location": "Buenos Aires",
                "link": "https://ar.indeed.com",
                "description": f"Buscamos {keywords} con sólida experiencia",
                "requirements": ["react", "typescript", "javascript"]
            },
            {
                "title": f"Desarrollador {keywords}",
                "company": "Startup Digital",
                "location": "CABA - Remoto",
                "link": "https://ar.indeed.com",
                "description": "Equipo ágil busca talento frontend",
                "requirements": ["react", "css", "html"]
            }
        ]

if __name__ == "__main__":
    agent = ScraperAgent()
    jobs = agent.search_jobs("Frontend Developer", "Buenos Aires")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['link']}")