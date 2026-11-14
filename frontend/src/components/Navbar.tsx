import React from 'react';
import { Globe, Compass, GitCompare, Sparkles, BookOpen, Orbit } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  activePlanet: 'earth' | 'moon' | 'mars';
  setActivePlanet: (planet: 'earth' | 'moon' | 'mars') => void;
  onSelectPreset?: (preset: { planet: 'moon' | 'mars'; lat: number; lon: number; name: string }) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  activePlanet,
  setActivePlanet,
  onSelectPreset,
}) => {
  const PRESETS = [
    { label: 'Artemis III: Shackleton', planet: 'moon' as const, lat: -89.9, lon: 0.0, name: 'Shackleton Crater' },
    { label: 'Perseverance: Jezero', planet: 'mars' as const, lat: 18.38, lon: 77.58, name: 'Jezero Crater' },
    { label: 'Curiosity: Gale', planet: 'mars' as const, lat: -5.4, lon: 137.8, name: 'Gale Crater' },
    { label: 'Apollo 11: Tranquillitatis', planet: 'moon' as const, lat: 8.5, lon: 31.4, name: 'Mare Tranquillitatis' },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-sky-900/30 bg-[#070a14]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 via-indigo-600 to-amber-500 p-0.5 flex items-center justify-center shadow-[0_0_15px_rgba(56,189,248,0.3)]">
            <div className="w-full h-full bg-[#07090e] rounded-[10px] flex items-center justify-center">
              <Orbit className="text-sky-400" size={18} />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-white text-base tracking-wider">TERRATWIN</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-sky-950 border border-sky-800 text-sky-300 font-mono">
                NASA SPACE APPS
              </span>
            </div>
            <p className="text-[10px] text-slate-400 tracking-tight">AI-Powered Planetary Analog Discovery</p>
          </div>
        </div>

        {/* Planet Switcher Buttons */}
        <div className="flex items-center p-1 rounded-xl bg-slate-900/80 border border-slate-800">
          <button
            onClick={() => setActivePlanet('earth')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activePlanet === 'earth'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-sky-400" />
            <span>Earth (Cesium)</span>
          </button>

          <button
            onClick={() => setActivePlanet('moon')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activePlanet === 'moon'
                ? 'bg-slate-700/60 text-slate-100 border border-slate-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-slate-400" />
            <span>Moon (LOLA)</span>
          </button>

          <button
            onClick={() => setActivePlanet('mars')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activePlanet === 'mars'
                ? 'bg-orange-500/20 text-orange-300 border border-orange-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-orange-400" />
            <span>Mars (MOLA)</span>
          </button>
        </div>

        {/* Main Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1">
          <button
            onClick={() => setActiveTab('explorer')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'explorer'
                ? 'text-sky-300 bg-sky-500/10 border-b-2 border-sky-400'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <Globe size={14} />
            <span>Planet Explorer</span>
          </button>

          <button
            onClick={() => setActiveTab('discovery')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'discovery'
                ? 'text-sky-300 bg-sky-500/10 border-b-2 border-sky-400'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <Compass size={14} />
            <span>Analog Discovery</span>
          </button>

          <button
            onClick={() => setActiveTab('comparison')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'comparison'
                ? 'text-sky-300 bg-sky-500/10 border-b-2 border-sky-400'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <GitCompare size={14} />
            <span>3D Compare</span>
          </button>

          <button
            onClick={() => setActiveTab('assistant')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'assistant'
                ? 'text-sky-300 bg-sky-500/10 border-b-2 border-sky-400'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <Sparkles size={14} />
            <span>AI Assistant & Report</span>
          </button>

          <button
            onClick={() => setActiveTab('methodology')}
            className={`px-3 py-2 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'methodology'
                ? 'text-sky-300 bg-sky-500/10 border-b-2 border-sky-400'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <BookOpen size={14} />
            <span>Data & Science</span>
          </button>
        </nav>
      </div>

      {/* Subheader Mission Presets Bar */}
      <div className="bg-[#05070d] border-t border-slate-900 px-4 py-1.5 flex items-center justify-between text-xs overflow-x-auto">
        <div className="flex items-center gap-2 text-slate-400 text-[11px] whitespace-nowrap">
          <span className="font-semibold text-slate-300">Target Missions:</span>
          {PRESETS.map((p, i) => (
            <button
              key={i}
              onClick={() => {
                setActivePlanet(p.planet);
                if (onSelectPreset) onSelectPreset(p);
                setActiveTab('explorer');
              }}
              className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-sky-500/40 transition"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
};
