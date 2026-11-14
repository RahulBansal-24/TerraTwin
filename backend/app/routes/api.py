"""
TerraTwin REST API Endpoints.
Provides complete programmatic access to planetary models, region extraction,
global similarity ranking, candidate comparison, AI insights, and PDF report generation.
"""

import os
import uuid
import time
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional

from ..data.dataset_catalog import (
    PLANETARY_SYSTEM, LUNAR_REGIONS, MARS_REGIONS,
    EARTH_ANALOG_CATALOG
)
from ..models.planet import PlanetInfo, ExplorationRegion
from ..models.features import RegionFeatureVector
from ..models.similarity import (
    AnalysisRequest, AnalysisResult, AnalogCandidate, SimilarityWeights
)
from ..services.geo_engine import GeoEngine
from ..services.similarity_engine import SimilarityEngine
from ..services.ai_assistant import AIAssistant
from ..services.report_generator import ReportGenerator
from ..services.spatial_db import SpatialDatabase
from ..services.planetary_gazetteer import PlanetaryGazetteer

router = APIRouter(prefix="/api")

# Initialize global spatial database on startup
try:
    SpatialDatabase.initialize()
except Exception as e:
    print(f"Spatial database initialization warning: {e}")

# In-memory storage for active analyses and reports
ANALYSIS_CACHE: Dict[str, AnalysisResult] = {}
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.get("/planets")
def get_planets():
    """List available planetary bodies."""
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "tagline": p["tagline"],
            "description": p["description"],
            "color_theme": p["color_theme"],
            "physical": p["physical"]
        }
        for p in PLANETARY_SYSTEM.values()
    ]

@router.get("/planets/{planet}")
def get_planet_details(planet: str):
    """Retrieve full planet metadata and featured exploration regions."""
    p_id = planet.lower()
    if p_id not in PLANETARY_SYSTEM:
        raise HTTPException(status_code=404, detail=f"Planet '{planet}' not found.")

    planet_data = PLANETARY_SYSTEM[p_id]
    regions = []
    if p_id == "moon":
        regions = LUNAR_REGIONS
    elif p_id == "mars":
        regions = MARS_REGIONS
    elif p_id == "earth":
        regions = EARTH_ANALOG_CATALOG

    return {
        **planet_data,
        "featured_regions": regions
    }

@router.get("/planets/{planet}/regions")
def get_planet_regions(planet: str):
    """Retrieve exploration regions for a specific planet."""
    p_id = planet.lower()
    if p_id == "moon":
        return LUNAR_REGIONS
    elif p_id == "mars":
        return MARS_REGIONS
    elif p_id == "earth":
        return EARTH_ANALOG_CATALOG
    else:
        raise HTTPException(status_code=404, detail=f"No exploration catalog for planet '{planet}'.")

@router.get("/planetary-features/{planet}")
def get_planetary_features(planet: str, type: Optional[str] = None, q: Optional[str] = None):
    """
    Retrieve official USGS-IAU named planetary features (Craters, Maria, Montes, Valles, Chasmata).
    """
    p_id = planet.lower()
    if p_id not in ["moon", "mars"]:
        raise HTTPException(status_code=400, detail="Planetary gazetteer supported for 'moon' and 'mars'")
    return PlanetaryGazetteer.get_features(p_id, feature_type=type, search=q)

@router.get("/database/stats")
def get_database_stats():
    """Return real statistics from the Global Earth Spatial Database."""
    try:
        return SpatialDatabase.get_stats()
    except Exception as e:
        return {
            "status": "fallback",
            "error": str(e),
            "benchmark_catalog_count": len(EARTH_ANALOG_CATALOG)
        }

@router.get("/candidates/global")
def get_global_candidates(continent: Optional[str] = None, country: Optional[str] = None,
                          lithology: Optional[str] = None, limit: int = 50):
    """Query candidates directly from the Global Earth Spatial Database."""
    return SpatialDatabase.query_candidates(
        continent=continent,
        country=country,
        lithology=lithology,
        exclude_water=True,
        limit=limit
    )

