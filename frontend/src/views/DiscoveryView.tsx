import React, { useState } from 'react';
import { AnalysisResult, AnalogCandidate } from '../types';
import { CandidateCard } from '../components/CandidateCard';
import { CesiumEarth } from '../components/CesiumEarth';
import { Compass, Filter, Sparkles, GitCompare, ArrowLeft, Download, ShieldCheck, MapPin } from 'lucide-react';

interface DiscoveryViewProps {
  analysisResult: AnalysisResult | null;
  selectedCandidate: AnalogCandidate | null;
  setSelectedCandidate: (cand: AnalogCandidate | null) => void;
  onLaunchComparison: (cand: AnalogCandidate) => void;
  onLaunchAssistant: (cand: AnalogCandidate) => void;
  onBackToExplorer: () => void;
  onFilterByContinent?: (continent: string) => void;
}

const COUNTRY_TO_CONTINENT: Record<string, string> = {
  'india': 'Asia',
  'iran': 'Asia',
  'mongolia': 'Asia',
  'saudi arabia': 'Asia',
  'china': 'Asia',
  'russia': 'Asia',
  'nepal': 'Asia',
  'chad': 'Africa',
  'ethiopia': 'Africa',
  'namibia': 'Africa',
  'algeria': 'Africa',
  'south africa': 'Africa',
  'mauritania': 'Africa',
  'tanzania': 'Africa',
  'niger': 'Africa',
  'antarctica': 'Antarctica',
  'iceland': 'Europe',
  'norway': 'Europe',
  'spain': 'Europe',
  'germany': 'Europe',
  'italy': 'Europe',
  'united states': 'North America',
  'canada': 'North America',
  'chile': 'South America',
  'bolivia': 'South America',
  'argentina': 'South America',
  'australia': 'Oceania',
};

