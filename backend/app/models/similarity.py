from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from .features import RegionFeatureVector

class SimilarityWeights(BaseModel):
    topography_weight: float = Field(0.35, ge=0.0, le=1.0)
    geology_weight: float = Field(0.30, ge=0.0, le=1.0)
    thermal_weight: float = Field(0.20, ge=0.0, le=1.0)
    surface_weight: float = Field(0.15, ge=0.0, le=1.0)

class ComponentScores(BaseModel):
    topography_similarity: float
    geological_similarity: float
    thermal_similarity: float
    surface_similarity: float
    weighted_overall: float

class FeatureDifference(BaseModel):
    feature_name: str
    category: str
    reference_value: str
    candidate_value: str
    unit: str
    delta_score: float
    scientific_note: str

class AnalogCandidate(BaseModel):
    candidate_id: str
    name: str
    country: str
    continent: Optional[str] = "Global"
    latitude: float
    longitude: float
    elevation_m: float
    overall_similarity: float # 0 - 100%
    confidence_level: str # "Strong data coverage", "Partial data coverage", "Limited comparison"
    components: ComponentScores
    features: RegionFeatureVector
    strongest_matches: List[str]
    major_differences: List[str]
    exploration_suitability: Dict[str, str] # e.g., {"rover_mobility": "High", "drilling_isru": "Moderate", ...}
    geological_context: str
    real_world_missions: List[str]
    rank: int

class AnalysisRequest(BaseModel):
    planet: str
    region_id: Optional[str] = None
    latitude: float
    longitude: float
    radius_km: float = Field(50.0, ge=5.0, le=500.0)
    weights: SimilarityWeights = Field(default_factory=SimilarityWeights)
    min_confidence: Optional[float] = 0.5
    filter_environment: Optional[str] = "all"
    continent_filter: Optional[str] = "all"
    country_filter: Optional[str] = "all"
    lithology_filter: Optional[str] = "all"
    diversity_balanced: bool = True
    use_benchmark_catalog: bool = False
    limit: int = Field(12, ge=1, le=50)

class AnalysisResult(BaseModel):
    analysis_id: str
    created_at: str
    reference_planet: str
    reference_name: str
    reference_coordinates: Dict[str, float]
    radius_km: float
    weights_used: SimilarityWeights
    reference_features: RegionFeatureVector
    candidates: List[AnalogCandidate]
    total_candidates_searched: int
    computation_time_ms: float
    scientific_summary: str
    database_mode: str = "Global Spatial Database"
    diversity_balanced: bool = True
    continents_represented: List[str] = []