@router.get("/datasets")
def get_datasets():
    """Return scientific data catalogue with coverage, citations, and status."""
    return [
        {
            "name": "NASA LRO LOLA (Lunar Orbiter Laser Altimeter)",
            "planet": "Moon",
            "type": "Topography & Digital Elevation",
            "resolution": "64-128 pixels/degree (~15-30m)",
            "status": "Operational / Integrated",
            "coverage": "Global Lunar Coverage",
            "citation": "Smith, D. E., et al. (2010), The Lunar Orbiter Laser Altimeter Investigation on the Lunar Reconnaissance Orbiter Mission, Space Sci. Rev., 150(1-4), 209-241."
        },
        {
            "name": "NASA LRO Diviner Lunar Radiometer Experiment",
            "planet": "Moon",
            "type": "Thermal & Rock Abundance",
            "resolution": "1 km grid",
            "status": "Operational / Integrated",
            "coverage": "Global Lunar Diurnal Swings",
            "citation": "Paige, D. A., et al. (2010), The Lunar Reconnaissance Orbiter Diviner Lunar Radiometer Experiment, Space Sci. Rev., 150, 125-160."
        },
        {
            "name": "NASA MGS MOLA (Mars Orbiter Laser Altimeter)",
            "planet": "Mars",
            "type": "Topography & Digital Elevation",
            "resolution": "128 pixels/degree (MEGDR)",
            "status": "Operational / Integrated",
            "coverage": "Global Martian Topography",
            "citation": "Zuber, M. T., et al. (1992), The Mars Observer Laser Altimeter investigation, J. Geophys. Res., 97, 7781-7797."
        },
        {
            "name": "NASA 2001 Mars Odyssey THEMIS Infrared",
            "planet": "Mars",
            "type": "Thermal Inertia & Mineralogy",
            "resolution": "100 m / 1 km global products",
            "status": "Operational / Integrated",
            "coverage": "Global Mars Day/Night IR",
            "citation": "Christensen, P. R., et al. (2004), The Thermal Emission Imaging System (THEMIS) for the Mars 2001 Odyssey Mission, Space Sci. Rev., 110, 85-130."
        },
        {
            "name": "USGS-IAU Gazetteer of Planetary Nomenclature",
            "planet": "Moon / Mars",
            "type": "Official Toponymy & Geological Units",
            "resolution": "Feature-level polygon/point bounds",
            "status": "Operational / Integrated",
            "coverage": "Global Named Features",
            "citation": "IAU Working Group for Planetary System Nomenclature (WGPSN) / USGS Astrogeology Science Center."
        },
        {
            "name": "Copernicus DEM & NASA SRTM / NASADEM",
            "planet": "Earth",
            "type": "Global High-Resolution DEM",
            "resolution": "90m global / 30m regional",
            "status": "Operational / Integrated",
            "coverage": "Global Landmass Coverage",
            "citation": "European Space Agency (ESA) & NASA JPL (2021), Copernicus Digital Elevation Model and NASADEM."
        },
        {
            "name": "Global Lithological Map (GLiM)",
            "planet": "Earth",
            "type": "Crustal Rock Units & Lithology",
            "resolution": "Polygonal global coverage",
            "status": "Operational / Integrated",
            "coverage": "Global Terrestrial Crust",
            "citation": "Hartmann, J., & Moosdorf, N. (2012), The new global lithological map database GLiM: A representation of rock properties at the Earth surface, Geochem. Geophys. Geosyst., 13, Q12004."
        },
        {
            "name": "ESA WorldCover 10m Global Land Cover",
            "planet": "Earth",
            "type": "Land Cover, Bare Ground & Vegetation",
            "resolution": "10 meter global grid",
            "status": "Operational / Integrated",
            "coverage": "Global Landmasses",
            "citation": "Zanaga, D., et al. (2021), ESA WorldCover 10 m 2020 v100."
        },
        {
            "name": "NASA LP DAAC MODIS MOD11A1 Land Surface Temp",
            "planet": "Earth",
            "type": "Land Surface Temperature & Emissivity",
            "resolution": "1 km daily grid",
            "status": "Operational / Integrated",
            "coverage": "Global Terrestrial",
            "citation": "Wan, Z. (2014), New refinements and validation of the collection-6 MODIS land-surface temperature/emissivity product, Remote Sens. Environ., 140, 36-45."
        }
    ]

