"""
Agente 1: Scraper de ofertas laborales
Busca trabajos en LinkedIn/otras plataformas según criterios
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

class ScraperAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_jobs(self, keywords: str, location: str = "Buenos Aires") -> List[Dict]:
        """
        Busca trabajos según keywords y ubicación
        
        Args:
            keywords: Términos de búsqueda (ej: "Python Developer")
            location: Ubicación (default: Buenos Aires)
            
        Returns:
            Lista de trabajos encontrados con título, empresa, link
        """
        print(f"🔍 Buscando: {keywords} en {location}...")
        
        # Por ahora retornamos datos mock para testing
        # Más adelante implementamos scraping real de LinkedIn
        jobs = [
            {
                "title": "Frontend Developer React",
                "company": "Tech Startup Argentina",
                "location": "Buenos Aires (Remoto)",
                "link": "https://linkedin.com/jobs/view/123456",
                "description": "Buscamos Frontend Developer con experiencia en React, TypeScript y Next.js. Proyecto innovador en fintech.",
                "requirements": ["React", "TypeScript", "3+ años experiencia"]
            },
            {
                "title": "Full Stack Developer",
                "company": "Globant",
                "location": "Buenos Aires (Híbrido)",
                "link": "https://linkedin.com/jobs/view/789012",
                "description": "Desarrollador Full Stack para cliente internacional. Stack: React, Node.js, PostgreSQL.",
                "requirements": ["React", "Node.js", "PostgreSQL", "5+ años"]
            },
            {
                "title": "Senior Frontend Engineer",
                "company": "Mercado Libre",
                "location": "Buenos Aires",
                "link": "https://linkedin.com/jobs/view/345678",
                "description": "Buscamos Senior Frontend para equipo de checkout. React, Next.js, microservicios.",
                "requirements": ["React", "Next.js", "Testing", "Liderazgo técnico"]
            }
        ]
        
        print(f"✅ Encontrados: {len(jobs)} trabajos")
        return jobs

# Test del agente
if __name__ == "__main__":
    agent = ScraperAgent()
    
    # Buscar trabajos
    jobs = agent.search_jobs("Frontend Developer", "Buenos Aires")
    
    # Mostrar resultados
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']} - {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['link']}")
        print(f"   📋 {job['description'][:100]}...")