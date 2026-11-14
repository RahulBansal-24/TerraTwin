"""
USGS-IAU Planetary Nomenclature Gazetteer Database.
Provides searchable, categorized named features for the Moon and Mars
(Craters, Montes, Valles, Maria, Planitiae, Chasmata, Rimae, Fossae).
"""

from typing import List, Dict, Any, Optional

LUNAR_GAZETTEER = [
    # Craters & Basins
    {"id": "moon_feat_001", "name": "Shackleton", "type": "Crater", "lat": -89.9, "lon": 0.0, "diameter_km": 21.0, "geological_unit": "Polar Highland Ice Trap", "description": "Permanently shadowed crater at the lunar South Pole with ice volatiles."},
    {"id": "moon_feat_002", "name": "Malapert", "type": "Crater", "lat": -85.0, "lon": 11.4, "diameter_km": 69.0, "geological_unit": "South Polar Highland", "description": "Near-polar crater near Malapert Massif Artemis exploration zone."},
    {"id": "moon_feat_003", "name": "Copernicus", "type": "Crater", "lat": 9.6, "lon": -20.1, "diameter_km": 93.0, "geological_unit": "Copernican Impact Breccia", "description": "Prominent complex impact crater with massive terraced rim and central peaks."},
    {"id": "moon_feat_004", "name": "Tycho", "type": "Crater", "lat": -43.3, "lon": -11.2, "diameter_km": 86.0, "geological_unit": "Copernican Impact Melt", "description": "Fresh impact crater with spectacular bright radial rays extending thousands of km."},
    {"id": "moon_feat_005", "name": "Aristarchus", "type": "Crater", "lat": 23.7, "lon": -47.4, "diameter_km": 40.0, "geological_unit": "Pyroclastic Plateau", "description": "Bright crater on an elevated volcanic plateau with intense radon degassing anomalies."},
    {"id": "moon_feat_006", "name": "Schrödinger", "type": "Basin", "lat": -75.0, "lon": 132.4, "diameter_km": 312.0, "geological_unit": "Impact Basin & Pyroclastics", "description": "Second youngest lunar impact basin with deep crustal uplift and dark volcanic vents."},
    {"id": "moon_feat_007", "name": "Plato", "type": "Crater", "lat": 51.6, "lon": -9.3, "diameter_km": 101.0, "geological_unit": "Flooded Basalt Crater", "description": "Dark basalt-flooded circular crater on the northern border of Mare Imbrium."},
    {"id": "moon_feat_008", "name": "Archimedes", "type": "Crater", "lat": 29.7, "lon": -4.0, "diameter_km": 83.0, "geological_unit": "Imbrium Basin Floor", "description": "Large flooded crater within eastern Mare Imbrium with smooth interior floor."},
    {"id": "moon_feat_009", "name": "Clavius", "type": "Crater", "lat": -58.4, "lon": -14.4, "diameter_km": 225.0, "geological_unit": "Highland Southern Terrain", "description": "One of the largest craters on the Moon; SOFIA detected molecular water in its illuminated regolith."},
    {"id": "moon_feat_010", "name": "Kepler", "type": "Crater", "lat": 8.1, "lon": -38.0, "diameter_km": 31.0, "geological_unit": "Oceanus Procellarum Floor", "description": "Bright rayed impact crater between Oceanus Procellarum and Mare Insularum."},
    {"id": "moon_feat_011", "name": "Gassendi", "type": "Crater", "lat": -17.5, "lon": -39.9, "diameter_km": 110.0, "geological_unit": "Fractured Floor Crater", "description": "Floor-fractured crater with central mountain cluster and network of rilles."},
    {"id": "moon_feat_012", "name": "Theophilus", "type": "Crater", "lat": -11.4, "lon": 26.4, "diameter_km": 100.0, "geological_unit": "Eratosthenian Impact", "description": "Deep crater with complex triple central peak overlooking Sinus Asperitatis."},

    # Maria & Planitiae (Lava Plains)
    {"id": "moon_feat_013", "name": "Mare Tranquillitatis", "type": "Mare", "lat": 8.5, "lon": 31.4, "diameter_km": 873.0, "geological_unit": "High-Titanium Flood Basalt", "description": "Historic Apollo 11 landing site; rich in ilmenite and effusive lava flows."},
    {"id": "moon_feat_014", "name": "Mare Imbrium", "type": "Mare", "lat": 32.8, "lon": -15.6, "diameter_km": 1145.0, "geological_unit": "Multiring Impact Basin Basalt", "description": "Colossal impact basin filled by successive episodes of dark flood basalts."},
    {"id": "moon_feat_015", "name": "Oceanus Procellarum", "type": "Oceanus", "lat": 18.4, "lon": -57.4, "diameter_km": 2568.0, "geological_unit": "KREEP Basalt Ocean", "description": "The largest lunar mare expanse, covering the western nearside with volcanic deposits."},
    {"id": "moon_feat_016", "name": "Mare Serenitatis", "type": "Mare", "lat": 28.0, "lon": 17.5, "diameter_km": 707.0, "geological_unit": "Circular Mare Basin", "description": "Circular mare with prominent mass concentration (mascon) and Apollo 17 valley rim."},
    {"id": "moon_feat_017", "name": "Mare Crisium", "type": "Mare", "lat": 17.0, "lon": 59.1, "diameter_km": 555.0, "geological_unit": "Isolated Circular Basin", "description": "Prominent isolated circular basalt plain on the eastern lunar limb."},
    {"id": "moon_feat_018", "name": "Mare Orientale", "type": "Mare", "lat": -19.4, "lon": -92.8, "diameter_km": 930.0, "geological_unit": "Concentric Multiring Basin", "description": "The best preserved multiring impact basin on the Moon with Cordillera mountain rings."},

    # Montes & Rilles
    {"id": "moon_feat_019", "name": "Malapert Massif", "type": "Mons", "lat": -86.0, "lon": 2.7, "diameter_km": 60.0, "geological_unit": "Highland Crustal Massif", "description": "Elevated 5 km peak near the South Pole with near-permanent solar illumination and direct Earth line-of-sight."},
    {"id": "moon_feat_020", "name": "Mons Hadley & Hadley Rille", "type": "Rima", "lat": 26.1, "lon": 3.6, "diameter_km": 80.0, "geological_unit": "Sinuous Collapse Lava Channel", "description": "Apollo 15 site featuring a 1.5 km wide volcanic collapse rille at the base of the Apennines."},
    {"id": "moon_feat_021", "name": "Montes Apenninus", "type": "Montes", "lat": 18.9, "lon": -3.7, "diameter_km": 600.0, "geological_unit": "Basin Rim Mountain Chain", "description": "Spectacular 5 km high mountain range forming the southeastern rim of the Imbrium basin."},
    {"id": "moon_feat_022", "name": "Mons Rümker", "type": "Mons", "lat": 40.8, "lon": -58.1, "diameter_km": 70.0, "geological_unit": "Lunar Volcanic Dome Complex", "description": "Chang'e 5 landing site; large volcanic mound studded with dozens of effusive domes."}
]

