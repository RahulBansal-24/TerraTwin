import React, { useEffect, useRef, useState } from 'react';
import * as Cesium from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';
import { AnalogCandidate } from '../types';
import { Layers, Globe, MapPin, ZoomIn, ZoomOut, Compass } from 'lucide-react';
import { ThreeGlobe } from './ThreeGlobe';

interface CesiumEarthProps {
  candidates?: AnalogCandidate[];
  selectedCandidateId?: string | null;
  onSelectCandidate?: (candidate: AnalogCandidate) => void;
  onSelectCoords?: (lat: number, lon: number) => void;
  selectedCoords?: { lat: number; lon: number } | null;
  radiusKm?: number;
  height?: string;
  className?: string;
}

export const CesiumEarth: React.FC<CesiumEarthProps> = ({
  candidates = [],
  selectedCandidateId,
  onSelectCandidate,
  onSelectCoords,
  selectedCoords,
  radiusKm = 50,
  height = '600px',
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);
  const [use3DThreeFallback, setUse3DThreeFallback] = useState<boolean>(false);
  const [cesiumError, setCesiumError] = useState<string | null>(null);

  // Initialize Cesium viewer
  useEffect(() => {
    if (use3DThreeFallback || !containerRef.current) return;

    try {
      // Set Cesium Ion default access token or base imagery
      Cesium.Ion.defaultAccessToken = ''; // Will fall back to open imagery providers

      const viewerOptions: any = {
        animation: false,
        baseLayerPicker: false,
        fullscreenButton: false,
        geocoder: false,
        homeButton: false,
        infoBox: false,
        sceneModePicker: false,
        selectionIndicator: false,
        timeline: false,
        navigationHelpButton: false,
        scene3DOnly: true,
        baseLayer: new Cesium.ImageryLayer(new Cesium.UrlTemplateImageryProvider({
          url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          credit: 'OpenStreetMap contributors'
        })),
      };

      const viewer = new Cesium.Viewer(containerRef.current, viewerOptions);

      // Start in a full global orbital view of Earth
      viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(0.0, 15.0, 22000000),
      });

      // Dark futuristic atmosphere styling
      viewer.scene.globe.enableLighting = true;
      viewer.scene.backgroundColor = Cesium.Color.fromCssColorString('#07090e');
      viewer.scene.fog.enabled = true;
      viewer.scene.fog.density = 0.0002;

      // Handle coordinate picking on Earth surface
      const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
      handler.setInputAction((movement: any) => {
        const pickedObject = viewer.scene.pick(movement.position);
        if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.candidateData) {
          if (onSelectCandidate) {
            onSelectCandidate(pickedObject.id.candidateData);
          }
          return;
        }

        const cartesian = viewer.camera.pickEllipsoid(movement.position, viewer.scene.globe.ellipsoid);
        if (cartesian) {
          const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
          const lat = Cesium.Math.toDegrees(cartographic.latitude);
          const lon = Cesium.Math.toDegrees(cartographic.longitude);
          if (onSelectCoords) {
            onSelectCoords(Math.round(lat * 100) / 100, Math.round(lon * 100) / 100);
          }
        }
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

      viewerRef.current = viewer;

      return () => {
        handler.destroy();
        if (!viewer.isDestroyed()) {
          viewer.destroy();
        }
      };
    } catch (err: any) {
      console.warn('Cesium initialization fallback to Three.js Earth:', err);
      setCesiumError('Falling back to hardware-accelerated 3D WebGL Earth');
      setUse3DThreeFallback(true);
    }
  }, [use3DThreeFallback]);

  // Update candidate markers on Cesium globe
  useEffect(() => {
    if (!viewerRef.current || use3DThreeFallback) return;
    const viewer = viewerRef.current;

    viewer.entities.removeAll();

    // Add candidate analog markers
    candidates.forEach((cand) => {
      const isSelected = cand.candidate_id === selectedCandidateId;

      // Color coding based on similarity score
      let pinColor = Cesium.Color.fromCssColorString('#0ea5e9'); // cyan
      if (cand.overall_similarity >= 85) {
        pinColor = Cesium.Color.fromCssColorString('#10b981'); // emerald
      } else if (cand.overall_similarity < 75) {
        pinColor = Cesium.Color.fromCssColorString('#f59e0b'); // amber
      }

      viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(cand.longitude, cand.latitude, 2000),
        point: {
          pixelSize: isSelected ? 18 : 12,
          color: pinColor,
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: isSelected ? 3 : 1.5,
          heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND,
        },
        label: {
          text: `${cand.name} (${cand.overall_similarity}%)`,
          font: isSelected ? 'bold 12px sans-serif' : '10px sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 2,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          pixelOffset: new Cesium.Cartesian2(0, -20),
          showBackground: true,
          backgroundColor: Cesium.Color.fromCssColorString('rgba(15, 23, 42, 0.8)'),
        },
        candidateData: cand,
      } as any);

      // If selected candidate, highlight coverage area circle
      if (isSelected) {
        viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(cand.longitude, cand.latitude),
          ellipse: {
            semiMinorAxis: radiusKm * 1000,
            semiMajorAxis: radiusKm * 1000,
            material: Cesium.Color.fromCssColorString('rgba(56, 189, 248, 0.25)'),
            outline: true,
            outlineColor: Cesium.Color.fromCssColorString('#38bdf8'),
            outlineWidth: 2,
          },
        });

        // Fly camera to selected candidate
        viewer.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(cand.longitude, cand.latitude, radiusKm * 3500),
          duration: 1.5,
        });
      }
    });

    // Custom selected coordinate marker
    if (selectedCoords) {
      viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(selectedCoords.lon, selectedCoords.lat, 2000),
        point: {
          pixelSize: 14,
          color: Cesium.Color.fromCssColorString('#fb923c'),
          outlineColor: Cesium.Color.WHITE,
          outlineWidth: 2,
        },
        ellipse: {
          semiMinorAxis: radiusKm * 1000,
          semiMajorAxis: radiusKm * 1000,
          material: Cesium.Color.fromCssColorString('rgba(251, 146, 60, 0.25)'),
          outline: true,
          outlineColor: Cesium.Color.fromCssColorString('#fb923c'),
        },
      });
    }
  }, [candidates, selectedCandidateId, selectedCoords, radiusKm, use3DThreeFallback]);

  if (use3DThreeFallback) {
    return (
      <div className={`relative ${className}`}>
        <ThreeGlobe
          planet="earth"
          selectedCoords={selectedCoords}
          radiusKm={radiusKm}
          onSelectCoords={onSelectCoords}
          height={height}
          showControls={true}
        />
        {/* Mode toggle back to Photorealistic Cesium */}
        <div className="absolute top-4 right-4 z-10 flex items-center gap-2">
          <button
            onClick={() => setUse3DThreeFallback(false)}
            className="glass-panel text-xs text-sky-300 hover:text-white px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition cursor-pointer border border-sky-500/40 bg-[#070a14]/90 shadow-md"
            title="Switch to Photorealistic CesiumJS Earth"
          >
            <Layers size={13} className="text-sky-400" />
            <span>Switch to Cesium Earth</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative overflow-hidden rounded-xl border border-sky-900/40 bg-[#07090e] ${className}`}>
      <div ref={containerRef} style={{ height }} className="w-full" />

      {/* Mode toggle */}
      <div className="absolute top-4 right-4 z-10 flex items-center gap-2">
        <button
          onClick={() => setUse3DThreeFallback(true)}
          className="glass-panel text-xs text-slate-300 hover:text-white px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition cursor-pointer border border-slate-700/60 bg-[#070a14]/80 shadow-md"
          title="Switch to 3D Three.js Globe Mode"
        >
          <Globe size={13} className="text-sky-400" />
          <span>Switch to Three.js Globe</span>
        </button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 z-10 glass-panel rounded-lg px-3 py-2 text-[11px] text-slate-300 pointer-events-none">
        <div className="font-semibold text-white mb-1">Earth Analog Candidates</div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500" /> &gt;85% High Match</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-sky-400" /> 75-84% Moderate</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400" /> &lt;75% Partial</span>
        </div>
      </div>
    </div>
  );
};
