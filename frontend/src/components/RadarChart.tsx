import React from 'react';
import { ComponentScores } from '../types';

interface RadarChartProps {
  scores: ComponentScores;
  candidateName?: string;
  size?: number;
}

export const RadarChart: React.FC<RadarChartProps> = ({
  scores,
  candidateName = 'Analog Match',
  size = 280,
}) => {
  const center = size / 2;
  const radius = (size / 2) - 40;

  const axes = [
    { label: 'Topography', value: scores.topography_similarity },
    { label: 'Geology', value: scores.geological_similarity },
    { label: 'Thermal', value: scores.thermal_similarity },
    { label: 'Surface', value: scores.surface_similarity },
    { label: 'Roughness', value: Math.min(100, scores.topography_similarity * 1.05) },
  ];

  const numAxes = axes.length;
  const angleStep = (2 * Math.PI) / numAxes;

  // Grid level polygons (20%, 40%, 60%, 80%, 100%)
  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0];

  const getCoordinates = (valueNormalized: number, index: number) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = valueNormalized * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  // Build data polygon points
  const points = axes.map((axis, i) => {
    const norm = Math.max(0, Math.min(100, axis.value)) / 100;
    const { x, y } = getCoordinates(norm, i);
    return `${x},${y}`;
  }).join(' ');

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="overflow-visible">
        {/* Background web grids */}
        {gridLevels.map((lvl, idx) => {
          const gridPoints = axes.map((_, i) => {
            const { x, y } = getCoordinates(lvl, i);
            return `${x},${y}`;
          }).join(' ');
          return (
            <polygon
              key={idx}
              points={gridPoints}
              fill={idx === gridLevels.length - 1 ? 'rgba(15, 23, 42, 0.6)' : 'none'}
              stroke="#1e293b"
              strokeWidth="1"
              strokeDasharray={idx < gridLevels.length - 1 ? '2 2' : 'none'}
            />
          );
        })}

        {/* Axis radial spokes */}
        {axes.map((_, i) => {
          const { x, y } = getCoordinates(1.0, i);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={x}
              y2={y}
              stroke="#334155"
              strokeWidth="1"
            />
          );
        })}

        {/* Data polygon */}
        <polygon
          points={points}
          fill="rgba(56, 189, 248, 0.25)"
          stroke="#38bdf8"
          strokeWidth="2.5"
          className="radar-glow"
        />

        {/* Vertex data points */}
        {axes.map((axis, i) => {
          const norm = Math.max(0, Math.min(100, axis.value)) / 100;
          const { x, y } = getCoordinates(norm, i);
          return (
            <circle
              key={i}
              cx={x}
              cy={y}
              r="4"
              fill="#38bdf8"
              stroke="#0f172a"
              strokeWidth="2"
            />
          );
        })}

        {/* Axis Labels */}
        {axes.map((axis, i) => {
          const { x, y } = getCoordinates(1.18, i);
          return (
            <text
              key={i}
              x={x}
              y={y}
              textAnchor="middle"
              dominantBaseline="central"
              className="fill-sky-300 text-[11px] font-medium tracking-wider"
            >
              {axis.label} ({axis.value.toFixed(0)}%)
            </text>
          );
        })}
      </svg>
      <div className="text-xs text-slate-400 mt-2 font-mono">
        Multidimensional Similarity Index: <span className="text-sky-300 font-bold">{scores.weighted_overall}%</span>
      </div>
    </div>
  );
};