MARS_GAZETTEER = [
    # Craters
    {"id": "mars_feat_001", "name": "Jezero", "type": "Crater", "lat": 18.38, "lon": 77.58, "diameter_km": 49.0, "geological_unit": "Deltaic Clay & Olivine Floor", "description": "Perseverance rover exploration site; ancient river delta preserving clay and carbonate minerals."},
    {"id": "mars_feat_002", "name": "Gale", "type": "Crater", "lat": -5.4, "lon": 137.8, "diameter_km": 154.0, "geological_unit": "Sedimentary Mount Sharp Mound", "description": "Curiosity rover site holding a 5.5 km layered sedimentary mountain with sulfate/clay strata."},
    {"id": "mars_feat_003", "name": "Gusev", "type": "Crater", "lat": -14.6, "lon": 175.5, "diameter_km": 166.0, "geological_unit": "Basaltic Plains & Columbia Hills", "description": "Spirit rover site; ancient crater filled with basaltic lavas and hydrothermal silica deposits."},
    {"id": "mars_feat_004", "name": "Holden", "type": "Crater", "lat": -26.4, "lon": -34.0, "diameter_km": 154.0, "geological_unit": "Megabreccia & Lake Beds", "description": "Spectacular impact crater in Uzboi-Ladon outflow system with well-exposed lake strata."},
    {"id": "mars_feat_005", "name": "Eberswalde", "type": "Crater", "lat": -24.0, "lon": -33.3, "diameter_km": 65.0, "geological_unit": "Distributary River Delta", "description": "Pristine preserved fossil river delta with meandering channels and inverted topography."},
    {"id": "mars_feat_006", "name": "Victoria", "type": "Crater", "lat": -2.05, "lon": -5.5, "diameter_km": 0.8, "geological_unit": "Meridiani Sulfate Sandstones", "description": "Explored by Opportunity rover; reveals layered sulfate rocks and hematite concretions."},
    {"id": "mars_feat_007", "name": "Hellas", "type": "Basin", "lat": -42.4, "lon": 70.5, "diameter_km": 2300.0, "geological_unit": "Giant Impact Basin", "description": "Deepest impact basin on Mars (-7 km elevation); high atmospheric pressure supporting frost dynamics."},

    # Volcanoes (Montes & Tholi)
    {"id": "mars_feat_008", "name": "Olympus Mons", "type": "Mons", "lat": 18.65, "lon": -133.8, "diameter_km": 624.0, "geological_unit": "Super-Shield Volcano", "description": "The largest volcano in the Solar System, rising nearly 22 km with a nested summit caldera."},
    {"id": "mars_feat_009", "name": "Ascraeus Mons", "type": "Mons", "lat": 11.9, "lon": -104.5, "diameter_km": 480.0, "geological_unit": "Tharsis Shield Volcano", "description": "Northernmost of the three Tharsis Montes shield volcanoes, towering 18 km above datum."},
    {"id": "mars_feat_010", "name": "Pavonis Mons", "type": "Mons", "lat": 0.8, "lon": -113.0, "diameter_km": 375.0, "geological_unit": "Equatorial Shield Volcano", "description": "Equatorial Tharsis shield volcano with extensive lava tube collapse pits and glacial moraines."},
    {"id": "mars_feat_011", "name": "Arsia Mons", "type": "Mons", "lat": -9.0, "lon": -120.5, "diameter_km": 435.0, "geological_unit": "Southern Tharsis Volcano", "description": "Southern Tharsis shield with colossal 110 km caldera and deep pit crater skylights."},
    {"id": "mars_feat_012", "name": "Elysium Mons", "type": "Mons", "lat": 25.0, "lon": 147.2, "diameter_km": 240.0, "geological_unit": "Elysium Volcanic Province", "description": "Isolated volcanic construct standing 14 km above the surrounding northern volcanic plains."},

    # Canyons & Valleys (Chasmata & Valles)
    {"id": "mars_feat_013", "name": "Valles Marineris (Coprates)", "type": "Chasma", "lat": -14.0, "lon": -59.2, "diameter_km": 4000.0, "geological_unit": "Tectonic Rift Canyon", "description": "Grand canyon system of Mars up to 10 km deep, revealing colossal crustal cross-sections."},
    {"id": "mars_feat_014", "name": "Mawrth Vallis", "type": "Vallis", "lat": 24.0, "lon": -19.0, "diameter_km": 636.0, "geological_unit": "Stratified Phyllosilicate Sequence", "description": "Ancient outflow channel exposing hundreds of meters of diverse Noachian clay strata."},
    {"id": "mars_feat_015", "name": "Kasei Valles", "type": "Vallis", "lat": 24.6, "lon": -65.0, "diameter_km": 1780.0, "geological_unit": "Catastrophic Mega-Flood Channel", "description": "Immense outflow system carved by catastrophic sub-ice floods and volcanic lava flows."},
    {"id": "mars_feat_016", "name": "Nili Fossae", "type": "Fossae", "lat": 22.0, "lon": 75.0, "diameter_km": 667.0, "geological_unit": "Carbonate & Serpentine Troughs", "description": "Tectonic graben exposing smectite clays, magnesite carbonates, and olivine bedrock."},
    {"id": "mars_feat_017", "name": "Candor Chasma", "type": "Chasma", "lat": -6.5, "lon": -75.7, "diameter_km": 810.0, "geological_unit": "Interior Layered Deposits", "description": "Central canyon within Valles Marineris with multi-kilometer hills of layered sulfate salts."},
    {"id": "mars_feat_018", "name": "Athabasca Valles", "type": "Vallis", "lat": 9.8, "lon": 156.0, "diameter_km": 285.0, "geological_unit": "Young Flood Basalt & Ice Plates", "description": "One of the youngest volcanic-aqueous flood channels on Mars with rafted plate morphologies."},
    {"id": "mars_feat_019", "name": "Chryse Planitia", "type": "Planitia", "lat": 28.4, "lon": -40.0, "diameter_km": 1540.0, "geological_unit": "Outflow Basin Plain", "description": "Viking 1 landing site; vast circular plain receiving major ancient catastrophic flood channels."},
    {"id": "mars_feat_020", "name": "Utopia Planitia", "type": "Planitia", "lat": 46.7, "lon": 117.5, "diameter_km": 3300.0, "geological_unit": "Subsurface Excess Ice Plain", "description": "Zhurong rover exploration region with massive ground ice reserves and scalloped permafrost depressions."},
    {"id": "mars_feat_021", "name": "Argyre", "type": "Basin", "lat": -49.7, "lon": -44.0, "diameter_km": 1800.0, "geological_unit": "Impact Basin & Glacier Moraines", "description": "Southern hemisphere impact basin exhibiting extensive glacial and periglacial landforms."},
    {"id": "mars_feat_022", "name": "Noctis Labyrinthus", "type": "Labyrinthus", "lat": -7.0, "lon": -101.0, "diameter_km": 1200.0, "geological_unit": "Complex Graben Network", "description": "Tectonic maze of intersecting valleys and collapse pits at the western edge of Valles Marineris."},
    {"id": "mars_feat_023", "name": "Korolev", "type": "Crater", "lat": 73.0, "lon": 165.0, "diameter_km": 81.4, "geological_unit": "Glacial Ice Trap", "description": "Deep high-latitude crater filled year-round by a dome of pure water ice 1.8 km thick."},
    {"id": "mars_feat_024", "name": "Elysium Planitia", "type": "Planitia", "lat": 3.0, "lon": 154.7, "diameter_km": 1700.0, "geological_unit": "Cerberus Fossae Flood Basalts", "description": "InSight lander site; smooth volcanic plain cut by recent tectonic fissures and marsquake sources."}
]

