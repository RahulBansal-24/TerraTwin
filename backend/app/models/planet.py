from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PhysicalProperties(BaseModel):
    radius_km: float
    surface_gravity_ms2: float
    atmospheric_pressure_hpa: float
    mean_surface_temp_k: float
    temp_range_k: List[float]  # [min, max]
    solar_flux_wm2: float
    atmosphere_summary: str
    magnetic_field: str
    vacuum_environment: bool

class ExplorationRegion(BaseModel):
    id: str
    planet: str
    name: str
    latitude: float
    longitude: float
    elevation_m: float
    diameter_km: float
    geological_period: str
    description: str
    mission_significance: str
    key_features: List[str]
    scientific_targets: List[str]
    preview_image: Optional[str] = None

class PlanetInfo(BaseModel):
    id: str
    name: str
    tagline: str
    description: str
    physical: PhysicalProperties
    color_theme: str
    featured_regions: List[ExplorationRegion]
    data_sources: List[str]
