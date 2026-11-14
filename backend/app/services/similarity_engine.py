"""
TerraTwin AI/ML Planetary Analog Similarity Engine.
Scientifically defensible multidimensional similarity calculation between
planetary reference regions (Moon, Mars) and terrestrial candidate environments.
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Any, Optional
from ..models.features import RegionFeatureVector
from ..models.similarity import (
    SimilarityWeights, ComponentScores, AnalogCandidate,
    AnalysisResult, FeatureDifference
)
from ..data.dataset_catalog import EARTH_ANALOG_CATALOG, PLANETARY_SYSTEM
from .geo_engine import GeoEngine

# Petrological & Geochemical Compatibility Matrix
# Evaluates compatibility between terrestrial lithologies and extraterrestrial crustal units.
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

# Empirical Standard Deviations (Sigma) for robust Z-score feature scaling across analog environments
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
    """Scientific similarity calculation and ranking engine."""

    @staticmethod
    def get_lithology_compatibility(lith1: str, lith2: str) -> float:
        """Query bidirectional lithological compatibility score (0.0 to 1.0)."""
        key1 = (lith1, lith2)
        key2 = (lith2, lith1)
        if key1 in LITHOLOGY_COMPATIBILITY:
            return LITHOLOGY_COMPATIBILITY[key1]
        if key2 in LITHOLOGY_COMPATIBILITY:
            return LITHOLOGY_COMPATIBILITY[key2]
        return 0.30 # Baseline geological disparity

    @classmethod
    def compute_topography_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        """
        Compute weighted Euclidean distance across normalized topographic parameters.
        Returns similarity percentage (0-100), strong matches, and notable divergences.
        """
        t_ref = ref.topography
        t_cand = cand.topography

        diffs = [
            ("Mean Slope", (t_ref.slope_mean.value - t_cand.slope_mean.value) / FEATURE_SIGMAS["slope_mean"], 0.25),
            ("Peak Slope (p90)", (t_ref.slope_p90.value - t_cand.slope_p90.value) / FEATURE_SIGMAS["slope_p90"], 0.20),
            ("Terrain Roughness (TRI)", (t_ref.terrain_roughness.value - t_cand.terrain_roughness.value) / FEATURE_SIGMAS["terrain_roughness"], 0.25),
            ("Topographic Relief", (t_ref.relief_m.value - t_cand.relief_m.value) / FEATURE_SIGMAS["relief_m"], 0.15),
            ("Elevation Standard Deviation", (t_ref.elevation_std.value - t_cand.elevation_std.value) / FEATURE_SIGMAS["elevation_std"], 0.15),
        ]

        # Weighted squared Euclidean distance
        weighted_sq_dist = sum(weight * (norm_delta ** 2) for _, norm_delta, weight in diffs)
        euclidean_dist = math.sqrt(weighted_sq_dist)

        # Convert distance to similarity score via exponential decay: S = 100 * exp(-D / 1.5)
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
        """
        Compute petrological and mineralogical similarity.
        """
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
        """
        Compare diurnal temperature swing and thermal inertia.
        Normalizes for absolute atmospheric baseline differences (Earth 1 atm vs Mars 6 mbar vs Lunar vacuum).
        """
        th_ref = ref.thermal
        th_cand = cand.thermal

        # Diurnal swing normalized comparison
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
            divergences.append(f"Substantial thermal diurnal swing difference (Δ = {abs(th_ref.diurnal_range_k.value - th_cand.diurnal_range_k.value):.0f} K)")

        return therm_score, strong_matches, divergences

    @classmethod
    def compute_surface_similarity(cls, ref: RegionFeatureVector, cand: RegionFeatureVector) -> Tuple[float, List[str], List[str]]:
        """
        Compare optical albedo, bare ground fraction, and sub-meter rock obstacle roughness.
        """
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
            strong_matches.append("Near-identical bare ground and lack of vegetative canopy")
        if rough_delta < 0.4:
            strong_matches.append("Equivalent sub-meter rock boulder obstacle distribution")
        if albedo_delta > 1.2:
            divergences.append("Optical surface reflectance / albedo disparity")

        return surf_score, strong_matches, divergences

    @classmethod
    def rank_candidates(cls, ref_vector: RegionFeatureVector,
                        weights: Optional[SimilarityWeights] = None,
                        top_n: int = 8) -> List[AnalogCandidate]:
        """
        Score and rank Earth analog candidates against the reference planetary region.
        """
        if weights is None:
            weights = SimilarityWeights()

        # Normalize weights to sum to 1.0
        w_sum = weights.topography_weight + weights.geology_weight + weights.thermal_weight + weights.surface_weight
        w_topo = weights.topography_weight / w_sum
        w_geol = weights.geology_weight / w_sum
        w_therm = weights.thermal_weight / w_sum
        w_surf = weights.surface_weight / w_sum

        candidates_scored = []

        for analog_def in EARTH_ANALOG_CATALOG:
            # Extract features for candidate
            cand_vector = GeoEngine.extract_features(
                planet="earth",
                lat=analog_def["latitude"],
                lon=analog_def["longitude"],
                radius_km=50.0,
                custom_name=analog_def["name"]
            )

            # Compute component similarities
            topo_sim, t_matches, t_divs = cls.compute_topography_similarity(ref_vector, cand_vector)
            geol_sim, g_matches, g_divs = cls.compute_geological_similarity(ref_vector, cand_vector)
            therm_sim, th_matches, th_divs = cls.compute_thermal_similarity(ref_vector, cand_vector)
            surf_sim, s_matches, s_divs = cls.compute_surface_similarity(ref_vector, cand_vector)

            # Weighted overall score
            overall = round(
                w_topo * topo_sim +
                w_geol * geol_sim +
                w_therm * therm_sim +
                w_surf * surf_sim,
                1
            )

            all_strong = t_matches + g_matches + th_matches + s_matches
            all_divs = t_divs + g_divs + th_divs + s_divs

            # Confidence level determination
            data_cov = (ref_vector.data_coverage_score + cand_vector.data_coverage_score) / 2.0
            if data_cov >= 0.90:
                conf_level = "Strong data coverage"
            elif data_cov >= 0.75:
                conf_level = "Partial data coverage"
            else:
                conf_level = "Limited comparison"

            candidate = AnalogCandidate(
                candidate_id=analog_def["id"],
                name=analog_def["name"],
                country=analog_def["country"],
                latitude=analog_def["latitude"],
                longitude=analog_def["longitude"],
                elevation_m=analog_def["elevation_m"],
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
                exploration_suitability=analog_def["exploration_suitability"],
                geological_context=analog_def["geological_context"],
                real_world_missions=analog_def["real_world_missions"],
                rank=0 # updated after sorting
            )
            candidates_scored.append(candidate)

        # Sort descending by overall similarity
        candidates_scored.sort(key=lambda c: c.overall_similarity, reverse=True)

        # Assign ranks
        for idx, cand in enumerate(candidates_scored):
            cand.rank = idx + 1

        return candidates_scored[:top_n]
