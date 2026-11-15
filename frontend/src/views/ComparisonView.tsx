import React from 'react';
import { AnalysisResult, AnalogCandidate } from '../types';
import { ThreeGlobe } from '../components/ThreeGlobe';
import { CesiumEarth } from '../components/CesiumEarth';
import { RadarChart } from '../components/RadarChart';
import { ElevationProfileChart } from '../components/ElevationProfileChart';
import { ArrowLeft, Sparkles, Download, GitCompare, Mountain, Layers, Flame, Activity } from 'lucide-react';

interface ComparisonViewProps {
  analysisResult: AnalysisResult | null;
  candidate: AnalogCandidate | null;
  onBack: () => void;
  onLaunchAssistant: (cand: AnalogCandidate) => void;
}

export const ComparisonView: React.FC<ComparisonViewProps> = ({
  analysisResult,
  candidate,
  onBack,
  onLaunchAssistant,
}) => {
  if (!analysisResult || !candidate) {
    return (
      <div className="glass-panel p-12 rounded-2xl text-center space-y-4 max-w-xl mx-auto my-12">
        <GitCompare size={40} className="text-sky-400 mx-auto" />
        <h2 className="text-lg font-bold text-white">No Comparison Active</h2>
        <p className="text-xs text-slate-400">
          Run an analog discovery search and select an Earth candidate to inspect side-by-side.
        </p>
        <button
          onClick={onBack}
          className="px-4 py-2 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-semibold hover:bg-sky-500/30 transition"
        >
          Back to Discovery
        </button>
      </div>
    );
  }

  const ref = analysisResult.reference_features;
  const cand = candidate.features;
  const planet = analysisResult.reference_planet;

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <button
              onClick={onBack}
              className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition mr-1"
              title="Back"
            >
              <ArrowLeft size={16} />
            </button>
            <span className="text-xs px-2 py-0.5 rounded bg-sky-950 border border-sky-800 text-sky-300 font-mono">
              3D SCIENTIFIC COMPARISON
            </span>
            <span className="text-xs text-slate-400">
              Quantitative Match: <strong className="text-sky-300 font-mono">{candidate.overall_similarity}%</strong>
            </span>
          </div>
          <h1 className="text-lg font-bold text-white tracking-wide">
            {ref.name} ({planet.toUpperCase()}) vs {candidate.name} (EARTH)
          </h1>
        </div>

        <button
          onClick={() => onLaunchAssistant(candidate)}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-sky-600 text-white text-xs font-semibold hover:opacity-90 transition flex items-center gap-1.5 shadow-md self-start md:self-auto"
        >
          <Sparkles size={14} />
          <span>AI Exploration Guidance</span>
        </button>
      </div>

      {/* Side-by-Side 3D Globes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Extraterrestrial Globe */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className={`w-2 h-2 rounded-full ${planet === 'mars' ? 'bg-orange-400' : 'bg-slate-400'}`} />
              {planet.toUpperCase()}: {ref.name}
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              {ref.latitude.toFixed(2)}°, {ref.longitude.toFixed(2)}°
            </span>
          </div>
          <ThreeGlobe
            planet={planet as 'moon' | 'mars'}
            selectedCoords={{ lat: ref.latitude, lon: ref.longitude }}
            radiusKm={ref.radius_km}
            height="380px"
            defaultAutoRotate={false}
          />
        </div>

        {/* Terrestrial Analog Globe */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              EARTH ANALOG: {candidate.name} ({candidate.country})
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              {candidate.latitude.toFixed(2)}°, {candidate.longitude.toFixed(2)}°
            </span>
          </div>
          <CesiumEarth
            candidates={[candidate]}
            selectedCandidateId={candidate.candidate_id}
            selectedCoords={{ lat: candidate.latitude, lon: candidate.longitude }}
            radiusKm={ref.radius_km}
            height="380px"
            defaultAutoRotate={false}
            zoomToCandidate={false}
          />
        </div>
      </div>

      {/* Scientific Comparison Analysis Grid: Radar + Elevation Profile */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radar Chart */}
        <div className="lg:col-span-5 glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col items-center justify-center">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider mb-2 self-start">
            Multidimensional Parameter Congruence
          </h2>
          <RadarChart scores={candidate.components} candidateName={candidate.name} size={280} />
        </div>

        {/* Elevation Cross-Section Profile */}
        <div className="lg:col-span-7 glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col justify-between">
          <div>
            <h2 className="text-xs font-bold text-white uppercase tracking-wider mb-1">
              Topographic Cross-Section Morphometry
            </h2>
            <p className="text-[11px] text-slate-400 mb-3">
              Normalized elevation variations across the {ref.radius_km} km radius slice.
            </p>
            <ElevationProfileChart
              refName={ref.name}
              refProfile={ref.elevation_profile}
              candName={candidate.name}
              candProfile={cand.elevation_profile}
              refPlanet={planet.toUpperCase()}
              height={170}
            />
          </div>

          <div className="grid grid-cols-2 gap-3 mt-4 pt-3 border-t border-slate-800 text-xs">
            <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Terrain Ruggedness (TRI)</span>
              <span className="font-mono font-bold text-white">
                {ref.topography.terrain_roughness.value.toFixed(1)} vs {cand.topography.terrain_roughness.value.toFixed(1)}
              </span>
            </div>
            <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Mean Slope Gradient</span>
              <span className="font-mono font-bold text-white">
                {ref.topography.slope_mean.value.toFixed(1)}° vs {cand.topography.slope_mean.value.toFixed(1)}°
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Quantitative Parameter Comparison Table */}
      <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 overflow-x-auto">
        <h2 className="text-sm font-bold text-white mb-3">Quantitative Scientific Comparison Matrix</h2>
        <table className="w-full text-xs text-left">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 font-mono text-[11px]">
              <th className="pb-2.5">Category</th>
              <th className="pb-2.5">{ref.name} ({planet.toUpperCase()})</th>
              <th className="pb-2.5">{candidate.name} (EARTH)</th>
              <th className="pb-2.5">Unit</th>
              <th className="pb-2.5">Data Provenance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Mean Surface Elevation</td>
              <td className="py-2.5 text-white">{ref.topography.elevation_mean.value.toLocaleString()}</td>
              <td className="py-2.5 text-white">{cand.topography.elevation_mean.value.toLocaleString()}</td>
              <td className="py-2.5 text-slate-400">m</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">LOLA / MOLA / SRTM</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Topographic Relief</td>
              <td className="py-2.5 text-white">{ref.topography.relief_m.value.toLocaleString()}</td>
              <td className="py-2.5 text-white">{cand.topography.relief_m.value.toLocaleString()}</td>
              <td className="py-2.5 text-slate-400">m</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">Max - Min DEM</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Mean Slope Angle</td>
              <td className="py-2.5 text-white">{ref.topography.slope_mean.value.toFixed(1)}</td>
              <td className="py-2.5 text-white">{cand.topography.slope_mean.value.toFixed(1)}</td>
              <td className="py-2.5 text-slate-400">degrees</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">2D Gradient Filter</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Peak Slope (90th percentile)</td>
              <td className="py-2.5 text-white">{ref.topography.slope_p90.value.toFixed(1)}</td>
              <td className="py-2.5 text-white">{cand.topography.slope_p90.value.toFixed(1)}</td>
              <td className="py-2.5 text-slate-400">degrees</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">Regional Slope CDF</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Diurnal Temperature Swing</td>
              <td className="py-2.5 text-white">{ref.thermal.diurnal_range_k.value.toFixed(0)}</td>
              <td className="py-2.5 text-white">{cand.thermal.diurnal_range_k.value.toFixed(0)}</td>
              <td className="py-2.5 text-slate-400">K</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">Diviner / THEMIS / MODIS</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Thermal Inertia</td>
              <td className="py-2.5 text-white">{ref.thermal.thermal_inertia_si.value.toFixed(0)}</td>
              <td className="py-2.5 text-white">{cand.thermal.thermal_inertia_si.value.toFixed(0)}</td>
              <td className="py-2.5 text-slate-400">J m⁻² K⁻¹ s⁻¹/²</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">Thermal Inertia Model</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Optical Surface Albedo</td>
              <td className="py-2.5 text-white">{ref.surface.albedo.value.toFixed(2)}</td>
              <td className="py-2.5 text-white">{cand.surface.albedo.value.toFixed(2)}</td>
              <td className="py-2.5 text-slate-400">ratio</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">LROC / THEMIS / MODIS</td>
            </tr>
            <tr>
              <td className="py-2.5 text-slate-300 font-sans">Bare Ground Fraction</td>
              <td className="py-2.5 text-white">{(ref.surface.bare_ground_ratio.value * 100).toFixed(0)}%</td>
              <td className="py-2.5 text-white">{(cand.surface.bare_ground_ratio.value * 100).toFixed(0)}%</td>
              <td className="py-2.5 text-slate-400">percent</td>
              <td className="py-2.5 text-slate-400 text-[10px] font-sans">Copernicus / Planetary Map</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
