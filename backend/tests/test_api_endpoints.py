"""
Automated API Functional Tests for TerraTwin REST Endpoints.
Direct functional verification of all API handlers, request validation,
similarity pipeline, and PDF report compilation.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.routes.api import (
    get_planets, get_planet_details, get_datasets, get_datasets_status,
    select_region, start_analysis, get_analysis, compare_candidate,
    generate_insights, generate_report
)
from backend.app.models.similarity import AnalysisRequest, SimilarityWeights

class TestAPIEndpoints(unittest.TestCase):

    def test_get_planets(self):
        planets = get_planets()
        self.assertEqual(len(planets), 3)
        names = [p["name"] for p in planets]
        self.assertIn("The Moon", names)
        self.assertIn("Mars", names)
        self.assertIn("Earth", names)

    def test_get_planet_details(self):
        moon = get_planet_details("moon")
        self.assertEqual(moon["id"], "moon")
        self.assertGreater(len(moon["featured_regions"]), 0)

        mars = get_planet_details("mars")
        self.assertEqual(mars["id"], "mars")
        self.assertGreater(len(mars["featured_regions"]), 0)

    def test_get_datasets(self):
        datasets = get_datasets()
        self.assertGreaterEqual(len(datasets), 5)
        names = [d["name"] for d in datasets]
        self.assertTrue(any("LOLA" in n for n in names))
        self.assertTrue(any("MOLA" in n for n in names))
        self.assertTrue(any("SRTM" in n for n in names))

    def test_datasets_status(self):
        status = get_datasets_status()
        self.assertEqual(status["status"], "operational")
        self.assertGreater(status["total_earth_analogs_indexed"], 10)

    def test_select_region(self):
        payload = {
            "planet": "moon",
            "latitude": -89.9,
            "longitude": 0.0,
            "radius_km": 50.0
        }
        data = select_region(payload)
        self.assertEqual(data.planet, "moon")
        self.assertEqual(data.name, "Shackleton Crater")
        self.assertGreater(data.topography.slope_mean.value, 15.0)

    def test_full_analysis_workflow_and_pdf(self):
        # 1. Start Analysis for Mars Jezero Crater
        req = AnalysisRequest(
            planet="mars",
            latitude=18.38,
            longitude=77.58,
            radius_km=50.0,
            weights=SimilarityWeights(
                topography_weight=0.35,
                geology_weight=0.30,
                thermal_weight=0.20,
                surface_weight=0.15
            )
        )
        analysis_data = start_analysis(req)
        analysis_id = analysis_data.analysis_id
        self.assertTrue(bool(analysis_id))
        self.assertGreater(len(analysis_data.candidates), 0)

        top_cand = analysis_data.candidates[0]
        cand_id = top_cand.candidate_id

        # 2. Retrieve Analysis by ID
        get_res = get_analysis(analysis_id)
        self.assertEqual(get_res.analysis_id, analysis_id)

        # 3. Compare with Top Candidate
        comp_data = compare_candidate(analysis_id, cand_id)
        self.assertIn("explanation", comp_data)
        self.assertIn("why_selected", comp_data["explanation"])

        # 4. Generate AI Insights Query
        query_payload = {
            "analysis_id": analysis_id,
            "candidate_id": cand_id,
            "question": "Is this site suitable for rover mobility testing?"
        }
        insight_res = generate_insights(query_payload)
        self.assertIn("response", insight_res)

        # 5. Generate PDF Report
        report_payload = {
            "analysis_id": analysis_id,
            "candidate_id": cand_id
        }
        rep_res = generate_report(report_payload)
        self.assertTrue(rep_res["filename"].endswith(".pdf"))
        self.assertGreater(rep_res["file_size_bytes"], 10000)

if __name__ == "__main__":
    unittest.main()
