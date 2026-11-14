export interface DatabaseStats {
  status: string;
  total_candidates: number;
  coarse_cells: number;
  fine_cells: number;
  continents_count: number;
  continents: string[];
  lithologies_count: number;
  lithologies: string[];
  spatial_index: string;
  coordinate_system: string;
  resolution_coarse_km: number;
  resolution_fine_km: number;
  benchmark_catalog_count: number;
}

export interface PlanetaryFeature {
  feature_id: string;
  name: string;
  planet: string;
  feature_type: string;
  latitude: number;
  longitude: number;
  diameter_km: number;
  quadrangle?: string;
  geological_context?: string;
  approval_year?: number;
  origin?: string;
}

export interface PhysicalProperties {
  radius_km: number;
  surface_gravity_ms2: number;
  atmospheric_pressure_hpa: number;
  mean_surface_temp_k: number;
  temp_range_k: [number, number];
  solar_flux_wm2: number;
  atmosphere_summary: string;
  magnetic_field: string;
  vacuum_environment: boolean;
}

export interface ExplorationRegion {
  id: string;
  planet: string;
  name: string;
  latitude: number;
  longitude: number;
  elevation_m: number;
  diameter_km: number;
  geological_period: string;
  description: string;
  mission_significance: string;
  key_features: string[];
  scientific_targets: string[];
  preview_image?: string;
}

export interface PlanetInfo {
  id: string;
  name: string;
  tagline: string;
  description: string;
  color_theme: string;
  physical: PhysicalProperties;
  featured_regions?: ExplorationRegion[];
  data_sources?: string[];
}

export interface FeatureMeasurement {
  value: number;
  unit: string;
  data_source: string;
  resolution: string;
  confidence: number;
  is_estimated?: boolean;
}

export interface TopographyFeatures {
  elevation_mean: FeatureMeasurement;
  elevation_min: FeatureMeasurement;
  elevation_max: FeatureMeasurement;
  elevation_std: FeatureMeasurement;
  slope_mean: FeatureMeasurement;
  slope_p90: FeatureMeasurement;
  terrain_roughness: FeatureMeasurement;
  relief_m: FeatureMeasurement;
}

export interface GeologicalFeatures {
  lithology_category: string;
  rock_type: string;
  mineralogy_summary: string;
  volcanic_character: string;
  age_era: string;
  data_source: string;
  confidence: number;
}

export interface ThermalFeatures {
  surface_temp_mean_k: FeatureMeasurement;
  surface_temp_min_k: FeatureMeasurement;
  surface_temp_max_k: FeatureMeasurement;
  diurnal_range_k: FeatureMeasurement;
  thermal_inertia_si: FeatureMeasurement;
}

export interface SurfaceFeatures {
  albedo: FeatureMeasurement;
  bare_ground_ratio: FeatureMeasurement;
  vegetation_ndvi: FeatureMeasurement;
  roughness_submeter: FeatureMeasurement;
  dust_sediment_cover: FeatureMeasurement;
}

export interface RegionFeatureVector {
  region_id: string;
  planet: string;
  name: string;
  latitude: number;
  longitude: number;
  radius_km: number;
  topography: TopographyFeatures;
  geology: GeologicalFeatures;
  thermal: ThermalFeatures;
  surface: SurfaceFeatures;
  elevation_profile: number[];
  slope_histogram: Record<string, number>;
  data_coverage_score: number;
  coverage_label: string;
  provenance: string[];
}

export interface ComponentScores {
  topography_similarity: number;
  geological_similarity: number;
  thermal_similarity: number;
  surface_similarity: number;
  weighted_overall: number;
}

export interface AnalogCandidate {
  candidate_id: string;
  name: string;
  country: string;
  continent?: string;
  latitude: number;
  longitude: number;
  elevation_m: number;
  overall_similarity: number;
  confidence_level: string;
  components: ComponentScores;
  features: RegionFeatureVector;
  strongest_matches: string[];
  major_differences: string[];
  exploration_suitability: Record<string, string>;
  geological_context: string;
  real_world_missions: string[];
  rank: number;
}

export interface SimilarityWeights {
  topography_weight: number;
  geology_weight: number;
  thermal_weight: number;
  surface_weight: number;
}

export interface AnalysisRequest {
  planet: string;
  latitude: number;
  longitude: number;
  radius_km: number;
  weights?: SimilarityWeights;
  min_confidence?: number;
  filter_environment?: string;
  use_benchmark_catalog?: boolean;
  diversity_balanced?: boolean;
  continent_filter?: string;
  country_filter?: string;
  lithology_filter?: string;
  limit?: number;
}

export interface AnalysisResult {
  analysis_id: string;
  created_at: string;
  reference_planet: string;
  reference_name: string;
  reference_coordinates: { latitude: number; longitude: number };
  radius_km: number;
  weights_used: SimilarityWeights;
  reference_features: RegionFeatureVector;
  candidates: AnalogCandidate[];
  total_candidates_searched: number;
  computation_time_ms: number;
  scientific_summary: string;
  database_mode?: string;
  diversity_balanced?: boolean;
  continents_represented?: string[];
}

export interface ScientificInsight {
  candidate_id: string;
  candidate_name: string;
  reference_name: string;
  reference_planet: string;
  overall_similarity: number;
  why_selected: string;
  rover_mobility: string;
  drilling_isru: string;
  environmental_differences: string[];
  recommended_research: string[];
  real_world_missions: string[];
  key_alignments: string[];
  primary_divergences: string[];
}