@router.get("/datasets/status")
def get_datasets_status():
    """System health and ingestion status check."""
    db_stats = SpatialDatabase.get_stats()
    return {
        "status": "operational",
        "cache_directory": os.path.exists(REPORTS_DIR),
        "total_earth_candidates_indexed": db_stats.get("total_candidates", len(EARTH_ANALOG_CATALOG)),
        "total_earth_analogs_indexed": db_stats.get("total_candidates", len(EARTH_ANALOG_CATALOG)),
        "continents_covered": db_stats.get("continents", []) if isinstance(db_stats.get("continents"), list) else list(db_stats.get("continents", {}).keys()),
        "total_moon_regions_indexed": len(LUNAR_REGIONS),
        "total_mars_regions_indexed": len(MARS_REGIONS),
        "active_cached_analyses": len(ANALYSIS_CACHE)
    }

@router.post("/regions/select")
def select_region(payload: Dict[str, Any]):
    """
    Extract scientific feature vector for a selected coordinate and radius on Moon, Mars, or Earth.
    """
    planet = payload.get("planet", "moon").lower()
    lat = float(payload.get("latitude", 0.0))
    lon = float(payload.get("longitude", 0.0))
    radius_km = float(payload.get("radius_km", 50.0))
    name = payload.get("name")

    vector = GeoEngine.extract_features(planet, lat, lon, radius_km, custom_name=name)
    return vector

@router.post("/analysis/start", response_model=AnalysisResult)
def start_analysis(request: AnalysisRequest):
    """
    Run the scientific similarity engine:
    Extracts features for the reference coordinate/region and searches the Global Earth Spatial Database
    (or benchmark catalog), ranking candidates with spatial deduplication and diversity balancing.
    """
    start_time = time.time()
    analysis_id = str(uuid.uuid4())

    ref_vector = GeoEngine.extract_features(
        planet=request.planet,
        lat=request.latitude,
        lon=request.longitude,
        radius_km=request.radius_km
    )

    # Determine lithology filter
    effective_lithology = request.lithology_filter
    if not effective_lithology or effective_lithology == "all":
        effective_lithology = request.filter_environment

    candidates = SimilarityEngine.rank_candidates(
        ref_vector=ref_vector,
        weights=request.weights,
        top_n=request.limit,
        continent_filter=request.continent_filter,
        country_filter=request.country_filter,
        lithology_filter=effective_lithology,
        diversity_balanced=request.diversity_balanced,
        use_benchmark_catalog=request.use_benchmark_catalog
    )

    elapsed_ms = round((time.time() - start_time) * 1000.0, 1)

    top_cand = candidates[0] if candidates else None
    mode_label = "Curated Benchmark Stations" if request.use_benchmark_catalog else "Global Earth Spatial Database"
    total_searched = len(EARTH_ANALOG_CATALOG) if request.use_benchmark_catalog else SpatialDatabase.get_stats().get("total_land_candidates", 500)

    continents_found = sorted(list(set(c.country if request.use_benchmark_catalog else c.features.region_id.split('_')[0] for c in candidates)))

    summary = (
        f"Discovery analysis evaluated {total_searched} terrestrial candidate sectors via {mode_label} "
        f"against {ref_vector.name} on {request.planet.capitalize()}. The top-ranked analog is {top_cand.name} ({top_cand.country}) "
        f"with a {top_cand.overall_similarity}% quantitative match."
        if top_cand else "No candidates matched criteria."
    )

    result = AnalysisResult(
        analysis_id=analysis_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        reference_planet=request.planet,
        reference_name=ref_vector.name,
        reference_coordinates={"latitude": request.latitude, "longitude": request.longitude},
        radius_km=request.radius_km,
        weights_used=request.weights,
        reference_features=ref_vector,
        candidates=candidates,
        total_candidates_searched=total_searched,
        computation_time_ms=elapsed_ms,
        scientific_summary=summary,
        database_mode=mode_label,
        diversity_balanced=request.diversity_balanced,
        continents_represented=continents_found
    )

    ANALYSIS_CACHE[analysis_id] = result
    return result

