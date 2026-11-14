"""
TerraTwin AI Scientific Research Assistant.
Generates grounded scientific explanations, answers mission testbed queries,
and synthesizes exploration recommendations using real calculated parameters.
"""

import os
from typing import Dict, Any, List, Optional
from ..models.similarity import AnalogCandidate
from ..models.features import RegionFeatureVector
from ..data.dataset_catalog import PLANETARY_SYSTEM

class AIAssistant:
    """Scientific reasoning and exploration advisory engine."""

    @classmethod
    def generate_explanation(cls, ref_vector: RegionFeatureVector, candidate: AnalogCandidate) -> Dict[str, Any]:
        """
        Generate comprehensive, scientifically defensible synthesis of the analog pairing.
        Includes rover mobility, drilling/ISRU, sensor testing, and environmental differences.
        """
        planet_name = ref_vector.planet.capitalize()
        planet_data = PLANETARY_SYSTEM[ref_vector.planet]

        # Topographical analysis
        slope_ref = ref_vector.topography.slope_mean.value
        slope_cand = candidate.features.topography.slope_mean.value
        slope_delta = abs(slope_ref - slope_cand)

        rough_ref = ref_vector.topography.terrain_roughness.value
        rough_cand = candidate.features.topography.terrain_roughness.value

        # Petrological analysis
        lith_ref = ref_vector.geology.rock_type
        lith_cand = candidate.features.geology.rock_type

        # Thermal analysis
        diurnal_ref = ref_vector.thermal.diurnal_range_k.value
        diurnal_cand = candidate.features.thermal.diurnal_range_k.value

        # Synthesis reasoning
        why_selected = (
            f"{candidate.name} ({candidate.country}) was identified as a leading Earth analog for {ref_vector.name} on {planet_name} "
            f"with an overall quantitative similarity index of {candidate.overall_similarity}%. "
            f"The primary alignment is driven by a {candidate.components.topography_similarity}% topographic congruence "
            f"(mean slope: {slope_cand:.1f}° on Earth vs {slope_ref:.1f}° on {planet_name}; Δ = {slope_delta:.1f}°) and "
            f"a {candidate.components.geological_similarity}% geological compatibility between {candidate.features.geology.lithology_category.replace('_', ' ')} "
            f"and extraterrestrial {ref_vector.geology.lithology_category.replace('_', ' ')} crustal units."
        )

        rover_mobility_suitability = (
            f"Terrain Ruggedness Index is {rough_cand:.1f} TRI (Earth) versus {rough_ref:.1f} TRI ({planet_name}). "
            f"With a 90th percentile peak slope of {candidate.features.topography.slope_p90.value:.1f}° (reference: {ref_vector.topography.slope_p90.value:.1f}°), "
            f"this environment offers realistic terramechanics stress for wheel traction, slope slip prediction, "
            f"and autonomous hazard avoidance against rocky obstacle fields."
        )

        drilling_isru_suitability = (
            f"Subsurface sampling conditions: {candidate.features.geology.mineralogy_summary}. "
            f"Testing robotic rotary-percussive drills or regolith scoop mechanisms here will accurately simulate mechanical resistance "
            f"and bit abrasion experienced when encountering {ref_vector.geology.rock_type}."
        )

        # Environmental disclaimers (fundamental physics differences)
        gravity_ratio = candidate.features.topography.slope_mean.value # placeholder
        g_earth = PLANETARY_SYSTEM["earth"]["physical"]["surface_gravity_ms2"]
        g_ref = planet_data["physical"]["surface_gravity_ms2"]
        p_earth = PLANETARY_SYSTEM["earth"]["physical"]["atmospheric_pressure_hpa"]
        p_ref = planet_data["physical"]["atmospheric_pressure_hpa"]

        environmental_differences = [
            f"Gravity Disparity: Earth surface gravity is {g_earth:.2f} m/s² compared to {g_ref:.2f} m/s² on {planet_name} ({g_ref/g_earth*100:.1f}% of 1g). Rover suspension travel and regolith ejection dynamics will differ.",
            f"Atmospheric Pressure: Earth ambient pressure is {p_earth:.1f} hPa versus {'hard vacuum (<10^-10 hPa)' if p_ref < 0.01 else f'{p_ref:.1f} hPa'} on {planet_name}. Aerodynamic drag, convective cooling, and volatile phase stability cannot be replicated outdoors.",
            f"Cosmic Radiation & Photolysis: Earth is protected by an active ~45 µT magnetosphere and thick atmosphere. Unattenuated solar UV-C and galactic cosmic ray fluxes (GCR) present on {planet_name} must be simulated in vacuum chambers.",
            f"Diurnal Thermal Extremes: Diurnal amplitude is {diurnal_cand:.1f} K on Earth versus {diurnal_ref:.1f} K on {planet_name} (Δ = {abs(diurnal_ref - diurnal_cand):.1f} K)."
        ]

        # Recommended future investigations
        recommended_research = [
            f"Conduct in-situ high-resolution drone photogrammetry over {candidate.name} to produce cm-scale digital terrain models for fine wheel-rock interaction modeling.",
            f"Perform laboratory X-ray diffraction (XRD) and Raman spectroscopy on {candidate.name} field samples to calibrate flight spectrometers against {lith_ref}.",
            f"Utilize environmental thermal-vacuum chambers (TVAC) to bridge the {abs(diurnal_ref - diurnal_cand):.0f} K thermal swing difference between Earth and {planet_name}."
        ]

        return {
            "candidate_id": candidate.candidate_id,
            "candidate_name": candidate.name,
            "reference_name": ref_vector.name,
            "reference_planet": planet_name,
            "overall_similarity": candidate.overall_similarity,
            "why_selected": why_selected,
            "rover_mobility": rover_mobility_suitability,
            "drilling_isru": drilling_isru_suitability,
            "environmental_differences": environmental_differences,
            "recommended_research": recommended_research,
            "real_world_missions": candidate.real_world_missions,
            "key_alignments": candidate.strongest_matches,
            "primary_divergences": candidate.major_differences
        }

    @classmethod
    def answer_query(cls, ref_vector: RegionFeatureVector, candidate: AnalogCandidate, question: str) -> str:
        """
        Answer targeted user questions regarding test suitability, equipment, or science.
        """
        q = question.lower()
        if "rover" in q or "mobility" in q or "wheel" in q or "traction" in q:
            return (
                f"**Rover Mobility Assessment for {candidate.name}:**\n\n"
                f"- **Slope Characteristics:** Mean slope is {candidate.features.topography.slope_mean.value:.1f}° with peak slopes reaching {candidate.features.topography.slope_p90.value:.1f}°, closely matching {ref_vector.name}'s profile ({ref_vector.topography.slope_mean.value:.1f}° mean).\n"
                f"- **Surface Obstacles:** Sub-meter rock roughness is estimated at {candidate.features.surface.roughness_submeter.value:.2f} m, providing realistic obstacle density for hazard detection sensors (LiDAR/Stereo cameras).\n"
                f"- **Caveat:** Earth's 1g gravity ({PLANETARY_SYSTEM['earth']['physical']['surface_gravity_ms2']} m/s²) provides greater wheel ground pressure than {ref_vector.planet.capitalize()} ({PLANETARY_SYSTEM[ref_vector.planet]['physical']['surface_gravity_ms2']} m/s²). Off-weighting rigs or reduced tire pressures are recommended during testing."
            )
        elif "drill" in q or "isru" in q or "sample" in q or "water" in q:
            return (
                f"**Drilling & In-Situ Resource Utilization (ISRU) Evaluation:**\n\n"
                f"- **Lithological Target:** {candidate.features.geology.rock_type}.\n"
                f"- **Mineral Composition:** {candidate.features.geology.mineralogy_summary}.\n"
                f"- **Application:** Highly appropriate for testing rotary-percussive core extraction, cutting bit thermal dissipation, and autonomous caching mechanisms simulating operations on {ref_vector.name}."
            )
        elif "difference" in q or "gravity" in q or "atmosphere" in q:
            diffs = "\n".join([f"- {d}" for d in candidate.major_differences])
            return (
                f"**Critical Scientific Differences to Account For:**\n\n"
                f"{diffs}\n\n"
                f"Remember: Earth cannot simulate {ref_vector.planet.capitalize()}'s atmospheric pressure or partial gravity in open-air field conditions."
            )
        else:
            return (
                f"**Scientific Analog Summary:**\n\n"
                f"{candidate.name} is a {candidate.overall_similarity}% quantitative match to {ref_vector.name}. "
                f"Topography matches at {candidate.components.topography_similarity}%, geology at {candidate.components.geological_similarity}%, "
                f"and surface albedo/bare ground at {candidate.components.surface_similarity}%. "
                f"Historically utilized in: {', '.join(candidate.real_world_missions)}."
            )
