import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ExplorerView } from './views/ExplorerView';
import { DiscoveryView } from './views/DiscoveryView';
import { ComparisonView } from './views/ComparisonView';
import { AssistantView } from './views/AssistantView';
import { MethodologyView } from './views/MethodologyView';
import { PlanetInfo, ExplorationRegion, AnalysisResult, AnalogCandidate } from './types';
import { fetchPlanetDetails } from './api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('explorer');
  const [activePlanet, setActivePlanet] = useState<'earth' | 'moon' | 'mars'>('moon');
  const [planetDetails, setPlanetDetails] = useState<PlanetInfo | null>(null);

  // Selected region state
  const [selectedCoords, setSelectedCoords] = useState<{ lat: number; lon: number }>({ lat: -89.9, lon: 0.0 });
  const [radiusKm, setRadiusKm] = useState<number>(50);
  const [selectedRegion, setSelectedRegion] = useState<ExplorationRegion | null>(null);

  // Analysis state
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<AnalogCandidate | null>(null);

  // Load planet details when active planet changes
  useEffect(() => {
    let isMounted = true;
    fetchPlanetDetails(activePlanet)
      .then((data) => {
        if (isMounted) {
          setPlanetDetails(data);
          // Set sensible default coordinates for each planet
          if (activePlanet === 'moon') {
            setSelectedCoords({ lat: -89.9, lon: 0.0 });
            if (data.featured_regions?.length) setSelectedRegion(data.featured_regions[0]);
          } else if (activePlanet === 'mars') {
            setSelectedCoords({ lat: 18.38, lon: 77.58 });
            if (data.featured_regions?.length) setSelectedRegion(data.featured_regions[0]);
          } else {
            setSelectedCoords({ lat: -24.08, lon: -69.87 });
            setSelectedRegion(null);
          }
        }
      })
      .catch((err) => console.error('Failed to load planet info:', err));

    return () => { isMounted = false; };
  }, [activePlanet]);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    if (result.candidates.length > 0) {
      setSelectedCandidate(result.candidates[0]);
    }
    setActiveTab('discovery');
  };

  const handleSelectPreset = (preset: { planet: 'moon' | 'mars'; lat: number; lon: number; name: string }) => {
    setActivePlanet(preset.planet);
    setSelectedCoords({ lat: preset.lat, lon: preset.lon });
    if (planetDetails?.featured_regions) {
      const match = planetDetails.featured_regions.find((r) => r.name === preset.name);
      if (match) setSelectedRegion(match);
    }
  };

  return (
    <div className="min-h-screen bg-[#05070c] text-slate-100 flex flex-col font-sans selection:bg-sky-500/30 selection:text-sky-200">
      {/* Top Telemetry & Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activePlanet={activePlanet}
        setActivePlanet={setActivePlanet}
        onSelectPreset={handleSelectPreset}
      />

      {/* Main Scientific Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6">
        {activeTab === 'explorer' && (
          <ExplorerView
            planet={activePlanet}
            planetDetails={planetDetails}
            selectedCoords={selectedCoords}
            setSelectedCoords={setSelectedCoords}
            radiusKm={radiusKm}
            setRadiusKm={setRadiusKm}
            selectedRegion={selectedRegion}
            setSelectedRegion={setSelectedRegion}
            onAnalysisComplete={handleAnalysisComplete}
          />
        )}

        {activeTab === 'discovery' && (
          <DiscoveryView
            analysisResult={analysisResult}
            selectedCandidate={selectedCandidate}
            setSelectedCandidate={setSelectedCandidate}
            onLaunchComparison={(cand) => {
              setSelectedCandidate(cand);
              setActiveTab('comparison');
            }}
            onLaunchAssistant={(cand) => {
              setSelectedCandidate(cand);
              setActiveTab('assistant');
            }}
            onBackToExplorer={() => setActiveTab('explorer')}
          />
        )}

        {activeTab === 'comparison' && (
          <ComparisonView
            analysisResult={analysisResult}
            candidate={selectedCandidate}
            onBack={() => setActiveTab('discovery')}
            onLaunchAssistant={(cand) => {
              setSelectedCandidate(cand);
              setActiveTab('assistant');
            }}
          />
        )}

        {activeTab === 'assistant' && (
          <AssistantView
            analysisResult={analysisResult}
            candidate={selectedCandidate}
            onBackToDiscovery={() => setActiveTab('discovery')}
          />
        )}

        {activeTab === 'methodology' && (
          <MethodologyView />
        )}
      </main>

      {/* Scientific Footer */}
      <footer className="border-t border-slate-900 bg-[#04060a] py-6 px-4 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3 text-center md:text-left">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-400">TerraTwin</span>
            <span>•</span>
            <span>NASA Space Apps Challenge 2026</span>
            <span>•</span>
            <span className="font-mono text-[11px] text-sky-400">PDS / LOLA / MOLA / SRTM / GLiM Ingestion</span>
          </div>
          <div className="text-[11px]">
            Powered by Three.js & CesiumJS Interactive Planetary Exploration
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
