"""
Orquestador - Coordina todos los agentes del sistema
"""

from agents.scraper_agent import ScraperAgent
from agents.analyzer_agent import AnalyzerAgent
from typing import List, Dict

class JobAssistantOrchestrator:
    def __init__(self):
        print("🤖 Inicializando Job Assistant con arquitectura multi-agente...")
        self.scraper = ScraperAgent()
        self.analyzer = AnalyzerAgent()
        print("✅ Agentes cargados: Scraper, Analyzer")
    
    def search_and_analyze(self, keywords: str, location: str = "Buenos Aires") -> Dict:
        """
        Flujo completo: busca trabajos y los analiza
        
        Args:
            keywords: Términos de búsqueda
            location: Ubicación
            
        Returns:
            Diccionario con resultados y análisis
        """
        print(f"\n{'='*60}")
        print(f"🎯 BÚSQUEDA: {keywords} en {location}")
        print(f"{'='*60}\n")
        
        # PASO 1: Scraper busca trabajos
        print("📍 PASO 1: Buscando ofertas laborales...")
        jobs = self.scraper.search_jobs(keywords, location)
        
        if not jobs:
            print("❌ No se encontraron ofertas")
            return {"jobs": [], "analyses": []}
        
        # PASO 2: Analyzer analiza cada trabajo
        print(f"\n📊 PASO 2: Analizando {len(jobs)} ofertas...")
        analyses = self.analyzer.analyze_multiple(jobs)
        
        # PASO 3: Ordenar por match score
        analyses_sorted = sorted(analyses, key=lambda x: x['match_score'], reverse=True)
        
        print(f"\n✅ Análisis completado\n")
        
        return {
            "jobs": jobs,
            "analyses": analyses_sorted,
            "total_found": len(jobs)
        }
    
    def show_results(self, results: Dict):
        """
        Muestra los resultados de forma legible
        """
        if not results['analyses']:
            print("No hay resultados para mostrar")
            return
        
        print("\n" + "="*60)
        print("📋 RESULTADOS ORDENADOS POR MATCH")
        print("="*60)
        
        for i, analysis in enumerate(results['analyses'], 1):
            print(f"\n🏆 #{i} - {analysis['job_title']}")
            print(f"   🏢 Empresa: {analysis['company']}")
            print(f"   🎯 Nivel: {analysis['seniority_level']}")
            print(f"   ⏱ Experiencia: {analysis['experience_required']}")
            print(f"   ⭐ Match Score: {analysis['match_score']}/100")
            print(f"   💻 Skills: {', '.join(analysis['tech_skills'][:5])}")  # Top 5
            print(f"   🔗 Link: {analysis['link']}")
        
        print(f"\n{'='*60}")
        print(f"Total encontrados: {results['total_found']}")
        print(f"{'='*60}\n")

# Test del orquestador
if __name__ == "__main__":
    # Crear orquestador
    orchestrator = JobAssistantOrchestrator()
    
    # Ejecutar búsqueda y análisis
    results = orchestrator.search_and_analyze(
        keywords="Frontend Developer",
        location="Buenos Aires"
    )
    
    # Mostrar resultados
    orchestrator.show_results(results)
    
    print("\n🎉 Sistema multi-agente funcionando correctamente!")