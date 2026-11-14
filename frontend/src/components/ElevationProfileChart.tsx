import React from 'react';

interface ElevationProfileChartProps {
  refName: string;
  refProfile: number[];
  candName: string;
  candProfile: number[];
  refPlanet: string;
  height?: number;
}

export const ElevationProfileChart: React.FC<ElevationProfileChartProps> = ({
  refName,
  refProfile = [],
  candName,
  candProfile = [],
  refPlanet,
  height = 160,
}) => {
  const width = 450;
  const padding = { top: 20, right: 30, bottom: 30, left: 55 };
  const plotW = width - padding.left - padding.right;
  const plotH = height - padding.top - padding.bottom;

  // Normalize profiles for side-by-side relative topographic morphology comparison
  const sampleCount = Math.max(refProfile.length, candProfile.length) || 30;

  const getProfilePoints = (profile: number[], color: string) => {
    if (!profile.length) return '';
    const minVal = Math.min(...profile);
    const maxVal = Math.max(...profile);
    const range = (maxVal - minVal) || 1;

    return profile.map((val, idx) => {
      const x = padding.left + (idx / (profile.length - 1)) * plotW;
      const y = padding.top + plotH - ((val - minVal) / range) * plotH;
      return `${x},${y}`;
    }).join(' ');
  };

  const refPoints = getProfilePoints(refProfile, '#38bdf8');
  const candPoints = getProfilePoints(candProfile, '#10b981');

  return (
    <div className="flex flex-col w-full">
      <div className="flex items-center justify-between text-xs mb-2">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-sky-400">
            <span className="w-3 h-0.5 bg-sky-400 inline-block" />
            {refName} ({refPlanet})
          </span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <span className="w-3 h-0.5 bg-emerald-400 inline-block" />
            {candName} (Earth)
          </span>
        </div>
        <span className="text-slate-400 text-[10px]">Relative Topographic Relief Profile</span>
      </div>

      <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} className="overflow-visible">
        {/* Horizontal gridlines */}
        {[0, 0.25, 0.5, 0.75, 1].map((pct, idx) => {
          const y = padding.top + plotH * pct;
          return (
            <line
              key={idx}
              x1={padding.left}
              y1={y}
              x2={width - padding.right}
              y2={y}
              stroke="#1e293b"
              strokeWidth="1"
              strokeDasharray="3 3"
            />
          );
        })}

        {/* Candidate Profile (Green) */}
        {candPoints && (
          <polyline
            points={candPoints}
            fill="none"
            stroke="#10b981"
            strokeWidth="2"
            strokeDasharray="4 2"
          />
        )}

        {/* Reference Profile (Cyan) */}
        {refPoints && (
          <polyline
            points={refPoints}
            fill="none"
            stroke="#38bdf8"
            strokeWidth="2.5"
          />
        )}

        {/* Axis labels */}
        <text x={padding.left} y={height - 10} fill="#64748b" fontSize="9">-Radius</text>
        <text x={padding.left + plotW / 2} y={height - 10} fill="#64748b" fontSize="9" textAnchor="middle">Center</text>
        <text x={width - padding.right} y={height - 10} fill="#64748b" fontSize="9" textAnchor="end">+Radius</text>
        <text x={12} y={padding.top + plotH / 2} fill="#64748b" fontSize="9" transform={`rotate(-90 12 ${padding.top + plotH / 2})`} textAnchor="middle">
          Elevation (Relief)
        </text>
      </svg>
    </div>
  );
};
