"""
Automated unit tests for TerraTwin Scientific Engines and Calculations using unittest.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.services.geo_engine import GeoEngine
from backend.app.services.similarity_engine import SimilarityEngine
from backend.app.services.ai_assistant import AIAssistant
from backend.app.services.report_generator import ReportGenerator
from backend.app.models.similarity import SimilarityWeights

class TestTerraTwinEngines(unittest.TestCase):

    def test_moon_feature_extraction(self):
        vector = GeoEngine.extract_features(planet="moon", lat=-89.9, lon=0.0, radius_km=30.0)
        self.assertEqual(vector.planet, "moon")
        self.assertEqual(vector.name, "Shackleton Crater")
        self.assertGreater(vector.topography.slope_mean.value, 15.0)
        self.assertGreater(vector.topography.relief_m.value, 3000.0)
        self.assertEqual(vector.geology.lithology_category, "polar_permafrost_ice")
        self.assertGreater(len(vector.elevation_profile), 0)
        total_p = sum(vector.slope_histogram.values())
        self.assertAlmostEqual(total_p, 100.0, delta=1.5)

    def test_mars_feature_extraction(self):
        vector = GeoEngine.extract_features(planet="mars", lat=18.38, lon=77.58, radius_km=50.0)
        self.assertEqual(vector.planet, "mars")
        self.assertEqual(vector.name, "Jezero Crater")
        self.assertEqual(vector.geology.lithology_category, "hyperarid_playa_evaporite")
        self.assertGreater(vector.thermal.diurnal_range_k.value, 50.0)
        self.assertEqual(vector.surface.bare_ground_ratio.value, 1.0)

    def test_similarity_ranking_moon(self):
        vector = GeoEngine.extract_features(planet="moon", lat=-89.9, lon=0.0)
        weights = SimilarityWeights(topography_weight=0.35, geology_weight=0.30, thermal_weight=0.20, surface_weight=0.15)
        candidates = SimilarityEngine.rank_candidates(vector, weights=weights, top_n=5)

        self.assertEqual(len(candidates), 5)
        scores = [c.overall_similarity for c in candidates]
        self.assertEqual(scores, sorted(scores, reverse=True))

        for c in candidates:
            self.assertTrue(0.0 <= c.overall_similarity <= 100.0)
            self.assertTrue(0.0 <= c.components.topography_similarity <= 100.0)
            self.assertTrue(0.0 <= c.components.geological_similarity <= 100.0)
            self.assertGreater(len(c.strongest_matches), 0)

    def test_similarity_ranking_mars(self):
        vector = GeoEngine.extract_features(planet="mars", lat=18.38, lon=77.58)
        candidates = SimilarityEngine.rank_candidates(vector, top_n=5)
        self.assertEqual(len(candidates), 5)
        top_cand = candidates[0]
        self.assertGreater(top_cand.overall_similarity, 60.0)

    def test_ai_assistant_explanation(self):
        vector = GeoEngine.extract_features(planet="mars", lat=18.38, lon=77.58)
        candidates = SimilarityEngine.rank_candidates(vector, top_n=1)
        cand = candidates[0]
        explanation = AIAssistant.generate_explanation(vector, cand)
        self.assertIn("why_selected", explanation)
        self.assertIn("rover_mobility", explanation)
        self.assertGreaterEqual(len(explanation["environmental_differences"]), 3)

    def test_pdf_report_generation(self):
        vector = GeoEngine.extract_features(planet="moon", lat=-89.9, lon=0.0)
        candidates = SimilarityEngine.rank_candidates(vector, top_n=1)
        cand = candidates[0]
        out_pdf = os.path.join(os.path.dirname(__file__), "test_sample_report.pdf")
        try:
            generated_path = ReportGenerator.generate_pdf_report(vector, cand, out_pdf)
            self.assertTrue(os.path.exists(generated_path))
            self.assertGreater(os.path.getsize(generated_path), 10000)
        finally:
            if os.path.exists(out_pdf):
                os.remove(out_pdf)

if __name__ == "__main__":
    unittest.main()
