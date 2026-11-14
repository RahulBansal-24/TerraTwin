"""
Automated unit tests for TerraTwin Global Spatial Database, Multi-Scale Grid,
Spatial Deduplication, and IAU Planetary Gazetteer.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.services.spatial_db import SpatialDatabase
from backend.app.services.planetary_gazetteer import PlanetaryGazetteer
from backend.app.services.similarity_engine import SimilarityEngine
from backend.app.services.geo_engine import GeoEngine
from backend.app.models.similarity import SimilarityWeights

class TestSpatialDatabaseAndGazetteer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = SpatialDatabase()

    def test_database_initialization_and_counts(self):
        stats = self.db.get_stats()
        self.assertEqual(stats["status"], "ready")
        self.assertGreater(stats["total_candidates"], 100)
        self.assertGreaterEqual(stats["continents_count"], 6)
        self.assertIn("Antarctica", stats["continents"])
        self.assertIn("Africa", stats["continents"])
        self.assertIn("North America", stats["continents"])
        self.assertIn("South America", stats["continents"])
        self.assertIn("Asia", stats["continents"])
        self.assertEqual(stats["spatial_index"], "SQLite R*Tree Virtual Table")

    def test_spatial_bbox_query(self):
        # Query bounding box for South America (Atacama region approx -30 to -15 lat, -75 to -65 lon)
        results = self.db.query_candidates(
            min_lat=-30.0,
            max_lat=-15.0,
            min_lon=-75.0,
            max_lon=-65.0,
            limit=20
        )
        self.assertGreater(len(results), 0)
        for cand in results:
            self.assertTrue(-30.0 <= cand["latitude"] <= -15.0)
            self.assertTrue(-75.0 <= cand["longitude"] <= -65.0)

    def test_attribute_filtering_continent_and_lithology(self):
        # Filter specifically by Antarctica
        antarctica_cands = self.db.query_candidates(continent="Antarctica", limit=50)
        self.assertGreater(len(antarctica_cands), 0)
        for cand in antarctica_cands:
            self.assertEqual(cand["continent"], "Antarctica")

        # Filter by lithology
        volcanic_cands = self.db.query_candidates(lithology="basalt", limit=50)
        self.assertGreater(len(volcanic_cands), 0)
        for cand in volcanic_cands:
            self.assertIn("basalt", cand["lithology_category"].lower())

    def test_spatial_deduplication(self):
        # Vector on Mars
        vector = GeoEngine.extract_features(planet="mars", lat=18.38, lon=77.58)

        # Global search with 80 km deduplication
        candidates = SimilarityEngine.rank_candidates(
            vector,
            use_benchmark_catalog=False,
            min_distance_km=80.0,
            top_n=10
        )
        self.assertGreater(len(candidates), 0)

        # Verify no two candidates are closer than 79 km
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                dist = GeoEngine.haversine_distance_km(
                    candidates[i].latitude, candidates[i].longitude,
                    candidates[j].latitude, candidates[j].longitude,
                    radius_km=6371.0
                )
                self.assertGreaterEqual(dist, 79.0, f"Candidates {candidates[i].name} and {candidates[j].name} are too close: {dist} km")

    def test_diversity_balanced_ranking(self):
        vector = GeoEngine.extract_features(planet="moon", lat=-89.9, lon=0.0)

        # Run with diversity_balanced=True
        candidates_div = SimilarityEngine.rank_candidates(
            vector,
            use_benchmark_catalog=False,
            diversity_balanced=True,
            top_n=8
        )
        self.assertGreater(len(candidates_div), 1)

        # Check represented continents
        continents = set()
        for cand in candidates_div:
            parts = cand.country.split(", ")
            continent = parts[-1] if len(parts) > 1 else cand.country
            continents.add(continent)

        self.assertGreaterEqual(len(continents), 2, "Diversity balancing should return multiple continents")

    def test_benchmark_catalog_fallback_mode(self):
        vector = GeoEngine.extract_features(planet="mars", lat=-14.57, lon=175.47)
        candidates_bm = SimilarityEngine.rank_candidates(
            vector,
            use_benchmark_catalog=True,
            top_n=5
        )
        self.assertEqual(len(candidates_bm), 5)
        # All benchmark candidates should be known curated stations
        names = [c.name for c in candidates_bm]
        self.assertTrue(any("Atacama" in n or "Dry Valleys" in n or "Haughton" in n or "Surtsey" in n or "Death Valley" in n for n in names))

    def test_planetary_gazetteer_moon(self):
        gaz = PlanetaryGazetteer()
        moon_features = gaz.get_features(planet="moon")
        self.assertGreater(len(moon_features), 15)

        # Check Shackleton
        shackleton = gaz.get_feature_by_name("moon", "Shackleton")
        self.assertIsNotNone(shackleton)
        self.assertEqual(shackleton["feature_type"], "Crater")
        self.assertAlmostEqual(shackleton["latitude"], -89.9, delta=0.5)

    def test_planetary_gazetteer_mars(self):
        gaz = PlanetaryGazetteer()
        mars_features = gaz.get_features(planet="mars")
        self.assertGreater(len(mars_features), 20)

        # Check Olympus Mons
        olympus = gaz.get_feature_by_name("mars", "Olympus Mons")
        self.assertIsNotNone(olympus)
        self.assertEqual(olympus["feature_type"], "Mons")
        self.assertGreater(olympus["diameter_km"], 500)

        # Check search query
        craters = gaz.get_features(planet="mars", feature_type="Crater")
        self.assertGreater(len(craters), 5)
        for c in craters:
            self.assertEqual(c["feature_type"], "Crater")

    def test_no_sector_labels_in_database(self):
        """Verify that the misleading 'Sector X' label is completely eliminated."""
        all_cands = self.db.query_candidates(limit=1000)
        for cand in all_cands:
            self.assertNotIn("Sector", cand["name"], f"Candidate {cand['name']} still contains 'Sector'")

    def test_strict_province_deduplication(self):
        """Verify that no two candidates in the top results share the same macro-province."""
        vector = GeoEngine.extract_features(planet="mars", lat=-21.2, lon=119.4) # Pilbara-like coordinates
        candidates = SimilarityEngine.rank_candidates(vector, top_n=10)
        
        provinces = []
        for cand in candidates:
            base_prov = cand.name.split(" (")[0].strip() if " (" in cand.name else cand.name.strip()
            provinces.append(base_prov)

        self.assertEqual(len(provinces), len(set(provinces)), f"Duplicate province found in top results: {provinces}")

    def test_ludhiana_on_demand_extraction(self):
        """Verify on-demand extraction for Ludhiana (Punjab, India) returns authentic alluvial plain metrics."""
        vector = GeoEngine.extract_features(planet="earth", lat=30.9, lon=75.8, radius_km=30.0)
        self.assertEqual(vector.geology.lithology_category, "sedimentary_alluvial")
        self.assertLess(vector.topography.slope_mean.value, 3.0)
        self.assertAlmostEqual(vector.topography.elevation_mean.value, 230.0, delta=50.0)
        self.assertGreater(vector.surface.vegetation_ndvi.value, 0.4)

    def test_continent_specific_query(self):
        """Verify that filtering by continent returns candidates strictly belonging to that continent."""
        vector = GeoEngine.extract_features(planet="moon", lat=-89.9, lon=0.0)
        asia_cands = SimilarityEngine.rank_candidates(vector, continent_filter="Asia", top_n=6)
        self.assertGreater(len(asia_cands), 0)
        for cand in asia_cands:
            self.assertEqual(cand.continent, "Asia")

if __name__ == "__main__":
    unittest.main()
