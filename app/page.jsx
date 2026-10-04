'use client';

import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const INDUSTRIES = [
  'E-Commerce', 'FinTech', 'EdTech', 'SaaS', 'HealthTech',
  'Electric Vehicles', 'Cybersecurity', 'Renewable Energy', 'Retail', 'Logistics',
];

const PIPELINE_STEPS = [
  { id: 'scout',     label: 'Market Scout',               desc: 'Searches the web for new entrants, pricing & launches', icon: '🔍' },
  { id: 'synthesis', label: 'Intelligence Synthesizer',   desc: 'Builds comparison matrix & identifies opportunities',    icon: '🧠' },
  { id: 'swot',      label: 'Strategy Consultant — SWOT', desc: 'Writes executive SWOT analysis',                         icon: '📊' },
  { id: 'brief',     label: 'Strategy Consultant — Brief',desc: 'Drafts actionable go-to-market brief',                   icon: '📋' },
];

// Rough per-step durations (seconds) used for visual progress only
const STEP_DURATIONS = [60, 45, 35, 35];

export default function Home() {
  const [industry, setIndustry]     = useState('SaaS');
  const [status, setStatus]         = useState('idle');   // idle | running | done | error
  const [results, setResults]       = useState(null);
  const [activeTab, setActiveTab]   = useState('swot');
  const [error, setError]           = useState(null);
  const [currentStep, setCurrentStep] = useState(-1);
  const [elapsed, setElapsed]       = useState(0);

  // Elapsed timer
  useEffect(() => {
    if (status !== 'running') return;
    const id = setInterval(() => setElapsed(s => s + 1), 1000);
    return () => clearInterval(id);
  }, [status]);

  // Visual step progression based on approximate durations
  useEffect(() => {
    if (status !== 'running') return;
    setCurrentStep(0);
    const timeouts = [];
    let acc = 0;
    STEP_DURATIONS.forEach((dur, i) => {
      if (i === 0) return;
      acc += STEP_DURATIONS[i - 1];
      timeouts.push(setTimeout(() => setCurrentStep(i), acc * 1000));
    });
    return () => timeouts.forEach(clearTimeout);
  }, [status]);

  const handleRun = async () => {
    setStatus('running');
    setResults(null);
    setError(null);
    setElapsed(0);
    setCurrentStep(0);

    try {
      const res = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ industry }),
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'Research failed');
      setResults(data);
      setStatus('done');
    } catch (err) {
      setError(err.message);
      setStatus('error');
    } finally {
      setCurrentStep(-1);
    }
  };

  const download = (content, filename) => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  };

  const fmt = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  return (
    <main className="min-h-screen bg-[#06060f] text-slate-100">

      {/* ── Nav ── */}
      <nav className="fixed inset-x-0 top-0 z-50 border-b border-white/[0.06] bg-[#06060f]/80 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-5xl items-center gap-3 px-6">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 text-xs">
            🔍
          </div>
          <span className="text-sm font-semibold tracking-tight text-white">Market Intelligence</span>
          <div className="ml-auto flex items-center gap-2">
            <span className="rounded-full border border-violet-500/30 bg-violet-500/10 px-2 py-0.5 text-[11px] text-violet-300">
              Powered by CrewAI
            </span>
          </div>
        </div>
      </nav>

      <div className="pt-14">

        {/* ── Hero ── */}
        <div className="mx-auto max-w-5xl px-6 pb-12 pt-20 text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-400">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            4-agent AI crew ready
          </div>
          <h1 className="mb-4 text-6xl font-bold tracking-tight">
            <span className="bg-gradient-to-br from-white via-slate-200 to-slate-500 bg-clip-text text-transparent">
              B2B Competitive
            </span>
            <br />
            <span className="bg-gradient-to-r from-violet-400 via-indigo-400 to-violet-400 bg-clip-text text-transparent">
              Intelligence
            </span>
          </h1>
          <p className="mx-auto max-w-lg text-lg leading-relaxed text-slate-400">
            A crew of AI agents researches, synthesises, and generates a strategic
            intelligence report for any industry.
          </p>
        </div>

        <div className="mx-auto max-w-3xl space-y-5 px-6 pb-24">

          {/* ── Control card ── */}
          <div className="rounded-2xl border border-white/[0.08] bg-[#0d0d1f] p-6">
            <label className="mb-3 block text-xs font-medium uppercase tracking-widest text-slate-400">
              Select Industry
            </label>
            <div className="flex gap-3">
              <div className="relative flex-1">
                <select
                  value={industry}
                  onChange={e => setIndustry(e.target.value)}
                  disabled={status === 'running'}
                  className="w-full appearance-none rounded-xl border border-white/[0.08] bg-[#161630] px-4 py-3 pr-9 text-sm text-white transition-all focus:border-violet-500/60 focus:outline-none focus:ring-2 focus:ring-violet-500/20 disabled:opacity-40"
                >
                  {INDUSTRIES.map(ind => <option key={ind} value={ind}>{ind}</option>)}
                </select>
                <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-500">▾</span>
              </div>
              <button
                onClick={handleRun}
                disabled={status === 'running'}
                className="whitespace-nowrap rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-900/40 transition-all hover:from-violet-500 hover:to-indigo-500 active:scale-95 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {status === 'running' ? (
                  <span className="flex items-center gap-2">
                    <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Running…
                  </span>
                ) : '🚀 Run Research'}
              </button>
            </div>
          </div>

          {/* ── Pipeline progress ── */}
          {(status === 'running' || status === 'done') && (
            <div className="rounded-2xl border border-white/[0.08] bg-[#0d0d1f] p-6">
              <div className="mb-5 flex items-center justify-between">
                <h2 className="text-xs font-medium uppercase tracking-widest text-slate-400">Agent Pipeline</h2>
                {status === 'running' && (
                  <span className="tabular-nums text-xs text-slate-500">{fmt(elapsed)}</span>
                )}
                {status === 'done' && (
                  <span className="text-xs font-medium text-emerald-400">✓ Complete</span>
                )}
              </div>

              <div className="space-y-2">
                {PIPELINE_STEPS.map((step, i) => {
                  const isDone   = status === 'done' || (status === 'running' && i < currentStep);
                  const isActive = status === 'running' && i === currentStep;

                  return (
                    <div
                      key={step.id}
                      className={`flex items-center gap-4 rounded-xl p-3 transition-all ${
                        isActive ? 'border border-violet-500/25 bg-violet-500/10' :
                        isDone   ? 'border border-emerald-500/15 bg-emerald-500/5' :
                                   'border border-transparent'
                      }`}
                    >
                      <div className={`flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg text-base transition-all ${
                        isDone   ? 'border border-emerald-500/30 bg-emerald-500/20' :
                        isActive ? 'border border-violet-500/40 bg-violet-500/20' :
                                   'border border-white/[0.06] bg-white/[0.04]'
                      }`}>
                        {isDone ? '✓' : step.icon}
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className={`text-sm font-medium ${
                          isDone ? 'text-emerald-400' : isActive ? 'text-violet-300' : 'text-slate-600'
                        }`}>
                          {step.label}
                        </p>
                        <p className="truncate text-xs text-slate-600">{step.desc}</p>
                      </div>
                      {isActive && (
                        <div className="flex flex-shrink-0 gap-1">
                          {[0, 1, 2].map(j => (
                            <span
                              key={j}
                              className="h-1.5 w-1.5 animate-bounce rounded-full bg-violet-400"
                              style={{ animationDelay: `${j * 0.15}s` }}
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {status === 'running' && (
                <p className="mt-4 text-center text-xs text-slate-600">Research typically takes 2–4 minutes</p>
              )}
            </div>
          )}

          {/* ── Error ── */}
          {error && (
            <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-5 text-sm text-red-400">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* ── Results ── */}
          {results && (
            <div className="overflow-hidden rounded-2xl border border-white/[0.08] bg-[#0d0d1f]">
              {/* Tab bar */}
              <div className="flex items-center border-b border-white/[0.06]">
                {[
                  { id: 'swot',  label: '📊 SWOT Analysis'   },
                  { id: 'brief', label: '📋 Actionable Brief' },
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-5 py-3.5 text-sm font-medium transition-all ${
                      activeTab === tab.id
                        ? 'border-b-2 border-violet-500 text-white'
                        : 'text-slate-500 hover:text-slate-300'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
                <div className="flex-1" />
                <button
                  onClick={() => download(
                    activeTab === 'swot' ? results.swot : results.brief,
                    `${activeTab}_${industry.toLowerCase().replace(/ /g, '_')}.md`,
                  )}
                  className="mx-4 flex items-center gap-1.5 rounded-lg border border-white/10 px-3 py-1.5 text-xs text-slate-400 transition-all hover:border-white/20 hover:text-white"
                >
                  ⬇ Download .md
                </button>
              </div>

              {/* Markdown content */}
              <div className="p-8 prose prose-invert prose-sm max-w-none
                prose-headings:font-semibold prose-headings:text-white
                prose-h1:text-2xl prose-h1:mb-4
                prose-h2:text-lg prose-h2:mt-6 prose-h2:mb-3 prose-h2:text-slate-200
                prose-p:text-slate-400 prose-p:leading-relaxed
                prose-li:text-slate-400
                prose-strong:text-slate-200
                prose-table:text-xs prose-td:text-slate-400 prose-th:text-slate-300
                prose-th:bg-white/5 prose-td:border-white/10 prose-th:border-white/10">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {activeTab === 'swot' ? results.swot : results.brief}
                </ReactMarkdown>
              </div>
            </div>
          )}

        </div>
      </div>
    </main>
  );
}