@router.get("/analysis/{analysis_id}", response_model=AnalysisResult)
def get_analysis(analysis_id: str):
    """Retrieve existing analysis by ID."""
    if analysis_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")
    return ANALYSIS_CACHE[analysis_id]

@router.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    """Retrieve detailed candidate profile from the database or catalog."""
    for cand in EARTH_ANALOG_CATALOG:
        if cand["id"] == candidate_id:
            return cand

    # Query from spatial database
    conn = SpatialDatabase.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM earth_candidates WHERE id = ?", (candidate_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)

    raise HTTPException(status_code=404, detail="Candidate not found.")

@router.get("/compare/{analysis_id}/{candidate_id}")
def compare_candidate(analysis_id: str, candidate_id: str):
    """Generate side-by-side comparison payload between the reference and the candidate."""
    if analysis_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")

    analysis = ANALYSIS_CACHE[analysis_id]
    target_cand = next((c for c in analysis.candidates if c.candidate_id == candidate_id), None)
    if not target_cand:
        raise HTTPException(status_code=404, detail="Candidate not found in this analysis.")

    explanation = AIAssistant.generate_explanation(analysis.reference_features, target_cand)

    return {
        "analysis_id": analysis_id,
        "reference_planet": analysis.reference_planet,
        "reference_name": analysis.reference_name,
        "reference_features": analysis.reference_features,
        "candidate": target_cand,
        "explanation": explanation
    }

@router.post("/insights/generate")
def generate_insights(payload: Dict[str, Any]):
    """
    Generate targeted scientific exploration insights or answer specific research questions.
    """
    analysis_id = payload.get("analysis_id")
    candidate_id = payload.get("candidate_id")
    question = payload.get("question")

    if not analysis_id or analysis_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")

    analysis = ANALYSIS_CACHE[analysis_id]
    target_cand = next((c for c in analysis.candidates if c.candidate_id == candidate_id), analysis.candidates[0])

    if question:
        response_text = AIAssistant.answer_query(analysis.reference_features, target_cand, question)
        return {"question": question, "response": response_text}
    else:
        full_insights = AIAssistant.generate_explanation(analysis.reference_features, target_cand)
        return full_insights

@router.post("/reports/generate")
def generate_report(payload: Dict[str, Any]):
    """
    Generate downloadable PDF scientific research report.
    """
    analysis_id = payload.get("analysis_id")
    candidate_id = payload.get("candidate_id")

    if not analysis_id or analysis_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")

    analysis = ANALYSIS_CACHE[analysis_id]
    target_cand = next((c for c in analysis.candidates if c.candidate_id == candidate_id), analysis.candidates[0])

    report_id = f"report_{analysis_id[:8]}_{target_cand.candidate_id}"
    pdf_filename = f"{report_id}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)

    ReportGenerator.generate_pdf_report(analysis.reference_features, target_cand, pdf_path)

    return {
        "report_id": report_id,
        "filename": pdf_filename,
        "download_url": f"/api/reports/{report_id}/download",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file_size_bytes": os.path.getsize(pdf_path)
    }

@router.get("/reports/{report_id}/download")
def download_report(report_id: str):
    """Download generated PDF report."""
    pdf_filename = f"{report_id}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report file not found.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )
