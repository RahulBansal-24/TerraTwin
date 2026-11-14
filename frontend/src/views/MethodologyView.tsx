import React, { useEffect, useState } from 'react';
import { fetchDatasets } from '../api';
import { BookOpen, Database, ShieldAlert, Cpu, ExternalLink, Award, CheckCircle2 } from 'lucide-react';

export const MethodologyView: React.FC = () => {
  const [datasets, setDatasets] = useState<any[]>([]);

  useEffect(() => {
    fetchDatasets().then(setDatasets).catch(console.error);
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Page Title */}
      <div className="glass-panel p-6 rounded-2xl border border-sky-900/30">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs px-2 py-0.5 rounded bg-sky-950 border border-sky-800 text-sky-300 font-mono">
            SCIENTIFIC FOUNDATION
          </span>
          <span className="text-xs text-slate-400">Peer-Reviewed Geospatial & Planetary Datasets</span>
        </div>
        <h1 className="text-xl font-bold text-white tracking-wide">
          Data Sources, Geospatial Pipelines & Similarity Methodology
        </h1>
        <p className="text-xs text-slate-400 max-w-3xl mt-1 leading-relaxed">
          TerraTwin integrates verified remote sensing observations from NASA Planetary Data System (PDS)
          missions (LRO, MGS, 2001 Mars Odyssey) and Earth observation repositories (USGS, LP DAAC, Hamburg GLiM).
        </p>
      </div>

      {/* Dataset Inventory Cards */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Database size={16} className="text-sky-400" />
          Integrated Scientific Dataset Catalogue
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {datasets.map((ds, idx) => (
            <div key={idx} className="glass-panel p-4 rounded-xl border border-slate-800/80 space-y-2">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-[10px] font-mono uppercase text-sky-400 block">{ds.planet} • {ds.type}</span>
                  <h3 className="font-semibold text-white text-xs mt-0.5">{ds.name}</h3>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400 flex items-center gap-1 font-mono">
                  <CheckCircle2 size={10} /> Active
                </span>
              </div>

              <div className="text-[11px] text-slate-300 grid grid-cols-2 gap-2 pt-1 font-mono">
                <div>
                  <span className="text-slate-400 block text-[9px] uppercase">Resolution</span>
                  <span>{ds.resolution}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[9px] uppercase">Coverage</span>
                  <span>{ds.coverage}</span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800/60 text-[10px] text-slate-400 italic">
                {ds.citation}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Mathematical Similarity Methodology */}
      <div className="glass-panel p-6 rounded-2xl border border-sky-900/30 space-y-4">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Cpu size={16} className="text-sky-400" />
          Multidimensional Similarity Algorithm Formulation
        </h2>

        <p className="text-xs text-slate-300 leading-relaxed">
          Planetary analog matching requires rigorous normalization across distinct planetary baselines.
          Comparing 30m Earth pixels directly with extraterrestrial terrain without robust statistical scaling
          would yield mathematically invalid conclusions. TerraTwin implements a 4-tier weighted distance metric:
        </p>

        {/* Math Block */}
        <div className="bg-[#050811] p-4 rounded-xl border border-slate-800 font-mono text-xs text-sky-200 overflow-x-auto space-y-2">
          <div>
            <span className="text-slate-400"># 1. Normalized Weighted Distance Metric</span><br />
            D(A, B) = √ [ ∑ w_i · ((A_i - B_i) / σ_i)² ]
          </div>
          <div>
            <span className="text-slate-400"># 2. Exponential Similarity Mapping</span><br />
            S_topo = 100 · exp( - D_topo / τ_topo )
          </div>
          <div>
            <span className="text-slate-400"># 3. Overall Composite Score</span><br />
            S_total = w_topo · S_topo + w_geol · S_geol + w_therm · S_therm + w_surf · S_surf
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300 pt-2">
          <div className="space-y-1.5">
            <h4 className="font-semibold text-white">Petrological Compatibility Matrix</h4>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Geological similarity is not simply distance between continuous numbers; it models real geochemical
              and petrological relationships. Basaltic mare units match terrestrial flood basalts at 98%, while
              polar ice-cemented regolith pairs with Antarctic dry permafrost at 98%.
            </p>
          </div>

          <div className="space-y-1.5">
            <h4 className="font-semibold text-white">Thermal Normalization Strategy</h4>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Because absolute surface temperatures depend on solar distance and atmospheric greenhouse effect,
              thermal comparison focuses on normalized diurnal amplitude (ΔT) and thermal inertia (resistance to temperature change).
            </p>
          </div>
        </div>
      </div>

      {/* Fundamental Scientific Limitations & Caveats */}
      <div className="glass-panel p-6 rounded-2xl border border-amber-900/40 bg-[#0c0e16] space-y-3">
        <h2 className="text-sm font-bold text-amber-300 uppercase tracking-wider flex items-center gap-2">
          <ShieldAlert size={16} className="text-amber-400" />
          Planetary Caveats & Scientific Boundaries
        </h2>

        <p className="text-xs text-slate-300 leading-relaxed">
          TerraTwin makes an explicit scientific distinction between a <em>planetary analog environment</em> and an <em>exact replica</em>.
          Field testers must account for environmental boundaries that Earth cannot replicate in open-air conditions:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs pt-1">
          <div className="bg-[#050811] p-3 rounded-xl border border-slate-800">
            <span className="font-semibold text-amber-300 block mb-1">Reduced Gravity (0.16g / 0.38g)</span>
            <span className="text-slate-400 text-[11px]">
              Earth's 1g produces higher wheel ground pressure and different projectile ejecta dynamics. Offloading suspension rigs must be used.
            </span>
          </div>

          <div className="bg-[#050811] p-3 rounded-xl border border-slate-800">
            <span className="font-semibold text-amber-300 block mb-1">Atmospheric Vacuum</span>
            <span className="text-slate-400 text-[11px]">
              Moon vacuum (&lt;10⁻¹⁰ hPa) and Mars 6 hPa atmosphere mean absence of convective air cooling and instant water boiling.
            </span>
          </div>

          <div className="bg-[#050811] p-3 rounded-xl border border-slate-800">
            <span className="font-semibold text-amber-300 block mb-1">Cosmic Radiation</span>
            <span className="text-slate-400 text-[11px]">
              Earth's thick atmosphere and 45 µT geomagnetic dipole shield against galactic cosmic rays and solar particle events.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
