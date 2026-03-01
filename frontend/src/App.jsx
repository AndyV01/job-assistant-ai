import { useMemo, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const quickTips = [
  "Incluye verbos de impacto en tu experiencia.",
  "Destaca resultados medibles en cada proyecto.",
  "Adapta tu CV al stack tecnológico del rol.",
  "Prioriza skills clave en el primer tercio del CV.",
];


const scoreLabel = (score) => {
  if (score >= 85) return "Match excelente 🚀";
  if (score >= 70) return "Match sólido ✨";
  return "Buen potencial 💪";
};

const CircularProgress = ({ score }) => {
  const ringStyle = {
    background: `conic-gradient(#22d3ee ${score * 3.6}deg, rgba(255,255,255,0.14) 0deg)`,
  };

  return (
    <div className="score-wrap">
      <div className="score-ring" style={ringStyle}>
        <div className="score-center">
          <strong>{score}</strong>
          <span>/100</span>
        </div>
      </div>
      <p>{scoreLabel(score)}</p>
    </div>
  );
};

const SkeletonCard = () => (
  <div className="job-card skeleton">
    <div className="sk-line w-60" />
    <div className="sk-line w-40" />
    <div className="sk-grid">
      <div className="sk-pill" />
      <div className="sk-pill" />
      <div className="sk-pill" />
    </div>
    <div className="sk-line w-90" />
  </div>
);

function App() {
  const [keywords, setKeywords] = useState();
  const [location, setLocation] = useState();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState(null);
  const [uploadingCV, setUploadingCV] = useState(false);
  const [cvLoaded, setCvLoaded] = useState(false);


  const topMatches = useMemo(() => results?.analyses || [], [results]);

  const runPipeline = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keywords, location }),
      });

      if (!response.ok) {
        throw new Error("No se pudo conectar al backend. Mostrando demo.");
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadCV = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadingCV(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/upload-cv`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setCvLoaded(true);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setUploadingCV(false);
    }
  };

  return (
    <>
      <style>{`
        :root {
          font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
          color: #e8f7ff;
          background: #040713;
        }
        * { box-sizing: border-box; }
        body {
          margin: 0;
          min-height: 100vh;
          background:
            radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.34), transparent 40%),
            radial-gradient(circle at 90% 0%, rgba(168, 85, 247, 0.34), transparent 35%),
            radial-gradient(circle at 40% 95%, rgba(59, 130, 246, 0.22), transparent 45%),
            linear-gradient(140deg, #040713, #0a1130 45%, #1b1042);
          color: inherit;
        }
        .app {
          max-width: 1100px;
          margin: 0 auto;
          padding: 32px 18px 64px;
        }
        .hero {
          padding: 26px;
          border-radius: 24px;
          border: 1px solid rgba(255, 255, 255, 0.2);
          background: linear-gradient(145deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08));
          box-shadow: 0 20px 50px rgba(0,0,0,0.34);
          backdrop-filter: blur(18px);
          animation: floatIn .8s ease;
        }
        h1 { margin: 0 0 8px; font-size: clamp(1.7rem, 3vw, 2.7rem); }
        .subtitle { margin: 0; opacity: 0.86; }
        form {
          margin-top: 22px;
          display: grid;
          grid-template-columns: 2fr 1.5fr auto;
          gap: 12px;
        }
        .input-wrap {
          display: flex;
          align-items: center;
          gap: 10px;
          border-radius: 16px;
          padding: 0 12px;
          background: rgba(255, 255, 255, 0.12);
          border: 1px solid rgba(255, 255, 255, 0.22);
        }
        input {
          width: 100%;
          background: transparent;
          border: none;
          outline: none;
          color: #ecfeff;
          padding: 14px 0;
          font-size: 0.98rem;
        }
        button {
          border: 0;
          border-radius: 16px;
          padding: 0 18px;
          font-weight: 700;
          color: #041524;
          background: linear-gradient(120deg, #67e8f9, #a5b4fc, #f0abfc);
          cursor: pointer;
          transition: transform .2s ease, box-shadow .2s ease;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 12px 26px rgba(125, 211, 252, 0.35); }
        button:disabled { opacity: .7; cursor: wait; }
        .warn {
          margin-top: 12px;
          color: #fef08a;
          background: rgba(234, 179, 8, 0.16);
          border: 1px solid rgba(234, 179, 8, 0.45);
          border-radius: 12px;
          padding: 10px 12px;
        }
        .results {
          margin-top: 20px;
          display: grid;
          grid-template-columns: 1.2fr 1fr;
          gap: 18px;
          align-items: start;
        }
        .panel {
          border-radius: 22px;
          border: 1px solid rgba(255,255,255,.22);
          background: rgba(255,255,255,.09);
          backdrop-filter: blur(16px);
          box-shadow: 0 22px 40px rgba(2, 8, 23, 0.35);
          padding: 18px;
          animation: floatIn .65s ease;
        }
        .panel-title {
          margin: 0 0 14px;
          font-size: 1.1rem;
        }
        .job-grid { display: grid; gap: 12px; }
        .job-card {
          border: 1px solid rgba(255,255,255,.2);
          border-radius: 16px;
          padding: 14px;
          background: rgba(255,255,255,.08);
          transition: transform .2s ease, border-color .2s ease, background .2s ease;
        }
        .job-card:hover {
          transform: translateY(-4px) scale(1.01);
          border-color: rgba(125, 211, 252, 0.65);
          background: rgba(191, 219, 254, 0.13);
        }
        .job-card h3 { margin: 0 0 6px; font-size: 1rem; }
        .muted { margin: 0; opacity: .85; font-size: .9rem; }
        .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
        .chip {
          font-size: .78rem;
          border-radius: 999px;
          padding: 6px 10px;
          background: rgba(8, 47, 73, .6);
          border: 1px solid rgba(125, 211, 252, .45);
        }
        .score-wrap { text-align: center; margin: 10px 0 18px; }
        .score-ring {
          width: 128px;
          aspect-ratio: 1;
          border-radius: 50%;
          margin: 0 auto;
          padding: 12px;
          animation: pulse 2.8s ease-in-out infinite;
        }
        .score-center {
          height: 100%;
          width: 100%;
          border-radius: 50%;
          display: grid;
          place-content: center;
          background: rgba(2, 6, 23, .8);
          border: 1px solid rgba(255,255,255,.16);
        }
        .score-center strong { font-size: 1.7rem; line-height: 1; }
        .score-center span { opacity: .76; font-size: .75rem; }
        .tips { margin: 10px 0 0; padding-left: 1.1rem; opacity: .9; }
        .skeleton { pointer-events: none; }
        .sk-line, .sk-pill {
          border-radius: 10px;
          background: linear-gradient(90deg, rgba(226,232,240,.14), rgba(226,232,240,.42), rgba(226,232,240,.14));
          background-size: 220% 100%;
          animation: shine 1.2s linear infinite;
        }
        .sk-line { height: 14px; margin-bottom: 10px; }
        .w-60 { width: 60%; } .w-40 { width: 40%; } .w-90 { width: 90%; }
        .sk-grid { display:flex; gap:8px; margin-bottom:10px; }
        .sk-pill { width: 72px; height: 24px; border-radius: 999px; }
        @media (max-width: 900px) {
          .results { grid-template-columns: 1fr; }
        }
        @media (max-width: 720px) {
          .app { padding: 18px 12px 40px; }
          .hero { padding: 18px; border-radius: 18px; }
          form { grid-template-columns: 1fr; }
          button { height: 48px; }
        }
        @keyframes shine { 0% { background-position: 200% 0; } 100% { background-position: -40% 0; } }
        @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.04); } }
        @keyframes floatIn { from { opacity:0; transform: translateY(10px); } to { opacity:1; transform: translateY(0); } }
      `}</style>

      <main className="app">
        <section className="hero">
          <h1>🚀 Job Assistant AI</h1>
          <p className="subtitle">Tu próximo trabajo ya existe. Solo falta encontrarlo antes que los demás.</p>

          <form onSubmit={runPipeline}>
            <label className="input-wrap">
              <span>🔎</span>
              <input value={keywords} onChange={(e) => setKeywords(e.target.value)} placeholder="Ej: Frontend Developer React" />
            </label>
            <label className="input-wrap">
              <span>📍</span>
              <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Ej: Buenos Aires / Remoto" />
            </label>
            <button type="submit" disabled={loading}>{loading ? "Analizando... ⏳" : "Buscar matches ✨"}</button>
          </form>

          <div style={{ marginTop: '16px', textAlign: 'center' }}>
            <label style={{ display: 'inline-block', padding: '12px 20px', background: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.3)', borderRadius: '12px', cursor: 'pointer', transition: 'all 0.2s' }} className={uploadingCV ? 'disabled' : ''}>
              {uploadingCV ? '⏳ Cargando CV...' : cvLoaded ? '✅ CV cargado' : '📄 Subir mi CV (PDF)'}
              <input type="file" accept=".pdf" onChange={handleUploadCV} style={{ display: 'none' }} disabled={uploadingCV} />
            </label>
          </div>
          {!cvLoaded && (
            <p style={{ marginTop: '10px', opacity: '0.75', fontSize: '0.88rem', textAlign: 'center' }}>
              💡 Subí tu CV para obtener recomendaciones personalizadas
            </p>
          )}
          {error && <p className="warn">⚠️ {error}</p>}
        </section>

        <section className="results">
          <article className="panel">
            <h2 className="panel-title">🏆 Top oportunidades</h2>
            <div className="job-grid">
              {loading && Array.from({ length: 3 }).map((_, i) => <SkeletonCard key={i} />)}

              {!loading && topMatches.map((job, index) => (
                <div className="job-card" key={`${job.company}-${job.job_title}`}>
                  <h3>{index + 1}. {job.job_title}</h3>
                  <p className="muted">🏢 {job.company} · 👨‍💻 {job.seniority_level} · ⌛ {job.experience_required}</p>
                  <div className="chips">
                    {job.tech_skills.slice(0, 5).map((skill) => (
                      <span className="chip" key={skill}>⚙️ {skill}</span>
                    ))}
                  </div>
                  {job.description && (
                    <p className="muted" style={{ marginTop: '10px', fontSize: '0.85rem', lineHeight: '1.5' }}>
                      {job.description}
                    </p>
                  )}
                  {job.link && job.link !== '#' && (
                    <a href={job.link} target="_blank" rel="noopener noreferrer" style={{
                      display: 'inline-block',
                      marginTop: '10px',
                      padding: '8px 16px',
                      borderRadius: '10px',
                      background: 'linear-gradient(120deg, #67e8f9, #a5b4fc)',
                      color: '#041524',
                      fontWeight: '700',
                      fontSize: '0.85rem',
                      textDecoration: 'none'
                    }}>
                      Postularme →
                    </a>
                  )}
                </div>
              ))}

              {!loading && results && !topMatches.length && (
                <div style={{ textAlign: 'center', padding: '32px 16px' }}>
                  <div style={{ fontSize: '4rem', marginBottom: '12px' }}>🔍</div>
                  <h3 style={{ margin: '0 0 8px', fontSize: '1.1rem' }}>Sin resultados para "{keywords}"</h3>
                  <p className="muted" style={{ margin: '0 0 16px' }}>
                    No encontramos ofertas para ese rol en este momento.<br />
                    Probá con otro keyword o ubicación.
                  </p>
                  <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', flexWrap: 'wrap' }}>
                    {['Frontend Developer', 'React Developer', 'Full Stack'].map((s) => (
                      <span
                        key={s}
                        className="chip"
                        style={{ cursor: 'pointer' }}
                        onClick={() => setKeywords(s)}
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

            </div>
          </article>

          <article className="panel">
            <h2 className="panel-title">🎯 Match principal</h2>
            {loading ? (
              <>
                <div className="score-ring skeleton" style={{ marginBottom: 14 }} />
                <SkeletonCard />
              </>
            ) : results?.best_match ? (
              <>
                <CircularProgress score={results.best_match.match_score || 0} />
                <h3>{results.best_match.job_title}</h3>
                <p className="muted">💼 {results.best_match.company}</p>
                <div className="chips">
                  {(results.cv_optimization?.matching_skills || []).map((skill) => (
                    <span className="chip" key={skill}>✅ {skill}</span>
                  ))}
                  {(results.cv_optimization?.missing_skills || []).slice(0, 3).map((skill) => (
                    <span className="chip" key={skill}>🧩 {skill}</span>
                  ))}
                </div>
                <p className="muted" style={{ marginTop: 12 }}>
                  🧠 {results.cv_optimization?.recommendations || "Sin recomendaciones por ahora."}
                </p>
                <ul className="tips">
                  {quickTips.map((tip) => <li key={tip}>💡 {tip}</li>)}
                </ul>
              </>
            ) : (
              <p className="muted">Completa la búsqueda para calcular tu match score.</p>
            )}
          </article>
        </section>
      </main>
    </>
  );
}

export default App;