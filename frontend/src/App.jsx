import { useMemo, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const quickTips = [
  "Incluye verbos de impacto en tu experiencia.",
  "Destaca resultados medibles en cada proyecto.",
  "Adapta tu CV al stack tecnológico del rol.",
  "Prioriza skills clave en el primer tercio del CV.",
];

const scoreLabel = (score) => {
  if (score >= 85) return "MATCH EXCELENTE";
  if (score >= 70) return "MATCH SÓLIDO";
  return "BUEN POTENCIAL";
};

const CircularProgress = ({ score }) => {
  const circumference = 2 * Math.PI * 52;
  const offset = circumference - (score / 100) * circumference;
  return (
    <div className="score-wrap">
      <div className="score-svg-wrap">
        <svg width="136" height="136" viewBox="0 0 136 136">
          <circle cx="68" cy="68" r="52" fill="none" stroke="#0d1f0d" strokeWidth="8" />
          <circle
            cx="68" cy="68" r="52" fill="none"
            stroke="#00ff88" strokeWidth="8"
            strokeLinecap="butt"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            transform="rotate(-90 68 68)"
            style={{ transition: 'stroke-dashoffset 1.2s ease', filter: 'drop-shadow(0 0 8px #00ff88)' }}
          />
        </svg>
        <div className="score-inner">
          <strong>{score}</strong>
          <span>/100</span>
        </div>
      </div>
      <p className="score-label">{scoreLabel(score)}</p>
    </div>
  );
};

const SkeletonCard = () => (
  <div className="job-card skeleton">
    <div className="sk-line w-60" />
    <div className="sk-line w-40" />
    <div className="sk-grid">
      <div className="sk-pill" /><div className="sk-pill" /><div className="sk-pill" />
    </div>
    <div className="sk-line w-90" />
  </div>
);

function App() {
  const [keywords, setKeywords] = useState("");
  const [location, setLocation] = useState("");
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
      if (!response.ok) throw new Error("No se pudo conectar al backend.");
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
    formData.append("file", file);
    try {
      const response = await fetch(`${API_BASE_URL}/api/upload-cv`, { method: "POST", body: formData });
      const data = await response.json();
      if (data.success) setCvLoaded(true);
    } catch (err) {
      console.error(err);
    } finally {
      setUploadingCV(false);
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
          --bg: #080c08;
          --bg1: #0d120d;
          --bg2: #111811;
          --bg3: #161e16;
          --green: #00ff88;
          --green-dim: #00cc6a;
          --green-dark: #003d1f;
          --green-glow: rgba(0,255,136,0.15);
          --text: #c8e6c8;
          --text-muted: #5a7a5a;
          --text-dim: #3a5a3a;
          --border: #1a2e1a;
          --border-bright: #2a4a2a;
          --mono: 'JetBrains Mono', monospace;
          --sans: 'Inter', sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: var(--sans);
          background: var(--bg);
          color: var(--text);
          min-height: 100vh;
          background-image:
            radial-gradient(ellipse at 20% 0%, rgba(0,255,136,0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, rgba(0,255,136,0.03) 0%, transparent 50%);
        }

        body::before {
          content: '';
          position: fixed;
          inset: 0;
          background: repeating-linear-gradient(
            0deg, transparent, transparent 2px,
            rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
          );
          pointer-events: none;
          z-index: 9999;
        }

        .app { max-width: 1100px; margin: 0 auto; padding: 0 20px 80px; }

        .header {
          padding: 32px 0 24px;
          margin-bottom: 32px;
          border-bottom: 1px solid var(--border-bright);
          animation: fadeUp .5s ease both;
        }
        .header-top { display: flex; align-items: center; gap: 16px; margin-bottom: 6px; }
        .header-prompt { font-family: var(--mono); font-size: 0.75rem; color: var(--green); opacity: 0.6; }
        .header-logo {
          font-family: var(--mono);
          font-size: clamp(1.8rem, 3.5vw, 2.8rem);
          font-weight: 700;
          color: var(--green);
          letter-spacing: -0.03em;
          text-shadow: 0 0 30px rgba(0,255,136,0.4);
        }
        .header-logo span { color: var(--text); font-weight: 300; }
        .header-badge {
          font-family: var(--mono);
          font-size: 0.65rem;
          color: var(--green);
          border: 1px solid var(--green-dark);
          padding: 3px 8px;
          border-radius: 3px;
          background: rgba(0,255,136,0.05);
          letter-spacing: 0.1em;
        }
        .header-sub { font-family: var(--mono); font-size: 0.78rem; color: var(--text-muted); }
        .cursor {
          display: inline-block; width: 8px; height: 14px;
          background: var(--green); margin-left: 4px;
          vertical-align: middle; animation: blink 1.1s step-end infinite;
        }

        .search-panel {
          background: var(--bg1);
          border: 1px solid var(--border-bright);
          border-radius: 12px;
          padding: 24px;
          margin-bottom: 24px;
          animation: fadeUp .5s .1s ease both;
          position: relative;
          overflow: hidden;
        }
        .search-panel::before {
          content: '';
          position: absolute; top: 0; left: 0; right: 0; height: 1px;
          background: linear-gradient(90deg, transparent, var(--green), transparent);
          opacity: 0.4;
        }
        .search-row { display: grid; grid-template-columns: 2fr 1.5fr auto; gap: 10px; margin-bottom: 14px; }
        .input-wrap {
          display: flex; align-items: center; gap: 10px;
          background: var(--bg2); border: 1px solid var(--border-bright);
          border-radius: 8px; padding: 0 14px; transition: border-color .2s;
        }
        .input-wrap:focus-within { border-color: var(--green); box-shadow: 0 0 0 3px var(--green-glow); }
        .input-icon { font-family: var(--mono); color: var(--green); font-size: 0.9rem; flex-shrink: 0; opacity: 0.7; }
        input {
          width: 100%; border: none; background: transparent; outline: none;
          color: var(--text); padding: 13px 0; font-size: 0.9rem; font-family: var(--mono);
        }
        input::placeholder { color: var(--text-dim); font-size: 0.85rem; }

        .btn-search {
          border: 1px solid var(--green); border-radius: 8px; padding: 0 22px;
          font-family: var(--mono); font-size: 0.85rem; font-weight: 700;
          color: var(--bg); background: var(--green); cursor: pointer;
          transition: all .2s; letter-spacing: 0.05em; white-space: nowrap;
        }
        .btn-search:hover { background: var(--green-dim); box-shadow: 0 0 20px rgba(0,255,136,0.3); }
        .btn-search:disabled { opacity: .5; cursor: wait; }

        .cv-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
        .btn-cv {
          display: inline-flex; align-items: center; gap: 8px;
          padding: 9px 16px; border: 1px solid var(--border-bright);
          border-radius: 8px; background: transparent; color: var(--text-muted);
          font-size: 0.8rem; font-family: var(--mono); cursor: pointer; transition: all .2s;
        }
        .btn-cv:hover { border-color: var(--green); color: var(--green); background: var(--green-glow); }
        .btn-cv.loaded { border-color: var(--green); color: var(--green); background: rgba(0,255,136,0.08); }
        .cv-hint { font-family: var(--mono); font-size: 0.75rem; color: var(--text-dim); }

        .warn {
          margin-top: 12px; font-family: var(--mono); font-size: 0.8rem;
          color: #ffcc44; background: rgba(255,204,68,0.08);
          border: 1px solid rgba(255,204,68,0.25); border-radius: 6px; padding: 10px 14px;
        }

        .results { display: grid; grid-template-columns: 1.3fr 1fr; gap: 16px; align-items: start; animation: fadeUp .5s .2s ease both; }

        .panel { background: var(--bg1); border: 1px solid var(--border-bright); border-radius: 12px; overflow: hidden; }
        .panel-header {
          padding: 14px 18px; border-bottom: 1px solid var(--border);
          display: flex; align-items: center; gap: 10px;
        }
        .panel-header h2 {
          font-family: var(--mono); font-size: 0.8rem; font-weight: 700;
          letter-spacing: 0.1em; color: var(--green); text-transform: uppercase;
        }
        .panel-count {
          margin-left: auto; font-family: var(--mono); font-size: 0.7rem;
          color: var(--text-muted); background: var(--bg3); padding: 2px 8px; border-radius: 4px;
        }
        .panel-body { padding: 14px; }
        .job-grid { display: grid; gap: 10px; }

        .job-card {
          border: 1px solid var(--border); border-radius: 10px; padding: 14px;
          background: var(--bg2); transition: border-color .2s, box-shadow .2s; position: relative;
        }
        .job-card:hover {
          border-color: var(--green-dark);
          box-shadow: 0 0 20px rgba(0,255,136,0.06), inset 0 0 20px rgba(0,255,136,0.02);
        }
        .job-number { position: absolute; top: 10px; right: 12px; font-family: var(--mono); font-size: 0.65rem; color: var(--text-dim); }
        .job-card h3 { font-size: 0.9rem; font-weight: 600; margin-bottom: 5px; padding-right: 36px; color: var(--text); line-height: 1.4; }
        .job-meta { font-family: var(--mono); font-size: 0.72rem; color: var(--text-muted); margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 8px; }
        .chips { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
        .chip {
          font-family: var(--mono); font-size: .68rem; border-radius: 4px; padding: 3px 8px;
          background: var(--green-dark); color: var(--green); border: 1px solid rgba(0,255,136,0.15);
        }
        .chip.match { background: rgba(0,255,136,0.12); color: var(--green); border-color: rgba(0,255,136,0.3); }
        .chip.missing { background: rgba(100,100,255,0.1); color: #8888ff; border-color: rgba(100,100,255,0.2); }

        .job-desc { font-size: 0.78rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .btn-apply {
          display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px;
          border-radius: 6px; border: 1px solid var(--border-bright); background: var(--bg3);
          color: var(--green); font-family: var(--mono); font-size: 0.75rem; font-weight: 700;
          text-decoration: none; transition: all .2s; letter-spacing: 0.05em;
        }
        .btn-apply:hover { border-color: var(--green); background: var(--green-dark); box-shadow: 0 0 12px rgba(0,255,136,0.2); }

        .score-wrap { text-align: center; padding: 10px 0 16px; }
        .score-svg-wrap { position: relative; width: 136px; height: 136px; margin: 0 auto 8px; }
        .score-inner { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .score-inner strong { font-family: var(--mono); font-size: 2.2rem; font-weight: 700; color: var(--green); text-shadow: 0 0 20px rgba(0,255,136,0.5); line-height: 1; }
        .score-inner span { font-family: var(--mono); font-size: 0.7rem; color: var(--text-muted); }
        .score-label { font-family: var(--mono); font-size: 0.7rem; font-weight: 700; color: var(--green); letter-spacing: 0.1em; opacity: 0.8; }

        .match-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 3px; }
        .match-company { font-family: var(--mono); font-size: 0.78rem; color: var(--text-muted); margin-bottom: 12px; }
        .recommendations { font-size: 0.8rem; color: var(--text-muted); line-height: 1.6; margin-top: 10px; padding: 12px; background: var(--bg2); border-radius: 8px; border-left: 2px solid var(--green); }
        .tips { list-style: none; margin-top: 14px; display: grid; gap: 6px; }
        .tips li { font-size: 0.78rem; color: var(--text-muted); padding: 8px 12px; background: var(--bg2); border-radius: 6px; border-left: 2px solid var(--border-bright); font-family: var(--mono); }
        .tips li::before { content: '> '; color: var(--green); opacity: 0.6; }

        .empty-state { text-align: center; padding: 40px 16px; }
        .empty-icon { font-family: var(--mono); font-size: 2rem; color: var(--text-dim); margin-bottom: 12px; }
        .empty-state h3 { font-family: var(--mono); font-size: 0.9rem; color: var(--text-muted); margin-bottom: 8px; }
        .empty-state p { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 14px; font-family: var(--mono); }
        .empty-chips { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
        .empty-chip { font-family: var(--mono); font-size: 0.75rem; padding: 6px 12px; border: 1px solid var(--border-bright); border-radius: 6px; cursor: pointer; color: var(--text-muted); transition: all .2s; }
        .empty-chip:hover { border-color: var(--green); color: var(--green); background: var(--green-glow); }

        .initial-state { text-align: center; padding: 40px 16px; font-family: var(--mono); font-size: 0.8rem; color: var(--text-dim); }

        .skeleton { pointer-events: none; }
        .sk-line, .sk-pill { border-radius: 4px; background: linear-gradient(90deg, var(--bg2), var(--bg3), var(--bg2)); background-size: 220% 100%; animation: shine 1.4s linear infinite; }
        .sk-line { height: 12px; margin-bottom: 10px; }
        .w-60 { width: 60%; } .w-40 { width: 40%; } .w-90 { width: 90%; }
        .sk-grid { display: flex; gap: 8px; margin-bottom: 10px; }
        .sk-pill { width: 64px; height: 20px; border-radius: 4px; }

        @media (max-width: 900px) { .results { grid-template-columns: 1fr; } }
        @media (max-width: 640px) { .search-row { grid-template-columns: 1fr; } .btn-search { height: 46px; } }

        @keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes shine { 0% { background-position: 200% 0; } 100% { background-position: -40% 0; } }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
      `}</style>

      <main className="app">
        <header className="header">
          <div className="header-top">
            <span className="header-prompt">~/job-search $</span>
            <h1 className="header-logo">job<span>assistant</span>.ai</h1>
            <span className="header-badge">v2.0 · MULTI-AGENT</span>
          </div>
          <p className="header-sub">
            Tu próximo trabajo ya existe. Solo falta encontrarlo antes que los demás.
            <span className="cursor" />
          </p>
        </header>

        <section className="search-panel">
          <form onSubmit={runPipeline}>
            <div className="search-row">
              <label className="input-wrap">
                <span className="input-icon">_</span>
                <input value={keywords} onChange={(e) => setKeywords(e.target.value)} placeholder="rol · ej: frontend developer react" />
              </label>
              <label className="input-wrap">
                <span className="input-icon">@</span>
                <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="ubicación · ej: brasil" />
              </label>
              <button className="btn-search" type="submit" disabled={loading}>
                {loading ? "RUNNING..." : "EXEC →"}
              </button>
            </div>
          </form>
          <div className="cv-row">
            <label className={`btn-cv ${cvLoaded ? "loaded" : ""}`}>
              {uploadingCV ? "[ LOADING... ]" : cvLoaded ? "[ ✓ CV LOADED ]" : "[ + UPLOAD CV ]"}
              <input type="file" accept=".pdf" onChange={handleUploadCV} style={{ display: "none" }} disabled={uploadingCV} />
            </label>
            {!cvLoaded && <span className="cv-hint">// subí tu CV para recomendaciones personalizadas</span>}
          </div>
          {error && <p className="warn">// ERROR: {error}</p>}
        </section>

        <section className="results">
          <article className="panel">
            <div className="panel-header">
              <h2>// Oportunidades</h2>
              {topMatches.length > 0 && <span className="panel-count">{topMatches.length} results</span>}
            </div>
            <div className="panel-body">
              <div className="job-grid">
                {loading && Array.from({ length: 3 }).map((_, i) => <SkeletonCard key={i} />)}
                {!loading && topMatches.map((job, index) => (
                  <div className="job-card" key={`${job.company}-${job.job_title}-${index}`}>
                    <span className="job-number">[{String(index + 1).padStart(2, '0')}]</span>
                    <h3>{job.job_title}</h3>
                    <div className="job-meta">
                      <span>{job.company}</span>
                      <span>· {job.seniority_level}</span>
                      <span>· {job.experience_required}</span>
                    </div>
                    <div className="chips">
                      {job.tech_skills.slice(0, 5).map((skill) => (
                        <span className="chip" key={skill}>{skill}</span>
                      ))}
                    </div>
                    {job.description && <p className="job-desc">{job.description}</p>}
                    {job.link && job.link !== "#" && (
                      <a href={job.link} target="_blank" rel="noopener noreferrer" className="btn-apply">APPLY →</a>
                    )}
                  </div>
                ))}
                {!loading && results && !topMatches.length && (
                  <div className="empty-state">
                    <div className="empty-icon">[ 0 results ]</div>
                    <h3>NULL — sin resultados para "{keywords}"</h3>
                    <p>// probá con otro keyword</p>
                    <div className="empty-chips">
                      {["Frontend Developer", "React Developer", "Full Stack"].map((s) => (
                        <span key={s} className="empty-chip" onClick={() => setKeywords(s)}>{s}</span>
                      ))}
                    </div>
                  </div>
                )}
                {!loading && !results && (
                  <p className="initial-state">// iniciá una búsqueda para ver oportunidades</p>
                )}
              </div>
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <h2>// Match Score</h2>
            </div>
            <div className="panel-body">
              {loading ? (
                <><SkeletonCard /><SkeletonCard /></>
              ) : results?.best_match ? (
                <>
                  <CircularProgress score={results.best_match.match_score || 0} />
                  <h3 className="match-title">{results.best_match.job_title}</h3>
                  <p className="match-company">{results.best_match.company}</p>
                  <div className="chips">
                    {(results.cv_optimization?.matching_skills || []).map((skill) => (
                      <span className="chip match" key={skill}>✓ {skill}</span>
                    ))}
                    {(results.cv_optimization?.missing_skills || []).slice(0, 3).map((skill) => (
                      <span className="chip missing" key={skill}>+ {skill}</span>
                    ))}
                  </div>
                  {results.cv_optimization?.recommendations && (
                    <p className="recommendations">{results.cv_optimization.recommendations}</p>
                  )}
                  <ul className="tips">
                    {quickTips.map((tip) => <li key={tip}>{tip}</li>)}
                  </ul>
                </>
              ) : (
                <p className="initial-state">// completá la búsqueda para ver tu match score</p>
              )}
            </div>
          </article>
        </section>
      </main>
    </>
  );
}

export default App;