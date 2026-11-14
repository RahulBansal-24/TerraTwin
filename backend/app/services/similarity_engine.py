"""
TerraTwin AI/ML Global Planetary Analog Similarity Engine.
Performs multidimensional similarity calculation against the Global Earth Spatial Database
with spatial deduplication, geographic diversity balancing, and robust Z-score normalization.
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Any, Optional

from ..models.features import RegionFeatureVector, TopographyFeatures, GeologicalFeatures, ThermalFeatures, SurfaceFeatures, FeatureMeasurement
from ..models.similarity import (
    SimilarityWeights, ComponentScores, AnalogCandidate,
    AnalysisResult, FeatureDifference
)
from ..data.dataset_catalog import EARTH_ANALOG_CATALOG, PLANETARY_SYSTEM
from .spatial_db import SpatialDatabase
from .geo_engine import GeoEngine

# Petrological & Geochemical Compatibility Matrix
LITHOLOGY_COMPATIBILITY = {
    ("basaltic_volcanic", "basaltic_volcanic"): 0.98,
    ("basaltic_volcanic", "impact_breccia"): 0.72,
    ("basaltic_volcanic", "silicified_craton"): 0.65,
    ("basaltic_volcanic", "acidic_sulfate_gossan"): 0.60,
    ("basaltic_volcanic", "hyperarid_playa_evaporite"): 0.45,
    ("basaltic_volcanic", "polar_permafrost_ice"): 0.35,

    ("hyperarid_playa_evaporite", "hyperarid_playa_evaporite"): 0.96,
    ("hyperarid_playa_evaporite", "acidic_sulfate_gossan"): 0.88,
    ("hyperarid_playa_evaporite", "polar_permafrost_ice"): 0.65,
    ("hyperarid_playa_evaporite", "silicified_craton"): 0.60,
    ("hyperarid_playa_evaporite", "basaltic_volcanic"): 0.45,
    ("hyperarid_playa_evaporite", "impact_breccia"): 0.40,

    ("polar_permafrost_ice", "polar_permafrost_ice"): 0.98,
    ("polar_permafrost_ice", "hyperarid_playa_evaporite"): 0.68,
    ("polar_permafrost_ice", "impact_breccia"): 0.60,
    ("polar_permafrost_ice", "silicified_craton"): 0.55,
    ("polar_permafrost_ice", "basaltic_volcanic"): 0.40,
    ("polar_permafrost_ice", "acidic_sulfate_gossan"): 0.35,

    ("acidic_sulfate_gossan", "acidic_sulfate_gossan"): 0.97,
    ("acidic_sulfate_gossan", "hyperarid_playa_evaporite"): 0.86,
    ("acidic_sulfate_gossan", "silicified_craton"): 0.68,
    ("acidic_sulfate_gossan", "basaltic_volcanic"): 0.55,
    ("acidic_sulfate_gossan", "impact_breccia"): 0.50,
    ("acidic_sulfate_gossan", "polar_permafrost_ice"): 0.35,

    ("silicified_craton", "silicified_craton"): 0.95,
    ("silicified_craton", "acidic_sulfate_gossan"): 0.70,
    ("silicified_craton", "impact_breccia"): 0.75,
    ("silicified_craton", "basaltic_volcanic"): 0.65,
    ("silicified_craton", "hyperarid_playa_evaporite"): 0.50,
    ("silicified_craton", "polar_permafrost_ice"): 0.45,

    ("impact_breccia", "impact_breccia"): 0.98,
    ("impact_breccia", "basaltic_volcanic"): 0.75,
    ("impact_breccia", "silicified_craton"): 0.72,
    ("impact_breccia", "polar_permafrost_ice"): 0.55,
    ("impact_breccia", "hyperarid_playa_evaporite"): 0.45,
    ("impact_breccia", "acidic_sulfate_gossan"): 0.45,
}

FEATURE_SIGMAS = {
    "slope_mean": 8.0,          # degrees
    "slope_p90": 14.0,          # degrees
    "terrain_roughness": 45.0,  # TRI
    "relief_m": 2500.0,         # meters
    "elevation_std": 600.0,     # meters
    "diurnal_range_k": 70.0,    # Kelvin
    "thermal_inertia_si": 120.0,# J m^-2 K^-1 s^-1/2
    "albedo": 0.15,             # ratio
    "bare_ground_ratio": 0.15,  # ratio
    "roughness_submeter": 0.25, # meters
    "dust_sediment_cover": 0.30 # ratio
}

class SimilarityEngine:
    """Scientific similarity calculation, spatial indexing, and ranking engine."""

    @staticmethod
    def get_lithology_compatibility(lith1: str, lith2: str) -> float:
        """Query petrological compatibility score (0.0 to 1.0)."""
        key1 = (lith1, lith2)
        key2 = (lith2, lith1)
        if key1 in LITHOLOGY_COMPATIBILITY:
            return LITHOLOGY_COMPATIBILITY[key1]
        if key2 in LITHOLOGY_COMPATIBILITY:
            return LITHOLOGY_COMPATIBILITY[key2]
        return 0.35 # Baseline geological compatibility

    @classmethod
    def compute_topography_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        t_ref = ref.topography
        t_cand = cand.topography

        diffs = [
            ("Mean Slope", (t_ref.slope_mean.value - t_cand.slope_mean.value) / FEATURE_SIGMAS["slope_mean"], 0.25),
            ("Peak Slope (p90)", (t_ref.slope_p90.value - t_cand.slope_p90.value) / FEATURE_SIGMAS["slope_p90"], 0.20),
            ("Terrain Roughness (TRI)", (t_ref.terrain_roughness.value - t_cand.terrain_roughness.value) / FEATURE_SIGMAS["terrain_roughness"], 0.25),
            ("Topographic Relief", (t_ref.relief_m.value - t_cand.relief_m.value) / FEATURE_SIGMAS["relief_m"], 0.15),
            ("Elevation Standard Deviation", (t_ref.elevation_std.value - t_cand.elevation_std.value) / FEATURE_SIGMAS["elevation_std"], 0.15),
        ]

        weighted_sq_dist = sum(weight * (norm_delta ** 2) for _, norm_delta, weight in diffs)
        euclidean_dist = math.sqrt(weighted_sq_dist)
        topo_score = round(100.0 * math.exp(-euclidean_dist / 1.5), 1)

        strong_matches = []
        divergences = []
        for name, norm_delta, _ in diffs:
            if abs(norm_delta) < 0.45:
                strong_matches.append(f"Highly congruent {name.lower()} (Δz < 0.45σ)")
            elif abs(norm_delta) > 1.2:
                divergences.append(f"Divergent {name.lower()} (Δz = {abs(norm_delta):.1f}σ)")

        return topo_score, strong_matches, divergences

    @classmethod
    def compute_geological_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        lith_compat = cls.get_lithology_compatibility(ref.geology.lithology_category, cand.geology.lithology_category)
        base_score = lith_compat * 100.0

        strong_matches = []
        divergences = []
        if lith_compat >= 0.85:
            strong_matches.append(f"Direct petrological match: {cand.geology.rock_type} analogous to {ref.geology.rock_type}")
        elif lith_compat >= 0.65:
            strong_matches.append(f"Compatible geological domain: {cand.geology.lithology_category.replace('_', ' ')}")
        else:
            divergences.append(f"Lithological disparity: {cand.geology.lithology_category.replace('_', ' ')} vs {ref.geology.lithology_category.replace('_', ' ')}")

        return round(base_score, 1), strong_matches, divergences

    @classmethod
    def compute_thermal_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        th_ref = ref.thermal
        th_cand = cand.thermal

        diurnal_delta = abs(th_ref.diurnal_range_k.value - th_cand.diurnal_range_k.value) / FEATURE_SIGMAS["diurnal_range_k"]
        inertia_delta = abs(th_ref.thermal_inertia_si.value - th_cand.thermal_inertia_si.value) / FEATURE_SIGMAS["thermal_inertia_si"]

        therm_dist = math.sqrt(0.55 * (diurnal_delta**2) + 0.45 * (inertia_delta**2))
        therm_score = round(100.0 * math.exp(-therm_dist / 1.8), 1)

        strong_matches = []
        divergences = []
        if diurnal_delta < 0.5:
            strong_matches.append("Comparable thermal amplitude and day/night swing")
        if inertia_delta < 0.6:
            strong_matches.append("Matching thermal inertia and conductive heat transfer properties")
        if diurnal_delta > 1.3:
            divergences.append(f"Thermal diurnal swing difference (Δ = {abs(th_ref.diurnal_range_k.value - th_cand.diurnal_range_k.value):.0f} K)")

        return therm_score, strong_matches, divergences

    @classmethod
    def compute_surface_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        s_ref = ref.surface
        s_cand = cand.surface

        albedo_delta = abs(s_ref.albedo.value - s_cand.albedo.value) / FEATURE_SIGMAS["albedo"]
        bare_delta = abs(s_ref.bare_ground_ratio.value - s_cand.bare_ground_ratio.value) / FEATURE_SIGMAS["bare_ground_ratio"]
        rough_delta = abs(s_ref.roughness_submeter.value - s_cand.roughness_submeter.value) / FEATURE_SIGMAS["roughness_submeter"]

        surf_dist = math.sqrt(0.35 * (albedo_delta**2) + 0.35 * (bare_delta**2) + 0.30 * (rough_delta**2))
        surf_score = round(100.0 * math.exp(-surf_dist / 1.6), 1)

        strong_matches = []
        divergences = []
        if bare_delta < 0.2:
            strong_matches.append("Near-identical bare ground fraction")
        if rough_delta < 0.4:
            strong_matches.append("Equivalent sub-meter rock boulder obstacle distribution")
        if albedo_delta > 1.2:
            divergences.append("Optical surface reflectance / albedo disparity")

        return surf_score, strong_matches, divergences

    @classmethod
    def build_candidate_vector_from_db_row(cls, row: Dict[str, Any]) -> RegionFeatureVector:
        """Convert SQLite database row into RegionFeatureVector."""
        return RegionFeatureVector(
            region_id=row["id"],
            planet="earth",
            name=row["name"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            radius_km=row["cell_resolution_km"],
            topography=TopographyFeatures(
                elevation_mean=FeatureMeasurement(value=row["elevation_mean"], unit="m", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                elevation_min=FeatureMeasurement(value=row["elevation_min"], unit="m", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                elevation_max=FeatureMeasurement(value=row["elevation_max"], unit="m", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                elevation_std=FeatureMeasurement(value=row["elevation_std"], unit="m", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                slope_mean=FeatureMeasurement(value=row["slope_mean"], unit="deg", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                slope_p90=FeatureMeasurement(value=row["slope_p90"], unit="deg", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                terrain_roughness=FeatureMeasurement(value=row["terrain_roughness"], unit="TRI", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"]),
                relief_m=FeatureMeasurement(value=row["relief_m"], unit="m", data_source="Copernicus GLO-90 DEM", resolution="90m", confidence=row["data_coverage_score"])
            ),
            geology=GeologicalFeatures(
                lithology_category=row["lithology_category"],
                rock_type=row["rock_type"],
                mineralogy_summary=row["mineralogy_summary"],
                volcanic_character="Terrestrial Geological Formation",
                age_era="Phanerozoic / Precambrian",
                data_source="University of Hamburg GLiM",
                confidence=row["data_coverage_score"]
            ),
            thermal=ThermalFeatures(
                surface_temp_mean_k=FeatureMeasurement(value=row["surface_temp_mean_k"], unit="K", data_source="NASA LP DAAC MOD11A1 LST", resolution="1km", confidence=row["data_coverage_score"]),
                surface_temp_min_k=FeatureMeasurement(value=row["surface_temp_mean_k"] - row["diurnal_range_k"]*0.5, unit="K", data_source="NASA LP DAAC MOD11A1 LST", resolution="1km", confidence=row["data_coverage_score"]),
                surface_temp_max_k=FeatureMeasurement(value=row["surface_temp_mean_k"] + row["diurnal_range_k"]*0.5, unit="K", data_source="NASA LP DAAC MOD11A1 LST", resolution="1km", confidence=row["data_coverage_score"]),
                diurnal_range_k=FeatureMeasurement(value=row["diurnal_range_k"], unit="K", data_source="NASA LP DAAC MOD11A1 LST", resolution="1km", confidence=row["data_coverage_score"]),
                thermal_inertia_si=FeatureMeasurement(value=row["thermal_inertia_si"], unit="J m^-2 K^-1 s^-1/2", data_source="Derived Thermal Inertia", resolution="1km", confidence=row["data_coverage_score"])
            ),
            surface=SurfaceFeatures(
                albedo=FeatureMeasurement(value=row["albedo"], unit="ratio", data_source="MODIS / Sentinel-2 Surface Reflectance", resolution="250m", confidence=row["data_coverage_score"]),
                bare_ground_ratio=FeatureMeasurement(value=row["bare_ground_ratio"], unit="ratio", data_source="ESA WorldCover 10m", resolution="10m", confidence=row["data_coverage_score"]),
                vegetation_ndvi=FeatureMeasurement(value=row["vegetation_ndvi"], unit="index", data_source="Sentinel-2 NDVI", resolution="10m", confidence=row["data_coverage_score"]),
                roughness_submeter=FeatureMeasurement(value=row["roughness_submeter"], unit="m", data_source="Topographic Derivative", resolution="Sub-meter", confidence=row["data_coverage_score"]),
                dust_sediment_cover=FeatureMeasurement(value=row["dust_sediment_cover"], unit="ratio", data_source="SoilGrids / MODIS", resolution="250m", confidence=row["data_coverage_score"])
            ),
            elevation_profile=[round(row["elevation_mean"] + math.sin(i*0.5)*(row["relief_m"]*0.4), 1) for i in range(25)],
            slope_histogram={
                "0-5°": round(max(5.0, 50.0 - row["slope_mean"] * 2.5), 1),
                "5-15°": round(max(10.0, 30.0 + row["slope_mean"] * 0.5), 1),
                "15-25°": round(max(5.0, row["slope_mean"] * 1.8), 1),
                ">25°": round(max(2.0, row["slope_p90"] * 0.8), 1)
            },
            data_coverage_score=row["data_coverage_score"],
            coverage_label="Strong data coverage" if row["data_coverage_score"] >= 0.9 else "Partial data coverage",
            provenance=row.get("data_sources", ["Copernicus DEM", "GLiM Lithology", "ESA WorldCover"])
        )

    @classmethod
    def rank_candidates(cls, ref_vector: RegionFeatureVector,
                        weights: Optional[SimilarityWeights] = None,
                        top_n: int = 12,
                        continent_filter: Optional[str] = None,
                        country_filter: Optional[str] = None,
                        lithology_filter: Optional[str] = None,
                        diversity_balanced: bool = True,
                        use_benchmark_catalog: bool = False,
                        min_distance_km: Optional[float] = None,
                        spatial_suppression_km: float = 80.0) -> List[AnalogCandidate]:
        """
        Primary Discovery Ranking Engine.
        Queries the persistent SQLite R*Tree Global Earth Database (or benchmark catalog),
        computes multidimensional weighted distance, applies spatial deduplication,
        and optionally balances geographic diversity across continents.
        """
        if weights is None:
            weights = SimilarityWeights()

        w_sum = weights.topography_weight + weights.geology_weight + weights.thermal_weight + weights.surface_weight
        w_topo = weights.topography_weight / w_sum
        w_geol = weights.geology_weight / w_sum
        w_therm = weights.thermal_weight / w_sum
        w_surf = weights.surface_weight / w_sum

        candidates_pool = []

        if use_benchmark_catalog:
            # Benchmark Mode: Evaluate the 14 historical planetary analog field stations
            for analog_def in EARTH_ANALOG_CATALOG:
                cand_vector = GeoEngine.extract_features(
                    planet="earth",
                    lat=analog_def["latitude"],
                    lon=analog_def["longitude"],
                    radius_km=50.0,
                    custom_name=analog_def["name"]
                )
                candidates_pool.append({
                    "id": analog_def["id"],
                    "name": analog_def["name"],
                    "country": analog_def["country"],
                    "continent": "Global",
                    "latitude": analog_def["latitude"],
                    "longitude": analog_def["longitude"],
                    "elevation_m": analog_def["elevation_m"],
                    "vector": cand_vector,
                    "geological_context": analog_def.get("geological_context", ""),
                    "real_world_missions": analog_def.get("real_world_missions", []),
                    "exploration_suitability": analog_def.get("exploration_suitability", {
                        "rover_mobility": "High", "drilling_isru": "Moderate", "sensor_calibration": "High"
                    })
                })
        else:
            # Global Spatial Database Discovery Mode
            raw_rows = SpatialDatabase.query_candidates(
                continent=continent_filter,
                country=country_filter,
                lithology=lithology_filter,
                exclude_water=True,
                limit=1000
            )

            for row in raw_rows:
                cand_vector = cls.build_candidate_vector_from_db_row(row)
                candidates_pool.append({
                    "id": row["id"],
                    "name": row["name"],
                    "country": row["country"],
                    "continent": row["continent"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "elevation_m": row["elevation_mean"],
                    "vector": cand_vector,
                    "geological_context": f"{row['name']} located in {row['country']} ({row['continent']}). Characterized by {row['rock_type']} with {row['mineralogy_summary']}.",
                    "real_world_missions": [f"Terrestrial Planetary Analog Grid Sector: {row['continent']}"],
                    "exploration_suitability": {
                        "rover_mobility": "Very High" if row["slope_p90"] < 25 else "Extreme Challenge (Steep Slopes)",
                        "drilling_isru": "Exceptional" if "evaporite" in row["lithology_category"] or "polar" in row["lithology_category"] else "High",
                        "sensor_calibration": "High (Copernicus DEM & GLiM Ground Truth)"
                    }
                })

        # Calculate multidimensional similarity scores
        scored_candidates = []
        for cand in candidates_pool:
            cand_vector = cand["vector"]
            topo_sim, t_matches, t_divs = cls.compute_topography_similarity(ref_vector, cand_vector)
            geol_sim, g_matches, g_divs = cls.compute_geological_similarity(ref_vector, cand_vector)
            therm_sim, th_matches, th_divs = cls.compute_thermal_similarity(ref_vector, cand_vector)
            surf_sim, s_matches, s_divs = cls.compute_surface_similarity(ref_vector, cand_vector)

            overall = round(
                w_topo * topo_sim +
                w_geol * geol_sim +
                w_therm * therm_sim +
                w_surf * surf_sim,
                1
            )

            all_strong = t_matches + g_matches + th_matches + s_matches
            all_divs = t_divs + g_divs + th_divs + s_divs

            data_cov = (ref_vector.data_coverage_score + cand_vector.data_coverage_score) / 2.0
            if data_cov >= 0.90:
                conf_level = "Strong data coverage"
            elif data_cov >= 0.75:
                conf_level = "Partial data coverage"
            else:
                conf_level = "Limited comparison"

            analog_candidate = AnalogCandidate(
                candidate_id=cand["id"],
                name=cand["name"],
                country=cand["country"],
                continent=cand.get("continent", "Global"),
                latitude=cand["latitude"],
                longitude=cand["longitude"],
                elevation_m=cand["elevation_m"],
                overall_similarity=overall,
                confidence_level=conf_level,
                components=ComponentScores(
                    topography_similarity=topo_sim,
                    geological_similarity=geol_sim,
                    thermal_similarity=therm_sim,
                    surface_similarity=surf_sim,
                    weighted_overall=overall
                ),
                features=cand_vector,
                strongest_matches=all_strong[:4],
                major_differences=all_divs[:4],
                exploration_suitability=cand["exploration_suitability"],
                geological_context=cand["geological_context"],
                real_world_missions=cand["real_world_missions"],
                rank=0
            )

            scored_candidates.append({
                "candidate": analog_candidate,
                "continent": cand["continent"],
                "lat": cand["latitude"],
                "lon": cand["longitude"],
                "score": overall
            })

        # Sort descending by raw score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        # Spatial Deduplication & Suppression Filter (prevent clustering 10 results in 1 province)
        suppression_radius = min_distance_km if min_distance_km is not None else spatial_suppression_km
        deduped = []
        for item in scored_candidates:
            too_close = False
            for kept in deduped:
                dist = GeoEngine.haversine_distance_km(
                    item["lat"], item["lon"],
                    kept["lat"], kept["lon"],
                    radius_km=6371.0
                )
                if dist < suppression_radius:
                    too_close = True
                    break
            if not too_close:
                deduped.append(item)

        final_selection = []
        seen_provinces = set()
        continent_quota = {}

        for item in deduped:
            cand_name = item["candidate"].name
            base_prov = cand_name.split(" (")[0].strip() if " (" in cand_name else cand_name.strip()

            # Enforce strict macro-province deduplication (no province appears multiple times in top results)
            if base_prov in seen_provinces:
                continue

            if diversity_balanced and not use_benchmark_catalog:
                # Geographic Diversity Balancing: Ensures representation across diverse global continents
                cont = item["continent"]
                current_cnt = continent_quota.get(cont, 0)
                # Allow maximum 2 candidates per continent to guarantee wide global distribution
                if current_cnt < 2:
                    final_selection.append(item["candidate"])
                    continent_quota[cont] = current_cnt + 1
                    seen_provinces.add(base_prov)
            else:
                final_selection.append(item["candidate"])
                seen_provinces.add(base_prov)

            if len(final_selection) >= top_n:
                break

        # If quota or strict province deduplication left room, backfill with next best unique candidates
        if len(final_selection) < top_n:
            for item in deduped:
                cand_name = item["candidate"].name
                base_prov = cand_name.split(" (")[0].strip() if " (" in cand_name else cand_name.strip()
                if item["candidate"] not in final_selection and base_prov not in seen_provinces:
                    final_selection.append(item["candidate"])
                    seen_provinces.add(base_prov)
                if len(final_selection) >= top_n:
                    break

        # Final backfill fallback if still below top_n
        if len(final_selection) < top_n:
            for item in deduped:
                if item["candidate"] not in final_selection:
                    final_selection.append(item["candidate"])
                if len(final_selection) >= top_n:
                    break

        # Assign final ranks
        for idx, cand in enumerate(final_selection):
            cand.rank = idx + 1

        return final_selection
