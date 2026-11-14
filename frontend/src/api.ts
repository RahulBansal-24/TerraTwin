import {
  PlanetInfo, ExplorationRegion, RegionFeatureVector,
  AnalysisRequest, AnalysisResult, AnalogCandidate, ScientificInsight
} from './types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export async function fetchPlanets(): Promise<PlanetInfo[]> {
  const res = await fetch(`${API_BASE}/planets`);
  if (!res.ok) throw new Error('Failed to fetch planets');
  return res.json();
}

export async function fetchPlanetDetails(planet: string): Promise<PlanetInfo> {
  const res = await fetch(`${API_BASE}/planets/${planet}`);
  if (!res.ok) throw new Error(`Failed to fetch ${planet} details`);
  return res.json();
}

export async function fetchPlanetRegions(planet: string): Promise<ExplorationRegion[]> {
  const res = await fetch(`${API_BASE}/planets/${planet}/regions`);
  if (!res.ok) throw new Error(`Failed to fetch regions for ${planet}`);
  return res.json();
}

export async function selectRegion(payload: {
  planet: string;
  latitude: number;
  longitude: number;
  radius_km: number;
  name?: string;
}): Promise<RegionFeatureVector> {
  const res = await fetch(`${API_BASE}/regions/select`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to extract region features');
  return res.json();
}

export async function startAnalysis(request: AnalysisRequest): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/analysis/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error('Similarity analysis execution failed');
  return res.json();
}

export async function fetchAnalysis(analysisId: string): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/analysis/${analysisId}`);
  if (!res.ok) throw new Error('Failed to fetch analysis result');
  return res.json();
}

export async function compareCandidate(analysisId: string, candidateId: string): Promise<{
  analysis_id: string;
  reference_planet: string;
  reference_name: string;
  reference_features: RegionFeatureVector;
  candidate: AnalogCandidate;
  explanation: ScientificInsight;
}> {
  const res = await fetch(`${API_BASE}/compare/${analysisId}/${candidateId}`);
  if (!res.ok) throw new Error('Failed to compare candidate');
  return res.json();
}

export async function generateInsights(payload: {
  analysis_id: string;
  candidate_id?: string;
  question?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/insights/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to generate AI insights');
  return res.json();
}

export async function generateReport(payload: {
  analysis_id: string;
  candidate_id: string;
}): Promise<{
  report_id: string;
  filename: string;
  download_url: string;
  created_at: string;
  file_size_bytes: number;
}> {
  const res = await fetch(`${API_BASE}/reports/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Report compilation failed');
  return res.json();
}

export function getReportDownloadUrl(reportId: string): string {
  return `${API_BASE}/reports/${reportId}/download`;
}

export async function fetchDatasets(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/datasets`);
  if (!res.ok) throw new Error('Failed to fetch datasets');
  return res.json();
}
