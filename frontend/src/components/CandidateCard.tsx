import React from 'react';
import { AnalogCandidate } from '../types';
import { Award, ArrowRight, Compass, ShieldCheck, Activity, Mountain, Flame, Layers } from 'lucide-react';

interface CandidateCardProps {
  candidate: AnalogCandidate;
  isSelected?: boolean;
  onSelect?: () => void;
  onCompare?: () => void;
  onViewAssistant?: () => void;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({
  candidate,
  isSelected = false,
  onSelect,
  onCompare,
  onViewAssistant,
}) => {
  const getScoreBadgeColor = (score: number) => {
    if (score >= 85) return 'text-emerald-400 bg-emerald-950/40 border-emerald-500/40';
    if (score >= 75) return 'text-sky-400 bg-sky-950/40 border-sky-500/40';
    return 'text-amber-400 bg-amber-950/40 border-amber-500/40';
  };

  return (
    <div
      onClick={onSelect}
      className={`glass-panel p-4 rounded-xl cursor-pointer transition-all duration-200 border ${
        isSelected
          ? 'border-sky-400 shadow-[0_0_20px_rgba(56,189,248,0.25)] bg-[#0e1628]'
          : 'border-slate-800/80 hover:border-sky-500/50 hover:bg-[#0b101e]'
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 text-xs font-mono font-bold text-sky-400">
            #{candidate.rank}
          </div>
          <div>
            <h3 className="font-semibold text-white text-sm tracking-wide">{candidate.name}</h3>
            <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
              <span>{candidate.country}</span>
              <span>•</span>
              <span className="font-mono text-[11px] text-slate-400">
                {candidate.latitude.toFixed(2)}°, {candidate.longitude.toFixed(2)}°
              </span>
            </p>
          </div>
        </div>

        {/* Overall Similarity Badge */}
        <div className={`px-2.5 py-1 rounded-md border text-xs font-mono font-bold flex items-center gap-1 ${getScoreBadgeColor(candidate.overall_similarity)}`}>
          <span>{candidate.overall_similarity}%</span>
          <span className="text-[10px] font-normal opacity-80">Match</span>
        </div>
      </div>

      {/* Component Scores Progress Bars */}
      <div className="grid grid-cols-4 gap-2 mt-3 pt-3 border-t border-slate-800/60">
        <div>
          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span className="flex items-center gap-1"><Mountain size={10} className="text-sky-400" /> Topo</span>
            <span className="font-mono text-sky-300">{candidate.components.topography_similarity.toFixed(0)}%</span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-sky-400 rounded-full" style={{ width: `${candidate.components.topography_similarity}%` }} />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span className="flex items-center gap-1"><Layers size={10} className="text-indigo-400" /> Geol</span>
            <span className="font-mono text-indigo-300">{candidate.components.geological_similarity.toFixed(0)}%</span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-400 rounded-full" style={{ width: `${candidate.components.geological_similarity}%` }} />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span className="flex items-center gap-1"><Flame size={10} className="text-orange-400" /> Therm</span>
            <span className="font-mono text-orange-300">{candidate.components.thermal_similarity.toFixed(0)}%</span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-orange-400 rounded-full" style={{ width: `${candidate.components.thermal_similarity}%` }} />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span className="flex items-center gap-1"><Activity size={10} className="text-emerald-400" /> Surf</span>
            <span className="font-mono text-emerald-300">{candidate.components.surface_similarity.toFixed(0)}%</span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${candidate.components.surface_similarity}%` }} />
          </div>
        </div>
      </div>

      {/* Key Alignments */}
      <div className="mt-3 flex flex-wrap gap-1.5">
        {candidate.strongest_matches.slice(0, 2).map((match, i) => (
          <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-sky-950/50 border border-sky-800/40 text-sky-300">
            ✓ {match}
          </span>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="mt-3.5 pt-2.5 border-t border-slate-800/60 flex items-center justify-between">
        <span className="text-[11px] text-slate-400 flex items-center gap-1">
          <ShieldCheck size={12} className="text-emerald-400" />
          {candidate.confidence_level}
        </span>

        <div className="flex items-center gap-2">
          {onCompare && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onCompare();
              }}
              className="text-xs px-2.5 py-1 rounded bg-sky-500/15 border border-sky-500/30 text-sky-300 hover:bg-sky-500/25 transition flex items-center gap-1"
            >
              <span>3D Compare</span>
              <ArrowRight size={12} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
