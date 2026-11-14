from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FeatureMeasurement(BaseModel):
    value: float
    unit: str
    data_source: str
    resolution: str
    confidence: float = Field(ge=0.0, le=1.0)
    is_estimated: bool = False

class TopographyFeatures(BaseModel):
    elevation_mean: FeatureMeasurement
    elevation_min: FeatureMeasurement
    elevation_max: FeatureMeasurement
    elevation_std: FeatureMeasurement
    slope_mean: FeatureMeasurement
    slope_p90: FeatureMeasurement
    terrain_roughness: FeatureMeasurement  # TRI (Terrain Ruggedness Index)
    relief_m: FeatureMeasurement

class GeologicalFeatures(BaseModel):
    lithology_category: str
    rock_type: str
    mineralogy_summary: str
    volcanic_character: str
    age_era: str
    silica_content_pct: Optional[float] = None
    iron_oxide_pct: Optional[float] = None
    data_source: str
    confidence: float = Field(ge=0.0, le=1.0)

class ThermalFeatures(BaseModel):
    surface_temp_mean_k: FeatureMeasurement
    surface_temp_min_k: FeatureMeasurement
    surface_temp_max_k: FeatureMeasurement
    diurnal_range_k: FeatureMeasurement
    thermal_inertia_si: FeatureMeasurement  # J m^-2 K^-1 s^-1/2

class SurfaceFeatures(BaseModel):
    albedo: FeatureMeasurement
    bare_ground_ratio: FeatureMeasurement  # 0 to 1
    vegetation_ndvi: FeatureMeasurement    # -1 to 1 (0 or negative on Moon/Mars)
    roughness_submeter: FeatureMeasurement # Estimated obstacle density
    dust_sediment_cover: FeatureMeasurement # 0 to 1

class RegionFeatureVector(BaseModel):
    region_id: str
    planet: str
    name: str
    latitude: float
    longitude: float
    radius_km: float
    topography: TopographyFeatures
    geology: GeologicalFeatures
    thermal: ThermalFeatures
    surface: SurfaceFeatures
    elevation_profile: List[float] = [] # Sample profile across radius
    slope_histogram: Dict[str, float] = {} # Binned slope % distribution
    data_coverage_score: float = 1.0     # 0 to 1 scale
    coverage_label: str = "Strong data coverage"
    provenance: List[str] = []