class PlanetaryGazetteer:
    """Provides lookup and spatial filtering for official named planetary features."""

    @classmethod
    def _format_feature(cls, feat: Dict[str, Any], planet: str) -> Dict[str, Any]:
        d = dict(feat)
        d["planet"] = planet.lower()
        d["feature_type"] = feat.get("type", "Feature")
        d["type"] = feat.get("type", "Feature")
        d["latitude"] = feat.get("lat", 0.0)
        d["lat"] = feat.get("lat", 0.0)
        d["longitude"] = feat.get("lon", 0.0)
        d["lon"] = feat.get("lon", 0.0)
        d["geological_context"] = feat.get("geological_unit", "")
        return d

    @classmethod
    def get_features(cls, planet: str, feature_type: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        planet = planet.lower()
        if planet == "moon":
            catalog = LUNAR_GAZETTEER
        elif planet == "mars":
            catalog = MARS_GAZETTEER
        else:
            return []

        results = []
        for feat in catalog:
            if feature_type and feature_type.lower() != "all":
                if feat["type"].lower() != feature_type.lower():
                    continue

            if search:
                s = search.lower()
                if s not in feat["name"].lower() and s not in feat["description"].lower():
                    continue

            results.append(cls._format_feature(feat, planet))

        return results

    @classmethod
    def get_feature_by_name(cls, planet: str, name: str) -> Optional[Dict[str, Any]]:
        planet = planet.lower()
        catalog = LUNAR_GAZETTEER if planet == "moon" else (MARS_GAZETTEER if planet == "mars" else [])
        for feat in catalog:
            if feat["name"].lower() == name.lower():
                return cls._format_feature(feat, planet)
        return None
