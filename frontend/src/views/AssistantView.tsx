import React, { useState, useEffect } from 'react';
import { AnalysisResult, AnalogCandidate, ScientificInsight } from '../types';
import { generateInsights, generateReport, getReportDownloadUrl } from '../api';
import { Sparkles, Download, Send, AlertTriangle, ShieldCheck, Truck, Wrench, Microscope, Compass } from 'lucide-react';

interface AssistantViewProps {
  analysisResult: AnalysisResult | null;
  candidate: AnalogCandidate | null;
  onBackToDiscovery: () => void;
}

export const AssistantView: React.FC<AssistantViewProps> = ({
  analysisResult,
  candidate,
  onBackToDiscovery,
}) => {
  const [insight, setInsight] = useState<ScientificInsight | null>(null);
  const [loadingInsight, setLoadingInsight] = useState<boolean>(false);
  const [downloadingReport, setDownloadingReport] = useState<boolean>(false);
  const [chatQuestion, setChatQuestion] = useState<string>('');
  const [chatHistory, setChatHistory] = useState<Array<{ sender: 'user' | 'assistant'; text: string }>>([]);
  const [chatLoading, setChatLoading] = useState<boolean>(false);

  const activeCand = candidate || (analysisResult?.candidates ? analysisResult.candidates[0] : null);

  useEffect(() => {
    let isMounted = true;
    const fetchInsights = async () => {
      if (!analysisResult || !activeCand) return;
      try {
        setLoadingInsight(true);
        const data = await generateInsights({
          analysis_id: analysisResult.analysis_id,
          candidate_id: activeCand.candidate_id,
        });
        if (isMounted) {
          setInsight(data);
        }
      } catch (err) {
        console.error('Failed to load insights:', err);
      } finally {
        if (isMounted) setLoadingInsight(false);
      }
    };

    fetchInsights();
    return () => { isMounted = false; };
  }, [analysisResult, activeCand]);

  const handleSendQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatQuestion.trim() || !analysisResult || !activeCand) return;

    const userText = chatQuestion.trim();
    setChatQuestion('');
    setChatHistory((prev) => [...prev, { sender: 'user', text: userText }]);

    try {
      setChatLoading(true);
      const res = await generateInsights({
        analysis_id: analysisResult.analysis_id,
        candidate_id: activeCand.candidate_id,
        question: userText,
      });

      setChatHistory((prev) => [...prev, { sender: 'assistant', text: res.response }]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { sender: 'assistant', text: 'Error contacting AI assistant. Please try again.' },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!analysisResult || !activeCand) return;
    try {
      setDownloadingReport(true);
      const rep = await generateReport({
        analysis_id: analysisResult.analysis_id,
        candidate_id: activeCand.candidate_id,
      });

      // Trigger browser download via direct URL
      const downloadLink = document.createElement('a');
      downloadLink.href = getReportDownloadUrl(rep.report_id);
      downloadLink.setAttribute('download', rep.filename);
      document.body.appendChild(downloadLink);
      downloadLink.click();
      downloadLink.remove();
    } catch (err) {
      console.error('Report compilation failed:', err);
      alert('PDF generation encountered an issue.');
    } finally {
      setDownloadingReport(false);
    }
  };

  if (!analysisResult || !activeCand) {
    return (
      <div className="glass-panel p-12 rounded-2xl text-center space-y-4 max-w-xl mx-auto my-12">
        <Sparkles size={40} className="text-sky-400 mx-auto" />
        <h2 className="text-lg font-bold text-white">No Candidate Selected</h2>
        <p className="text-xs text-slate-400">
          Run an analog discovery search and select an Earth analog to access AI mission analysis.
        </p>
        <button
          onClick={onBackToDiscovery}
          className="px-4 py-2 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-semibold hover:bg-sky-500/30 transition"
        >
          Return to Discovery
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner with Download Report Trigger */}
      <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs px-2 py-0.5 rounded bg-indigo-950 border border-indigo-800 text-indigo-300 font-mono">
              AI SCIENTIFIC RESEARCH ASSISTANT
            </span>
            <span className="text-xs text-slate-400">
              Grounded in LOLA, MOLA & SRTM Topographic Measurements
            </span>
          </div>
          <h1 className="text-lg font-bold text-white tracking-wide">
            Mission Readiness Assessment: {activeCand.name} ({activeCand.country})
          </h1>
          <p className="text-xs text-slate-400">
            Evaluating planetary suitability for {analysisResult.reference_name} ({analysisResult.reference_planet.toUpperCase()})
          </p>
        </div>

        <button
          onClick={handleDownloadReport}
          disabled={downloadingReport}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white text-xs font-semibold hover:opacity-90 transition flex items-center gap-2 shadow-lg disabled:opacity-60 cursor-pointer self-start md:self-auto"
        >
          {downloadingReport ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Compiling PDF Report...</span>
            </>
          ) : (
            <>
              <Download size={14} />
              <span>Download Scientific Report (PDF)</span>
            </>
          )}
        </button>
      </div>

      {/* Main Guidance Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Mission Domains (Rover, Drilling, Differences) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Executive Selection Rationale */}
          <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 space-y-2">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles size={16} className="text-sky-400" />
              Selection Rationale & Petrological Fit
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed">
              {insight?.why_selected || 'Generating grounded synthesis...'}
            </p>
          </div>

          {/* Rover Mobility & Traction Guidance */}
          <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 space-y-2">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <Truck size={16} className="text-sky-400" />
              Rover Mobility & Terramechanics Suitability
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed">
              {insight?.rover_mobility || 'Analyzing slope distributions and sub-meter rock obstacles...'}
            </p>
          </div>

          {/* Robotic Drilling & In-Situ Resource Utilization (ISRU) */}
          <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 space-y-2">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <Wrench size={16} className="text-indigo-400" />
              Robotic Drilling & Regolith Sampling Feasibility
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed">
              {insight?.drilling_isru || 'Evaluating mineral hardness and rotary-percussive penetration...'}
            </p>
          </div>

          {/* Environmental Disclaimers (Non-reproducible factors) */}
          <div className="glass-panel p-5 rounded-2xl border border-amber-900/40 bg-[#0e1017] space-y-2.5">
            <h2 className="text-sm font-bold text-amber-300 flex items-center gap-2">
              <AlertTriangle size={16} className="text-amber-400" />
              Non-Reproducible Planetary Differences (Critical Disclaimers)
            </h2>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {insight?.environmental_differences.map((diff, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-amber-400 font-bold">•</span>
                  <span>{diff}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Right Column: Interactive Research Chat Assistant */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col h-[600px]">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Microscope size={16} className="text-sky-400" />
                <h3 className="text-xs font-bold text-white tracking-wide">Interactive Research Queries</h3>
              </div>
              <span className="text-[10px] text-emerald-400 flex items-center gap-1 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                Ready
              </span>
            </div>

            {/* Quick Prompt Chips */}
            <div className="py-2.5 flex flex-wrap gap-1.5 border-b border-slate-800/60">
              {[
                'Is this site good for rover wheel testing?',
                'Can we test sample drilling here?',
                'What are the gravity differences?',
              ].map((prompt, i) => (
                <button
                  key={i}
                  onClick={() => setChatQuestion(prompt)}
                  className="text-[10px] px-2 py-1 rounded bg-slate-800/80 hover:bg-sky-500/20 text-slate-300 hover:text-sky-200 border border-slate-700/60 transition"
                >
                  {prompt}
                </button>
              ))}
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto py-3 space-y-3 pr-1 text-xs">
              <div className="bg-[#050811] p-3 rounded-xl border border-slate-800 text-slate-300 leading-relaxed">
                <p className="font-semibold text-sky-300 mb-1">TerraTwin Scientific Assistant</p>
                Ask questions regarding terramechanics, instrument calibration, mineralogical testing, or scientific limitations for this analog pairing.
              </div>

              {chatHistory.map((msg, i) => (
                <div
                  key={i}
                  className={`p-3 rounded-xl leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-sky-500/15 border border-sky-500/30 text-white ml-6'
                      : 'bg-[#050811] border border-slate-800 text-slate-200 mr-4'
                  }`}
                >
                  <p className="text-[10px] text-slate-400 mb-1 font-mono">
                    {msg.sender === 'user' ? 'Scientist' : 'TerraTwin Assistant'}
                  </p>
                  <div className="whitespace-pre-line text-xs">{msg.text}</div>
                </div>
              ))}

              {chatLoading && (
                <div className="p-3 bg-[#050811] rounded-xl border border-slate-800 text-slate-400 flex items-center gap-2">
                  <span className="w-3 h-3 border-2 border-sky-400 border-t-transparent rounded-full animate-spin" />
                  <span>Synthesizing scientific analysis...</span>
                </div>
              )}
            </div>

            {/* Query Input Form */}
            <form onSubmit={handleSendQuestion} className="pt-3 border-t border-slate-800 flex items-center gap-2">
              <input
                type="text"
                placeholder="Ask about terramechanics, instruments, or tests..."
                value={chatQuestion}
                onChange={(e) => setChatQuestion(e.target.value)}
                className="flex-1 bg-[#050811] border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
              <button
                type="submit"
                disabled={!chatQuestion.trim() || chatLoading}
                className="p-2 rounded-xl bg-sky-500 text-white hover:bg-sky-400 disabled:opacity-50 transition cursor-pointer"
              >
                <Send size={14} />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
