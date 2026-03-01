"""
Agente 2: Analyzer - Analiza ofertas laborales
Extrae requisitos, skills, nivel de seniority
"""

from typing import List, Dict
import re

class AnalyzerAgent:
    def __init__(self):
        # Keywords comunes en tech jobs
        self.tech_skills = [
            "react", "typescript", "javascript", "python", "node.js", 
            "next.js", "vue", "angular", "sql", "mongodb", "postgresql",
            "aws", "docker", "kubernetes", "git", "ci/cd", "fastapi",
            "django", "flask", "tailwind", "redux", "graphql"
        ]
        
        self.soft_skills = [
            "liderazgo", "comunicación", "trabajo en equipo", "agile",
            "scrum", "inglés", "autonomía", "problem solving"
        ]
    
    def analyze_job(self, job: Dict) -> Dict:
        """
        Analiza una oferta laboral y extrae información clave
        
        Args:
            job: Diccionario con datos del trabajo
            
        Returns:
            Diccionario con análisis completo
        """
        description = job.get('description', '').lower()
        requirements = job.get('requirements', [])
        
        # Extraer skills técnicas
        found_tech_skills = []
        for skill in self.tech_skills:
            if skill in description or any(skill.lower() in req.lower() for req in requirements):
                found_tech_skills.append(skill)
        
        # Extraer skills blandas
        found_soft_skills = []
        for skill in self.soft_skills:
            if skill in description:
                found_soft_skills.append(skill)
        
        # Detectar años de experiencia
        experience_years = self._extract_experience(description)
        
        # Detectar nivel de seniority
        seniority = self._detect_seniority(job['title'], description)
        
        # Calcular match score (placeholder por ahora)
        match_score = len(found_tech_skills) * 10  # Simple score
        
        analysis = {
            "job_title": job['title'],
            "company": job['company'],
            "tech_skills": found_tech_skills,
            "soft_skills": found_soft_skills,
            "experience_required": experience_years,
            "seniority_level": seniority,
            "match_score": match_score,
            "link": job['link'],
            "description": job.get('description', '')
        }
        
        return analysis
    
    def _extract_experience(self, text: str) -> str:
        """
        Extrae años de experiencia requeridos del texto
        """
        # Buscar patrones como "3+ años", "5 años", etc
        patterns = [
            r'(\d+)\+?\s*años',
            r'(\d+)\+?\s*years',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)}+ años"
        
        return "No especificado"
    
    def _detect_seniority(self, title: str, description: str) -> str:
        """
        Detecta nivel de seniority (Junior, Semi-Senior, Senior)
        """
        title_lower = title.lower()
        desc_lower = description.lower()
        
        if 'senior' in title_lower or 'sr' in title_lower:
            return "Senior"
        elif 'junior' in title_lower or 'jr' in title_lower:
            return "Junior"
        elif 'semi' in title_lower or 'ssr' in title_lower:
            return "Semi-Senior"
        elif 'lead' in title_lower or 'principal' in title_lower:
            return "Lead/Principal"
        else:
            # Inferir por años de experiencia
            if '5+' in desc_lower or '6+' in desc_lower:
                return "Senior"
            elif '3+' in desc_lower or '4+' in desc_lower:
                return "Semi-Senior"
            else:
                return "Semi-Senior"  # Default
    
    def analyze_multiple(self, jobs: List[Dict]) -> List[Dict]:
        """
        Analiza múltiples ofertas
        """
        analyses = []
        for job in jobs:
            analysis = self.analyze_job(job)
            analyses.append(analysis)
        
        return analyses

# Test del agente
if __name__ == "__main__":
    # Importar el agente 1 para obtener trabajos
    import sys
    sys.path.append('..')
    from scraper_agent import ScraperAgent
    
    # Obtener trabajos del scraper
    scraper = ScraperAgent()
    jobs = scraper.search_jobs("Frontend Developer", "Buenos Aires")
    
    # Analizar con el Analyzer
    analyzer = AnalyzerAgent()
    analyses = analyzer.analyze_multiple(jobs)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("ANÁLISIS DE OFERTAS LABORALES")
    print("="*60)
    
    for analysis in analyses:
        print(f"\n📋 {analysis['job_title']} - {analysis['company']}")
        print(f"   🎯 Nivel: {analysis['seniority_level']}")
        print(f"   ⏱ Experiencia: {analysis['experience_required']}")
        print(f"   💻 Skills técnicas: {', '.join(analysis['tech_skills'])}")
        print(f"   🤝 Skills blandas: {', '.join(analysis['soft_skills']) if analysis['soft_skills'] else 'No especificadas'}")
        print(f"   ⭐ Match Score: {analysis['match_score']}/100")