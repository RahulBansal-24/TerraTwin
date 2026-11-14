import React, { useState, useEffect } from 'react';
import { ThreeGlobe } from '../components/ThreeGlobe';
import { CesiumEarth } from '../components/CesiumEarth';
import { PlanetInfo, ExplorationRegion, RegionFeatureVector, SimilarityWeights } from '../types';
import { selectRegion, startAnalysis } from '../api';
import { Compass, Sliders, Database, ArrowRight, ShieldCheck, Mountain, Flame, Layers, Activity } from 'lucide-react';

interface ExplorerViewProps {
  planet: 'earth' | 'moon' | 'mars';
  planetDetails: PlanetInfo | null;
  selectedCoords: { lat: number; lon: number };
  setSelectedCoords: (coords: { lat: number; lon: number }) => void;
  radiusKm: number;
  setRadiusKm: (radius: number) => void;
  selectedRegion: ExplorationRegion | null;
  setSelectedRegion: (reg: ExplorationRegion | null) => void;
  onAnalysisComplete: (result: any) => void;
}

export const ExplorerView: React.FC<ExplorerViewProps> = ({
  planet,
  planetDetails,
  selectedCoords,
  setSelectedCoords,
  radiusKm,
  setRadiusKm,
  selectedRegion,
  setSelectedRegion,
  onAnalysisComplete,
}) => {
  const [loadingExtraction, setLoadingExtraction] = useState<boolean>(false);
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [featurePreview, setFeaturePreview] = useState<RegionFeatureVector | null>(null);
  const [showWeightsModal, setShowWeightsModal] = useState<boolean>(false);
  const [weights, setWeights] = useState<SimilarityWeights>({
    topography_weight: 0.35,
    geology_weight: 0.30,
    thermal_weight: 0.20,
    surface_weight: 0.15,
  });

  // Extract preview features when coordinates or radius changes
  useEffect(() => {
    let isMounted = true;
    const fetchPreview = async () => {
      try {
        setLoadingExtraction(true);
        const data = await selectRegion({
          planet,
          latitude: selectedCoords.lat,
          longitude: selectedCoords.lon,
          radius_km: radiusKm,
          name: selectedRegion?.name,
        });
        if (isMounted) {
          setFeaturePreview(data);
        }
      } catch (err) {
        console.error('Feature preview extraction error:', err);
      } finally {
        if (isMounted) setLoadingExtraction(false);
      }
    };

    fetchPreview();
    return () => { isMounted = false; };
  }, [planet, selectedCoords, radiusKm, selectedRegion]);

  const handleStartDiscovery = async () => {
    try {
      setAnalyzing(true);
      const result = await startAnalysis({
        planet,
        latitude: selectedCoords.lat,
        longitude: selectedCoords.lon,
        radius_km: radiusKm,
        weights,
      });
      onAnalysisComplete(result);
    } catch (err) {
      console.error('Discovery analysis failed:', err);
      alert('Analysis execution failed. Please verify the backend connection.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Planetary Context Header */}
      <div className="glass-panel p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 border border-sky-900/30">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className={`w-2.5 h-2.5 rounded-full ${planet === 'mars' ? 'bg-orange-400' : (planet === 'moon' ? 'bg-slate-300' : 'bg-sky-400')} animate-pulse`} />
            <h1 className="text-xl font-bold text-white tracking-wide">
              {planetDetails?.name || planet.toUpperCase()} EXPLORATION
            </h1>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {planetDetails?.tagline}
            </span>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
            {planetDetails?.description}
          </p>
        </div>

        {/* Physical Planetary Metrics */}
        {planetDetails && (
          <div className="grid grid-cols-3 gap-3 bg-[#050811] p-3 rounded-xl border border-slate-800 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px]">Surface Gravity</span>
              <span className="font-mono font-semibold text-white">{planetDetails.physical.surface_gravity_ms2} m/s²</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px]">Pressure</span>
              <span className="font-mono font-semibold text-white">
                {planetDetails.physical.atmospheric_pressure_hpa < 0.01 ? '<10⁻¹⁰ hPa' : `${planetDetails.physical.atmospheric_pressure_hpa} hPa`}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px]">Temp Range</span>
              <span className="font-mono font-semibold text-white">
                {planetDetails.physical.temp_range_k[0]} - {planetDetails.physical.temp_range_k[1]} K
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Main Interactive 3D Globe & Selection Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: 3D Globe Canvas */}
        <div className="lg:col-span-8 flex flex-col">
          {planet === 'earth' ? (
            <CesiumEarth
              selectedCoords={selectedCoords}
              radiusKm={radiusKm}
              onSelectCoords={(lat, lon) => {
                setSelectedCoords({ lat, lon });
                setSelectedRegion(null);
              }}
              height="580px"
            />
          ) : (
            <ThreeGlobe
              planet={planet}
              selectedCoords={selectedCoords}
              radiusKm={radiusKm}
              featuredRegions={planetDetails?.featured_regions || []}
              onSelectCoords={(lat, lon) => {
                setSelectedCoords({ lat, lon });
                setSelectedRegion(null);
              }}
              onSelectRegion={(reg) => {
                setSelectedRegion(reg);
                setSelectedCoords({ lat: reg.latitude, lon: reg.longitude });
              }}
              height="580px"
            />
          )}

          <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
            <span>Click anywhere on the planetary surface to raycast target coordinates</span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              LOLA & MOLA Topographic Data Ingested
            </span>
          </div>
        </div>

        {/* Right: Region Specification & Scientific Telemetry */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          {/* Coordinates and Radius Card */}
          <div className="glass-panel p-5 rounded-2xl border border-sky-900/30 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <Compass size={16} className="text-sky-400" />
                Selected Coordinates
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded bg-sky-950/80 border border-sky-800 text-sky-300 font-mono">
                {loadingExtraction ? 'Extracting...' : 'Calibrated'}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-[#050811] p-3 rounded-xl border border-slate-800">
                <label className="text-[10px] text-slate-400 uppercase font-mono">Latitude</label>
                <div className="font-mono text-base font-bold text-white mt-0.5">
                  {selectedCoords.lat.toFixed(2)}° {selectedCoords.lat >= 0 ? 'N' : 'S'}
                </div>
              </div>

              <div className="bg-[#050811] p-3 rounded-xl border border-slate-800">
                <label className="text-[10px] text-slate-400 uppercase font-mono">Longitude</label>
                <div className="font-mono text-base font-bold text-white mt-0.5">
                  {selectedCoords.lon.toFixed(2)}° {selectedCoords.lon >= 0 ? 'E' : 'W'}
                </div>
              </div>
            </div>

            {selectedRegion && (
              <div className="bg-sky-950/30 border border-sky-800/40 p-3 rounded-xl">
                <div className="text-xs font-semibold text-sky-200">{selectedRegion.name}</div>
                <div className="text-[11px] text-slate-300 mt-1 line-clamp-2">{selectedRegion.description}</div>
              </div>
            )}

            {/* Exploration Radius Slider */}
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="text-slate-300">Exploration Radius</span>
                <span className="font-mono text-sky-300 font-bold">{radiusKm} km</span>
              </div>
              <input
                type="range"
                min="10"
                max="250"
                step="5"
                value={radiusKm}
                onChange={(e) => setRadiusKm(parseInt(e.target.value))}
                className="w-full accent-sky-400 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1 font-mono">
                <span>10 km (Local Crater)</span>
                <span>250 km (Regional)</span>
              </div>
            </div>

            {/* Configurable Similarity Weights Trigger */}
            <div className="flex items-center justify-between pt-2 border-t border-slate-800">
              <button
                onClick={() => setShowWeightsModal(!showWeightsModal)}
                className="text-xs text-slate-400 hover:text-sky-300 flex items-center gap-1.5 transition"
              >
                <Sliders size={13} />
                <span>Adjust Scientific Weights</span>
              </button>
              <span className="text-[10px] text-slate-500 font-mono">4 Parameters Active</span>
            </div>

            {/* Weights Drawer */}
            {showWeightsModal && (
              <div className="bg-[#050811] p-3 rounded-xl border border-slate-800 space-y-2.5 text-xs">
                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-300">Topography (Slope/Roughness)</span>
                    <span className="font-mono text-sky-300">{(weights.topography_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.05"
                    value={weights.topography_weight}
                    onChange={(e) => setWeights({ ...weights, topography_weight: parseFloat(e.target.value) })}
                    className="w-full accent-sky-400 h-1"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-300">Geology (Lithology/Petrology)</span>
                    <span className="font-mono text-indigo-300">{(weights.geology_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.05"
                    value={weights.geology_weight}
                    onChange={(e) => setWeights({ ...weights, geology_weight: parseFloat(e.target.value) })}
                    className="w-full accent-indigo-400 h-1"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-300">Thermal (Diurnal Range/Inertia)</span>
                    <span className="font-mono text-orange-300">{(weights.thermal_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.05"
                    value={weights.thermal_weight}
                    onChange={(e) => setWeights({ ...weights, thermal_weight: parseFloat(e.target.value) })}
                    className="w-full accent-orange-400 h-1"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-300">Surface (Albedo/Obstacles)</span>
                    <span className="font-mono text-emerald-300">{(weights.surface_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.05"
                    value={weights.surface_weight}
                    onChange={(e) => setWeights({ ...weights, surface_weight: parseFloat(e.target.value) })}
                    className="w-full accent-emerald-400 h-1"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Real-Time Extracted Measurements Preview */}
          {featurePreview && (
            <div className="glass-panel p-4 rounded-2xl border border-sky-900/30 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-white flex items-center gap-1.5">
                  <Database size={14} className="text-sky-400" />
                  Extracted Feature Vector
                </span>
                <span className="text-[10px] text-emerald-400 flex items-center gap-1">
                  <ShieldCheck size={12} />
                  {featurePreview.coverage_label}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 flex items-center gap-1">
                    <Mountain size={11} className="text-sky-400" /> Mean Slope
                  </span>
                  <span className="font-mono font-bold text-white text-sm">
                    {featurePreview.topography.slope_mean.value.toFixed(1)}°
                  </span>
                </div>

                <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 flex items-center gap-1">
                    <Activity size={11} className="text-sky-400" /> Roughness (TRI)
                  </span>
                  <span className="font-mono font-bold text-white text-sm">
                    {featurePreview.topography.terrain_roughness.value.toFixed(1)}
                  </span>
                </div>

                <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 flex items-center gap-1">
                    <Flame size={11} className="text-orange-400" /> Diurnal Range
                  </span>
                  <span className="font-mono font-bold text-white text-sm">
                    {featurePreview.thermal.diurnal_range_k.value.toFixed(0)} K
                  </span>
                </div>

                <div className="bg-[#050811] p-2.5 rounded-lg border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 flex items-center gap-1">
                    <Layers size={11} className="text-indigo-400" /> Lithology
                  </span>
                  <span className="font-medium text-slate-200 text-[11px] truncate block">
                    {featurePreview.geology.lithology_category.replace('_', ' ')}
                  </span>
                </div>
              </div>

              <div className="text-[10px] text-slate-400 font-mono pt-1">
                Data Provenance: {featurePreview.provenance[0]}
              </div>
            </div>
          )}

          {/* Action Trigger CTA */}
          <button
            onClick={handleStartDiscovery}
            disabled={analyzing}
            className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-sky-500 via-indigo-600 to-sky-600 text-white font-semibold text-sm tracking-wide shadow-[0_0_25px_rgba(56,189,248,0.35)] hover:shadow-[0_0_35px_rgba(56,189,248,0.55)] transition-all flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
          >
            {analyzing ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Scanning Earth Analog Catalog...</span>
              </>
            ) : (
              <>
                <span>Search Earth for Analogs</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