export const DiscoveryView: React.FC<DiscoveryViewProps> = ({
  analysisResult,
  selectedCandidate,
  setSelectedCandidate,
  onLaunchComparison,
  onLaunchAssistant,
  onBackToExplorer,
  onFilterByContinent,
}) => {
  const [filterType, setFilterType] = useState<string>('all');
  const [continentFilter, setContinentFilter] = useState<string>('all');

  if (!analysisResult) {
    return (
      <div className="glass-panel p-12 rounded-2xl text-center space-y-4 max-w-xl mx-auto my-12">
        <Compass size={40} className="text-sky-400 mx-auto animate-spin" />
        <h2 className="text-lg font-bold text-white">No Active Analog Discovery</h2>
        <p className="text-xs text-slate-400">
          Select a region on the Moon or Mars in the Planet Explorer to initiate scientific matching.
        </p>
        <button
          onClick={onBackToExplorer}
          className="px-4 py-2 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-semibold hover:bg-sky-500/30 transition"
        >
          Return to Explorer
        </button>
      </div>
    );
  }

  const handleContinentChange = (newContinent: string) => {
    setContinentFilter(newContinent);
    if (onFilterByContinent) {
      onFilterByContinent(newContinent);
    }
  };

  const filteredCandidates = analysisResult.candidates.filter((cand) => {
    const matchesLithology = filterType === 'all' || cand.features.geology.lithology_category.toLowerCase().includes(filterType.toLowerCase());
    const candContinent = cand.continent || COUNTRY_TO_CONTINENT[cand.country?.toLowerCase()] || '';
    const matchesContinent = continentFilter === 'all' ||
      candContinent.toLowerCase() === continentFilter.toLowerCase() ||
      (cand.country && cand.country.toLowerCase().includes(continentFilter.toLowerCase()));
    return matchesLithology && matchesContinent;
  });

  const activeCand = selectedCandidate || filteredCandidates[0] || analysisResult.candidates[0];

  return (
    <div className="space-y-6">
      {/* Telemetry Status Banner */}
      <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col gap-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <button
                onClick={onBackToExplorer}
                className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition mr-1"
                title="Back to Explorer"
              >
                <ArrowLeft size={16} />
              </button>
              <span className="text-xs px-2 py-0.5 rounded bg-sky-950 border border-sky-800 text-sky-300 font-mono">
                ANALYSIS COMPLETE
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-indigo-950 border border-indigo-800 text-indigo-300 font-mono">
                {analysisResult.database_mode === 'benchmark_catalog' ? 'BENCHMARK SITES' : 'GLOBAL R*TREE DATABASE'}
              </span>
              {analysisResult.diversity_balanced && (
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-800 text-emerald-300 font-mono">
                  DIVERSITY BALANCED
                </span>
              )}
              <span className="text-xs text-slate-400">
                Evaluated {analysisResult.total_candidates_searched} candidates in {analysisResult.computation_time_ms} ms
              </span>
            </div>
            <h1 className="text-lg font-bold text-white tracking-wide">
              Earth Analogs for {analysisResult.reference_name} ({analysisResult.reference_planet.toUpperCase()})
            </h1>
            <p className="text-xs text-slate-400 mt-0.5">{analysisResult.scientific_summary}</p>
            {analysisResult.continents_represented && analysisResult.continents_represented.length > 0 && (
              <div className="flex items-center gap-1.5 mt-2 text-[11px] text-slate-400">
                <span className="text-slate-500">Continents represented:</span>
                {analysisResult.continents_represented.map((c) => (
                  <span key={c} className="px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-300 font-mono text-[10px]">
                    {c}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-800/80">
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
            <Filter size={14} className="text-slate-400 mr-1" />
            {[
              { id: 'all', label: 'All Environments' },
              { id: 'volcanic', label: 'Volcanic Basalts' },
              { id: 'evaporite', label: 'Playas / Salars' },
              { id: 'permafrost', label: 'Polar Cryo' },
              { id: 'breccia', label: 'Impact Structures' },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setFilterType(f.id)}
                className={`text-xs px-2.5 py-1 rounded-lg border transition whitespace-nowrap ${
                  filterType === f.id
                    ? 'bg-sky-500/20 text-sky-300 border-sky-500/50 font-medium'
                    : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:text-slate-200'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Continent:</span>
            <select
              value={continentFilter}
              onChange={(e) => handleContinentChange(e.target.value)}
              className="bg-[#050811] text-slate-200 text-xs px-2 py-1 rounded-lg border border-slate-800 focus:outline-none focus:border-sky-500"
            >
              <option value="all">All Continents</option>
              <option value="Africa">Africa</option>
              <option value="Antarctica">Antarctica</option>
              <option value="Asia">Asia</option>
              <option value="Europe">Europe</option>
              <option value="North America">North America</option>
              <option value="South America">South America</option>
              <option value="Oceania">Oceania</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Split Layout: Ranked Candidates List & Interactive Earth Globe */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Ranked Candidate Cards */}
        <div className="lg:col-span-5 flex flex-col gap-3.5 max-h-[720px] overflow-y-auto pr-1">
          {filteredCandidates.map((cand) => (
            <CandidateCard
              key={cand.candidate_id}
              candidate={cand}
              isSelected={activeCand?.candidate_id === cand.candidate_id}
              onSelect={() => setSelectedCandidate(cand)}
              onCompare={() => onLaunchComparison(cand)}
              onViewAssistant={() => onLaunchAssistant(cand)}
            />
          ))}

          {filteredCandidates.length === 0 && (
            <div className="glass-panel p-8 text-center text-xs text-slate-400 space-y-2">
              <p>No candidates match the selected environment or continent filters.</p>
              <button
                type="button"
                onClick={() => { setFilterType('all'); setContinentFilter('all'); }}
                className="px-3 py-1 bg-sky-950 border border-sky-800 text-sky-300 rounded text-xs hover:bg-sky-900 transition"
              >
                Reset Filters
              </button>
            </div>
          )}
        </div>

        {/* Right: Earth Globe Display with Candidate Pins */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <CesiumEarth
            candidates={filteredCandidates}
            selectedCandidateId={activeCand?.candidate_id}
            onSelectCandidate={(cand) => setSelectedCandidate(cand)}
            height="520px"
          />

          {/* Active Candidate Detailed Strip */}
          {activeCand && (
            <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-white">{activeCand.name}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-950/60 border border-emerald-500/40 text-emerald-400 font-mono font-bold">
                    {activeCand.overall_similarity}% Overall Match
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2">{activeCand.geological_context}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => onLaunchComparison(activeCand)}
                  className="px-3.5 py-2 rounded-xl bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-semibold hover:bg-sky-500/30 transition flex items-center gap-1.5 whitespace-nowrap"
                >
                  <GitCompare size={14} />
                  <span>3D Compare</span>
                </button>

                <button
                  onClick={() => onLaunchAssistant(activeCand)}
                  className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-sky-600 text-white text-xs font-semibold hover:opacity-90 transition flex items-center gap-1.5 whitespace-nowrap shadow-md"
                >
                  <Sparkles size={14} />
                  <span>AI Insights & Report</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
