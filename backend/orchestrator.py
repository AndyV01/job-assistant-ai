"""
Orquestador - Coordina todos los agentes del sistema
"""

from agents.scraper_agent import ScraperAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.cv_optimizer_agent import CVOptimizerAgent
from typing import List, Dict

class JobAssistantOrchestrator:
    def __init__(self):
        print("🤖 Inicializando Job Assistant con arquitectura multi-agente...")
        self.scraper = ScraperAgent()
        self.analyzer = AnalyzerAgent()
        self.cv_optimizer = CVOptimizerAgent()
        print("✅ Agentes cargados: Scraper, Analyzer, CV Optimizer")
    
    def full_pipeline(self, keywords: str, location: str = "Buenos Aires") -> Dict:
        """
        Pipeline completo: busca, analiza y optimiza CV
        """
        print(f"\n{'='*60}")
        print(f"🎯 BÚSQUEDA COMPLETA: {keywords} en {location}")
        print(f"{'='*60}\n")
        
        # PASO 1: Buscar trabajos
        print("📍 PASO 1: Buscando ofertas...")
        jobs = self.scraper.search_jobs(keywords, location)
        
        if not jobs:
            return {"error": "No se encontraron ofertas"}
        
        # PASO 2: Analizar trabajos
        print(f"\n📊 PASO 2: Analizando {len(jobs)} ofertas...")
        analyses = self.analyzer.analyze_multiple(jobs)
        
        # PASO 3: Optimizar CV para el mejor match
        analyses_sorted = sorted(analyses, key=lambda x: x['match_score'], reverse=True)
        best_match = analyses_sorted[0]
        
        print(f"\n🔧 PASO 3: Optimizando CV para mejor match...")
        cv_optimization = self.cv_optimizer.optimize_for_job(best_match)
        
        return {
            "analyses": analyses_sorted,
            "best_match": best_match,
            "cv_optimization": cv_optimization,
            "total_found": len(jobs)
        }
    
    def show_full_results(self, results: Dict):
        """
        Muestra resultados completos
        """
        print("\n" + "="*60)
        print("📋 TOP 3 MEJORES MATCHES")
        print("="*60)
        
        for i, analysis in enumerate(results['analyses'][:3], 1):
            print(f"\n🏆 #{i} - {analysis['job_title']}")
            print(f"   🏢 {analysis['company']}")
            print(f"   ⭐ Match: {analysis['match_score']}/100")
            print(f"   💻 Skills: {', '.join(analysis['tech_skills'][:3])}")
        
        print("\n" + "="*60)
        print("💡 OPTIMIZACIÓN DE CV PARA MEJOR MATCH")
        print("="*60)
        
        opt = results['cv_optimization']
        print(f"\n🎯 Trabajo: {opt['job_title']}")
        print(f"\n✅ Skills que tenés: {', '.join(opt['matching_skills'])}")
        print(f"\n❌ Skills faltantes: {', '.join(opt['missing_skills']) if opt['missing_skills'] else 'Ninguna'}")
        print(f"\n{opt['recommendations'][:500]}...")

# Test
if __name__ == "__main__":
    orchestrator = JobAssistantOrchestrator()
    results = orchestrator.full_pipeline("Frontend Developer")
    orchestrator.show_full_results(results)
    print("\n🎉 Sistema multi-agente completo funcionando!")