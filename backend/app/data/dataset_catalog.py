"""
TerraTwin Planetary and Geospatial Dataset Catalog.
Ground truth scientific coordinates, physical constants, mission significance,
and planetary parameters derived from NASA PDS (LOLA, Diviner, MOLA, THEMIS)
and Earth Observation datasets (SRTM, MODIS, GLiM).
"""

PLANETARY_SYSTEM = {
    "earth": {
        "id": "earth",
        "name": "Earth",
        "tagline": "Dynamic Terrestrial Benchmark",
        "description": "Our home planet serves as the comparative baseline. Earth exhibits active plate tectonics, hydrological erosion, and atmospheric pressure of ~1013 hPa.",
        "color_theme": "#38bdf8",
        "physical": {
            "radius_km": 6371.0,
            "surface_gravity_ms2": 9.807,
            "atmospheric_pressure_hpa": 1013.25,
            "mean_surface_temp_k": 288.0,
            "temp_range_k": [184.0, 330.0],
            "solar_flux_wm2": 1361.0,
            "atmosphere_summary": "78% N2, 21% O2, 0.9% Ar, 0.04% CO2. Dense atmosphere with active hydrological cycle.",
            "magnetic_field": "Strong dipole (~30-60 µT), shields surface from galactic cosmic rays.",
            "vacuum_environment": False
        },
        "data_sources": [
            "USGS Shuttle Radar Topography Mission (SRTM) 30m Global DEM",
            "NASA LP DAAC MODIS MOD11A1 Land Surface Temperature (1km)",
            "Global Lithological Map (GLiM) - University of Hamburg",
            "ESA WorldCover 10m Global Land Cover",
            "WorldClim v2.1 High Resolution Bioclimatic Data"
        ]
    },
    "moon": {
        "id": "moon",
        "name": "The Moon",
        "tagline": "Airless, Impact-Battered Regolith World",
        "description": "Earth's natural satellite. A pristine geological record shaped by impact cratering, ancient volcanic mare basalt outflows, and extreme vacuum thermal swings.",
        "color_theme": "#94a3b8",
        "physical": {
            "radius_km": 1737.4,
            "surface_gravity_ms2": 1.622,
            "atmospheric_pressure_hpa": 1e-10,
            "mean_surface_temp_k": 220.0,
            "temp_range_k": [40.0, 395.0],
            "solar_flux_wm2": 1361.0,
            "atmosphere_summary": "Hard vacuum (<10^-12 bar). Negligible collisionless exosphere (He, Ne, Ar, H).",
            "magnetic_field": "Negligible global dipole (<1 nT). Weak localized crustal remanent magnetic anomalies.",
            "vacuum_environment": True
        },
        "data_sources": [
            "NASA LRO Lunar Orbiter Laser Altimeter (LOLA) GDR Topography",
            "NASA LRO Diviner Lunar Radiometer Experiment (DLRE) Thermal & Rock Abundance",
            "NASA LROC Wide Angle Camera (WAC) Global Basemap",
            "MIT Imbrium Lunar Polar Illumination & Permanently Shadowed Regions (PSR)"
        ]
    },
    "mars": {
        "id": "mars",
        "name": "Mars",
        "tagline": "Cold, Hyper-Arid Desert World",
        "description": "The Red Planet preserves a record of ancient water activity, massive shield volcanoes, immense canyon systems, and global dust storm dynamics under a thin CO2 atmosphere.",
        "color_theme": "#fb923c",
        "physical": {
            "radius_km": 3389.5,
            "surface_gravity_ms2": 3.721,
            "atmospheric_pressure_hpa": 6.36,
            "mean_surface_temp_k": 210.0,
            "temp_range_k": [140.0, 305.0],
            "solar_flux_wm2": 589.0,
            "atmosphere_summary": "95.3% CO2, 2.6% N2, 1.9% Ar. Mean surface pressure 6.1 hPa (~0.6% of Earth).",
            "magnetic_field": "No active core dynamo; strong localized crustal remanent fields in southern highlands.",
            "vacuum_environment": False
        },
        "data_sources": [
            "NASA MGS Mars Orbiter Laser Altimeter (MOLA) MEGDR 128 ppd Topography",
            "NASA 2001 Mars Odyssey THEMIS Day/Night Infrared & Thermal Inertia",
            "NASA MRO HiRISE & Context Camera (CTX) Geomorphology",
            "USGS Astrogeology Mars Global Geologic Map (SIM 3292)"
        ]
    }
}

LUNAR_REGIONS = [
    {
        "id": "moon_shackleton",
        "planet": "moon",
        "name": "Shackleton Crater",
        "latitude": -89.9,
        "longitude": 0.0,
        "elevation_m": -4200.0,
        "diameter_km": 21.0,
        "geological_period": "Eratosthenian / Imbrian",
        "description": "An impact crater situated at the lunar south pole. The interior is in permanent shadow and acts as a cold trap (<90 K) preserving volatile water ice, while the elevated rim receives over 86% annual sunlight.",
        "mission_significance": "Prime exploration target for NASA Artemis III/IV and international lunar base concepts. Critical for In-Situ Resource Utilization (ISRU) water extraction.",
        "key_features": ["Permanently Shadowed Region (PSR)", "Volatile water ice cold-trap", "Illuminated ridge rims", "Steep crater walls (slope >25°)"],
        "scientific_targets": ["Cryogenic volatiles", "Extreme thermal gradient survival", "Solar power ridge generation", "Low-temperature rover lubricants"],
        "topography": {
            "elevation_mean": -3100.0, "elevation_min": -4250.0, "elevation_max": 1450.0, "elevation_std": 1420.0,
            "slope_mean": 21.4, "slope_p90": 34.2, "terrain_roughness": 128.5, "relief_m": 5700.0
        },
        "geology": {
            "lithology_category": "polar_permafrost_ice",
            "rock_type": "Anorthositic Highland Regolith with Cryogenic Volatile Ice",
            "mineralogy_summary": "Plagioclase-rich feldspar (anorthosite), shattered impact breccia, trapped water-hydroxyl compounds.",
            "volcanic_character": "Non-volcanic impact excavation",
            "age_era": "Circa 3.6 - 3.1 Ga",
            "confidence": 0.94
        },
        "thermal": {
            "surface_temp_mean_k": 78.0, "surface_temp_min_k": 40.0, "surface_temp_max_k": 220.0,
            "diurnal_range_k": 180.0, "thermal_inertia_si": 52.0
        },
        "surface": {
            "albedo": 0.13, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.65, "dust_sediment_cover": 0.90
        }
    },
    {
        "id": "moon_malapert",
        "planet": "moon",
        "name": "Malapert Massif",
        "latitude": -86.0,
        "longitude": 2.7,
        "elevation_m": 5000.0,
        "diameter_km": 60.0,
        "geological_period": "Pre-Nectarian",
        "description": "A prominent elevated highland massif near the lunar South Pole. It rises ~5 km above surrounding topography, providing a prime line-of-sight to Earth for continuous direct-to-Earth communication.",
        "mission_significance": "Key communications hub and candidate landing site for NASA Artemis human landing system (HLS).",
        "key_features": ["High solar illumination (>88%)", "Continuous direct-to-Earth line of sight", "Rugged anorthositic terrain", "Highland plateau"],
        "scientific_targets": ["Artemis base camp comms", "Solar power station", "South Pole-Aitken basin ejecta sampling"],
        "topography": {
            "elevation_mean": 4200.0, "elevation_min": 1800.0, "elevation_max": 5120.0, "elevation_std": 890.0,
            "slope_mean": 14.8, "slope_p90": 26.5, "terrain_roughness": 88.0, "relief_m": 3320.0
        },
        "geology": {
            "lithology_category": "silicified_craton",
            "rock_type": "Ferroan Anorthosite and Impact Melt Sheet",
            "mineralogy_summary": "Plagioclase feldspar (>90%), pyroxene, olivine accessory minerals. Ancient lunar crust remnant.",
            "volcanic_character": "Impact-uplifted crustal block",
            "age_era": "Circa 4.3 Ga Pre-Nectarian",
            "confidence": 0.91
        },
        "thermal": {
            "surface_temp_mean_k": 175.0, "surface_temp_min_k": 110.0, "surface_temp_max_k": 225.0,
            "diurnal_range_k": 115.0, "thermal_inertia_si": 65.0
        },
        "surface": {
            "albedo": 0.14, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.52, "dust_sediment_cover": 0.85
        }
    },
    {
        "id": "moon_tranquillitatis",
        "planet": "moon",
        "name": "Mare Tranquillitatis",
        "latitude": 8.5,
        "longitude": 31.4,
        "elevation_m": -2100.0,
        "diameter_km": 870.0,
        "geological_period": "Upper Imbrian",
        "description": "Historic landing site of Apollo 11. A vast, dark lunar mare basalt plain characterised by titanium-rich (ilmenite) flood basalts, low topography, collapse pits, and crater rays.",
        "mission_significance": "First human lunar landing site (Apollo 11). Baseline ground truth for lunar surface sample calibration, titanium resource extraction, and lava tube cavern exploration.",
        "key_features": ["High-titanium basalt flows", "Mare collapse pits / lava tubes", "Low average slope (<4°)", "Fine cohesive regolith"],
        "scientific_targets": ["Ilmenite oxygen extraction", "Subsurface lava tube habitation", "High-speed rover traversing"],
        "topography": {
            "elevation_mean": -2150.0, "elevation_min": -2400.0, "elevation_max": -1800.0, "elevation_std": 110.0,
            "slope_mean": 3.8, "slope_p90": 7.2, "terrain_roughness": 18.5, "relief_m": 600.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "High-Titanium Flood Basalt (Ilmenite-rich)",
            "mineralogy_summary": "Pyroxene (augite/pigeonite), plagioclase, ilmenite (FeTiO3 up to 13 wt%), olivine.",
            "volcanic_character": "Effusive flood volcanism",
            "age_era": "3.55 - 3.80 Ga Imbrian",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 255.0, "surface_temp_min_k": 100.0, "surface_temp_max_k": 390.0,
            "diurnal_range_k": 290.0, "thermal_inertia_si": 48.0
        },
        "surface": {
            "albedo": 0.08, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.28, "dust_sediment_cover": 0.95
        }
    },
    {
        "id": "moon_aristarchus",
        "planet": "moon",
        "name": "Aristarchus Plateau",
        "latitude": 23.7,
        "longitude": -47.4,
        "elevation_m": -1000.0,
        "diameter_km": 170.0,
        "geological_period": "Copernican / Imbrian",
        "description": "An elevated volcanic plateau famous for pyroclastic glass deposits, extensive sinuous rilles (Vallis Schröteri), active radon degassing detections, and complex impact craters.",
        "mission_significance": "Richest regional concentration of volcanic pyroclastic resources, volatiles, and thorium on the lunar nearside.",
        "key_features": ["Vallis Schröteri sinuous rille", "Pyroclastic volcanic glass blankets", "High thorium anomaly", "Fresh Copernican impact ejecta"],
        "scientific_targets": ["Pyroclastic ore mining", "Lunar volcanism evolution", "Transient lunar phenomena investigation"],
        "topography": {
            "elevation_mean": -850.0, "elevation_min": -3200.0, "elevation_max": 1800.0, "elevation_std": 680.0,
            "slope_mean": 11.2, "slope_p90": 22.8, "terrain_roughness": 72.0, "relief_m": 5000.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Pyroclastic Glass and KREEP Basalts",
            "mineralogy_summary": "Orange and black volcanic glass beads, clinopyroxene, KREEP (potassium, rare earths, phosphorus).",
            "volcanic_character": "Explosive fire-fountain volcanism and collapse rilles",
            "age_era": "3.6 Ga (plateau) / 450 Ma (crater)",
            "confidence": 0.92
        },
        "thermal": {
            "surface_temp_mean_k": 250.0, "surface_temp_min_k": 95.0, "surface_temp_max_k": 388.0,
            "diurnal_range_k": 293.0, "thermal_inertia_si": 56.0
        },
        "surface": {
            "albedo": 0.18, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.48, "dust_sediment_cover": 0.88
        }
    },
    {
        "id": "moon_copernicus",
        "planet": "moon",
        "name": "Copernicus Crater",
        "latitude": 9.6,
        "longitude": -20.1,
        "elevation_m": -3800.0,
        "diameter_km": 93.0,
        "geological_period": "Copernican",
        "description": "Archetypal complex lunar impact crater featuring terraced rim walls, impact melt pools, a multi-peaked central uplift exposing deep crustal troctolite and olivine.",
        "mission_significance": "Benchmark for Copernican cratering timescale; exposes deep crustal magmatic cumulates.",
        "key_features": ["Terraced crater walls", "Central peak complex (1.2 km high)", "Radial ejecta rays", "Impact melt ponds"],
        "scientific_targets": ["Impact dynamics verification", "Deep lunar crust sampling", "Steep slope rover climbing"],
        "topography": {
            "elevation_mean": -2400.0, "elevation_min": -4100.0, "elevation_max": 900.0, "elevation_std": 1250.0,
            "slope_mean": 18.6, "slope_p90": 31.0, "terrain_roughness": 115.0, "relief_m": 5000.0
        },
        "geology": {
            "lithology_category": "impact_breccia",
            "rock_type": "Impact Breccia and Shocked Olivine Troctolite",
            "mineralogy_summary": "Magnesian olivine, plagioclase, shocked glass, maskelynite.",
            "volcanic_character": "Impact excavation of deep plutonic rocks",
            "age_era": "Circa 800 Ma Copernican",
            "confidence": 0.95
        },
        "thermal": {
            "surface_temp_mean_k": 248.0, "surface_temp_min_k": 92.0, "surface_temp_max_k": 385.0,
            "diurnal_range_k": 293.0, "thermal_inertia_si": 68.0
        },
        "surface": {
            "albedo": 0.20, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.62, "dust_sediment_cover": 0.78
        }
    }
]

MARS_REGIONS = [
    {
        "id": "mars_jezero",
        "planet": "mars",
        "name": "Jezero Crater",
        "latitude": 18.38,
        "longitude": 77.58,
        "elevation_m": -2500.0,
        "diameter_km": 49.0,
        "geological_period": "Noachian / Early Hesperian",
        "description": "Landing site of NASA's Mars 2020 Perseverance rover. An ancient open-basin paleolake fed by two river systems with an exceptionally well-preserved prominent river delta rich in smectite clays and carbonate minerals.",
        "mission_significance": "Primary astrobiological sample return candidate. Deltaic sediments have high biosignature preservation potential.",
        "key_features": ["Ancient river delta deposit", "Carbonate & smectite clay minerals", "Crater rim bedrock outcrops", "Volcanic floor units"],
        "scientific_targets": ["Biosignature sample caching", "Deltaic sedimentology", "Autonomous rover navigation in boulder fields"],
        "topography": {
            "elevation_mean": -2480.0, "elevation_min": -2700.0, "elevation_max": -1950.0, "elevation_std": 165.0,
            "slope_mean": 6.8, "slope_p90": 16.4, "terrain_roughness": 32.0, "relief_m": 750.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Fluvial-Lacustrine Siltstone, Clay, and Olivine-Cumulate Basalt",
            "mineralogy_summary": "Fe/Mg smectite clays, magnesium carbonates, olivine, pyroxene, sulfate salts.",
            "volcanic_character": "Volcanic igneous crater floor overlain by sedimentary delta",
            "age_era": "3.8 - 3.5 Ga Noachian/Hesperian",
            "confidence": 0.97
        },
        "thermal": {
            "surface_temp_mean_k": 218.0, "surface_temp_min_k": 182.0, "surface_temp_max_k": 278.0,
            "diurnal_range_k": 96.0, "thermal_inertia_si": 285.0
        },
        "surface": {
            "albedo": 0.16, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.38, "dust_sediment_cover": 0.65
        }
    },
    {
        "id": "mars_gale",
        "planet": "mars",
        "name": "Gale Crater & Mount Sharp",
        "latitude": -5.4,
        "longitude": 137.8,
        "elevation_m": -4500.0,
        "diameter_km": 154.0,
        "geological_period": "Late Noachian / Hesperian",
        "description": "Explored by NASA's Curiosity rover. An immense impact crater holding Aeolis Mons (Mount Sharp), a central sedimentary mountain rising 5.5 km from the crater floor, displaying layered mudstones, clay-bearing units, and sulfate strata.",
        "mission_significance": "Demonstrated that ancient Mars possessed long-lived habitable freshwater lake environments with all essential organic elements.",
        "key_features": ["Mount Sharp 5.5 km sedimentary mound", "Fluvial mudstones & sandstones", "Sulfate-bearing transition strata", "Active barchan sand dunes"],
        "scientific_targets": ["Habitability transitions", "Long-term rover wheel wear on sharp ventifacts", "Stratigraphic drilling"],
        "topography": {
            "elevation_mean": -3200.0, "elevation_min": -4600.0, "elevation_max": 900.0, "elevation_std": 1450.0,
            "slope_mean": 11.5, "slope_p90": 24.0, "terrain_roughness": 84.0, "relief_m": 5500.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Lacustrine Mudstone, Sandstone, and Magnesium Sulfate",
            "mineralogy_summary": "Nontronite/saponite clays, hematite, jarosite, calcium/magnesium sulfates, amorphous silica.",
            "volcanic_character": "Sedimentary fill derived from basaltic crust",
            "age_era": "3.7 - 3.2 Ga Hesperian",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 222.0, "surface_temp_min_k": 190.0, "surface_temp_max_k": 285.0,
            "diurnal_range_k": 95.0, "thermal_inertia_si": 310.0
        },
        "surface": {
            "albedo": 0.18, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.42, "dust_sediment_cover": 0.58
        }
    },
    {
        "id": "mars_olympus",
        "planet": "mars",
        "name": "Olympus Mons",
        "latitude": 18.65,
        "longitude": -133.8,
        "elevation_m": 21287.0,
        "diameter_km": 600.0,
        "geological_period": "Amazonian / Hesperian",
        "description": "The largest volcano in the Solar System. A monumental basaltic shield volcano towering nearly 22 km above datum, crowned by a 80 km wide nested caldera and bounded by an outer 6 km high basal scarp.",
        "mission_significance": "Study of planetary super-volcanism, atmospheric boundary layer extremes, and unweathered basaltic lava flows.",
        "key_features": ["21.9 km vertical relief", "Massive nested summit calderas", "Basal cliff scarp (6-8 km high)", "Extensive lava flow tubes"],
        "scientific_targets": ["Extreme volcanic morphology", "Low atmospheric density aerodynamics", "Lava tube shelter surveys"],
        "topography": {
            "elevation_mean": 14500.0, "elevation_min": 2500.0, "elevation_max": 21287.0, "elevation_std": 4800.0,
            "slope_mean": 6.5, "slope_p90": 28.5, "terrain_roughness": 142.0, "relief_m": 18787.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Tholeiitic Flood Basalt and Pahoehoe Lava Sheets",
            "mineralogy_summary": "Pyroxene, plagioclase feldspar, titanomagnetite, minor olivine.",
            "volcanic_character": "Effusive basaltic shield volcano (hotspot mantle plume)",
            "age_era": "3.0 Ga to <100 Ma Amazonian",
            "confidence": 0.96
        },
        "thermal": {
            "surface_temp_mean_k": 185.0, "surface_temp_min_k": 145.0, "surface_temp_max_k": 240.0,
            "diurnal_range_k": 95.0, "thermal_inertia_si": 120.0
        },
        "surface": {
            "albedo": 0.24, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.55, "dust_sediment_cover": 0.85
        }
    },
    {
        "id": "mars_valles_marineris",
        "planet": "mars",
        "name": "Valles Marineris (Coprates Chasma)",
        "latitude": -14.0,
        "longitude": -59.2,
        "elevation_m": -4000.0,
        "diameter_km": 4000.0,
        "geological_period": "Hesperian",
        "description": "The grand canyon of Mars, spanning 4000 km in length and up to 10 km in depth. Coprates Chasma reveals gigantic exposed stratigraphic sequences of the Martian crust and colossal landslide debris aprons.",
        "mission_significance": "Provides the deepest accessible geological cross-section of the Martian crust and candidate sites for recurring slope lineae (RSL).",
        "key_features": ["10 km deep canyon walls", "Layered crustal stratigraphy", "Colossal landslide lobes", "Sulfate interior layered deposits"],
        "scientific_targets": ["Crustal cross-section analysis", "Hydrated mineral deposits", "Cliff-scaling climbing rovers"],
        "topography": {
            "elevation_mean": -2500.0, "elevation_min": -8500.0, "elevation_max": 3800.0, "elevation_std": 3200.0,
            "slope_mean": 24.5, "slope_p90": 42.0, "terrain_roughness": 185.0, "relief_m": 12300.0
        },
        "geology": {
            "lithology_category": "acidic_sulfate_gossan",
            "rock_type": "Basaltic Layered Wallrock with Polyhydrated Sulfates and Hematite",
            "mineralogy_summary": "Kieserite, gypsum, jarosite, ferric oxides, layered flood basalts.",
            "volcanic_character": "Tectonic rift valley with volcano-sedimentary fill",
            "age_era": "3.5 - 2.5 Ga Hesperian",
            "confidence": 0.95
        },
        "thermal": {
            "surface_temp_mean_k": 225.0, "surface_temp_min_k": 188.0, "surface_temp_max_k": 290.0,
            "diurnal_range_k": 102.0, "thermal_inertia_si": 340.0
        },
        "surface": {
            "albedo": 0.15, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.72, "dust_sediment_cover": 0.52
        }
    },
    {
        "id": "mars_mawrth_vallis",
        "planet": "mars",
        "name": "Mawrth Vallis",
        "latitude": 23.99,
        "longitude": -18.96,
        "elevation_m": -2200.0,
        "diameter_km": 636.0,
        "geological_period": "Early Noachian",
        "description": "One of the oldest outflow channels on Mars. Displays a thick sequence of diverse phyllosilicate (clay) strata, grading from Fe/Mg smectites at the base to Al-rich clays (kaolinite, montmorillonite) and hydrated silica at the top.",
        "mission_significance": "Candidate landing site for ExoMars Rosalind Franklin. Represents prime Noachian aqueous alteration environment.",
        "key_features": ["Stratified clay sequences", "Inverted paleochannels", "High phyllosilicate abundance", "Ancient eroded terrain"],
        "scientific_targets": ["Aqueous alteration sequence", "Deep subsurface biomarker preservation", "Drilling into phyllosilicate layers"],
        "topography": {
            "elevation_mean": -2100.0, "elevation_min": -3200.0, "elevation_max": -900.0, "elevation_std": 450.0,
            "slope_mean": 7.4, "slope_p90": 15.8, "terrain_roughness": 38.0, "relief_m": 2300.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Stratified Smectite-Kaolinite Clays and Hydrated Silica",
            "mineralogy_summary": "Nontronite, saponite, montmorillonite, kaolinite, opal-A, ferric oxides.",
            "volcanic_character": "Aqueously altered ancient volcanic basement",
            "age_era": ">3.8 Ga Early Noachian",
            "confidence": 0.96
        },
        "thermal": {
            "surface_temp_mean_k": 216.0, "surface_temp_min_k": 180.0, "surface_temp_max_k": 275.0,
            "diurnal_range_k": 95.0, "thermal_inertia_si": 290.0
        },
        "surface": {
            "albedo": 0.17, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.0, "roughness_submeter": 0.35, "dust_sediment_cover": 0.60
        }
    }
]

# Earth Analog Sites Database (Curated, scientifically published planetary analogs)
EARTH_ANALOG_CATALOG = [
    {
        "id": "earth_atacama",
        "name": "Atacama Desert (Yungay / Salar de Atacama)",
        "country": "Chile",
        "latitude": -24.08,
        "longitude": -69.87,
        "elevation_m": 2300.0,
        "geological_context": "Hyper-arid desert basin enclosed between the Andes and Coastal Range. Has experienced continuous hyper-aridity for >15 million years with negligible rain, intense UV radiation, and high nitrate/perchlorate soil concentrations.",
        "real_world_missions": ["NASA Viking life detection instrument benchmark", "ESA ExoMars rover field trials", "Atacama Rover Astrobiology Drilling Studies (ARADS)"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Extensive desert pavements, sand dunes, and salar polygons",
            "drilling_isru": "Exceptional - Deep subsurface drilling for crypto-endolithic microbes and salts",
            "sensor_calibration": "High - Optical, hyperspectral, and radar calibration over flat dry salt pans"
        },
        "topography": {
            "elevation_mean": 2350.0, "elevation_min": 1800.0, "elevation_max": 3100.0, "elevation_std": 240.0,
            "slope_mean": 5.2, "slope_p90": 12.8, "terrain_roughness": 24.0, "relief_m": 1300.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Evaporitic Halite, Gypsum, and Perchlorate-bearing Regolith",
            "mineralogy_summary": "Halite, anhydrite, gypsum, thenardite, perchlorate/nitrate salts, clay fractions.",
            "volcanic_character": "Volcanic-sedimentary endorheic basin",
            "age_era": "Miocene to Holocene",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 295.0, "surface_temp_min_k": 272.0, "surface_temp_max_k": 322.0,
            "diurnal_range_k": 50.0, "thermal_inertia_si": 380.0
        },
        "surface": {
            "albedo": 0.28, "bare_ground_ratio": 0.99, "vegetation_ndvi": 0.02, "roughness_submeter": 0.32, "dust_sediment_cover": 0.82
        }
    },
    {
        "id": "earth_askja_holuhraun",
        "name": "Askja Caldera & Holuhraun Lava Field",
        "country": "Iceland",
        "latitude": 65.03,
        "longitude": -16.75,
        "elevation_m": 1050.0,
        "geological_context": "Vast basaltic lava field in the volcanic northern rift zone. Characterised by fresh pahoehoe and a'a basalt flows, volcanic ash pumice, cinder cones, and subglacial hyaloclastites.",
        "real_world_missions": ["NASA Apollo astronaut geological field training (1965-1967)", "NASA Artemis astronaut field training", "ESA rover obstacle traversal testing"],
        "exploration_suitability": {
            "rover_mobility": "Extreme Challenge - Razor-sharp a'a basalt blocks test chassis suspension and wheel grousers",
            "drilling_isru": "High - Basalt core drilling, hydrothermal alteration investigation",
            "sensor_calibration": "Very High - Basaltic spectral and radar backscatter validation"
        },
        "topography": {
            "elevation_mean": 980.0, "elevation_min": 650.0, "elevation_max": 1510.0, "elevation_std": 210.0,
            "slope_mean": 8.5, "slope_p90": 21.0, "terrain_roughness": 96.0, "relief_m": 860.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Tholeiitic Basalt, Hyaloclastite, and Rhyolitic Tephra",
            "mineralogy_summary": "Augite, plagioclase (labradorite), olivine, volcanic glass, palagonite.",
            "volcanic_character": "Active rift zone fissure volcanism and calderas",
            "age_era": "Holocene (1875 Askja eruption, 2014 Holuhraun flow)",
            "confidence": 0.99
        },
        "thermal": {
            "surface_temp_mean_k": 271.0, "surface_temp_min_k": 248.0, "surface_temp_max_k": 298.0,
            "diurnal_range_k": 50.0, "thermal_inertia_si": 420.0
        },
        "surface": {
            "albedo": 0.10, "bare_ground_ratio": 0.97, "vegetation_ndvi": 0.04, "roughness_submeter": 0.74, "dust_sediment_cover": 0.25
        }
    },
    {
        "id": "earth_mcmurdo_dry_valleys",
        "name": "McMurdo Dry Valleys (Taylor / University Valley)",
        "country": "Antarctica",
        "latitude": -77.85,
        "longitude": 160.50,
        "elevation_m": 1200.0,
        "geological_context": "Hyper-arid, polar cold desert kept ice-free by katabatic winds. Features polygonally patterned ground, dry permafrost, subglacial brine seeps (Blood Falls), and endolithic microbial colonies.",
        "real_world_missions": ["NASA Phoenix Mars Lander cryogenic soil analog", "NASA Mars Icebreaker drilling project", "Astrobiology extreme cold habitability limits"],
        "exploration_suitability": {
            "rover_mobility": "High - Polygonal permafrost ground, loose regolith, ventifacts",
            "drilling_isru": "Exceptional - Testing deep permafrost and dry ice-cemented ground drills",
            "sensor_calibration": "Very High - Ground-penetrating radar (GPR) detection of subsurface ice"
        },
        "topography": {
            "elevation_mean": 950.0, "elevation_min": 50.0, "elevation_max": 2200.0, "elevation_std": 480.0,
            "slope_mean": 16.2, "slope_p90": 32.5, "terrain_roughness": 110.0, "relief_m": 2150.0
        },
        "geology": {
            "lithology_category": "polar_permafrost_ice",
            "rock_type": "Ice-Cemented Till, Ferrar Dolerite, and Beacon Sandstone",
            "mineralogy_summary": "Pyroxene, plagioclase, quartz, halite/mirabilite salts, interstitial ground ice.",
            "volcanic_character": "Jurassic dolerite sills intruding sandstone",
            "age_era": "Jurassic bedrock with Quaternary cryogenic regolith",
            "confidence": 0.97
        },
        "thermal": {
            "surface_temp_mean_k": 253.0, "surface_temp_min_k": 220.0, "surface_temp_max_k": 280.0,
            "diurnal_range_k": 60.0, "thermal_inertia_si": 480.0
        },
        "surface": {
            "albedo": 0.22, "bare_ground_ratio": 0.98, "vegetation_ndvi": 0.01, "roughness_submeter": 0.58, "dust_sediment_cover": 0.70
        }
    },
    {
        "id": "earth_mojave_death_valley",
        "name": "Mojave Desert & Death Valley (Cinder Cones & Alluvial Fans)",
        "country": "United States",
        "latitude": 35.68,
        "longitude": -116.22,
        "elevation_m": -86.0,
        "geological_context": "Basin and Range desert featuring extreme arid environments: active sand dunes (Dumont), basaltic cinder cone fields, steep alluvial fans, and salt playas (Badwater Basin).",
        "real_world_missions": ["NASA JPL Mars Yard and Field Rover Testing (Curiosity, Perseverance, Mars Exploration Rovers)", "NASA Sample Return terrain testbed"],
        "exploration_suitability": {
            "rover_mobility": "Gold Standard - NASA JPL primary testing terrain for wheel traction, slip, and rock hazards",
            "drilling_isru": "Moderate - Salt crust and basaltic core drilling",
            "sensor_calibration": "High - Thermal radiometry and hyperspectral camera calibration"
        },
        "topography": {
            "elevation_mean": 420.0, "elevation_min": -86.0, "elevation_max": 1850.0, "elevation_std": 410.0,
            "slope_mean": 10.4, "slope_p90": 26.0, "terrain_roughness": 65.0, "relief_m": 1936.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Alluvial Gravels, Olivine Basalt Cinder Cones, and Borate-Halite Playas",
            "mineralogy_summary": "Olivine, pyroxene, plagioclase, halite, borax, illite clay.",
            "volcanic_character": "Quaternary basaltic cinder cone eruptions",
            "age_era": "Pleistocene to Holocene",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 302.0, "surface_temp_min_k": 275.0, "surface_temp_max_k": 332.0,
            "diurnal_range_k": 57.0, "thermal_inertia_si": 360.0
        },
        "surface": {
            "albedo": 0.25, "bare_ground_ratio": 0.96, "vegetation_ndvi": 0.05, "roughness_submeter": 0.45, "dust_sediment_cover": 0.75
        }
    },
    {
        "id": "earth_mauna_kea_hiseas",
        "name": "Mauna Kea & Mauna Loa (HI-SEAS Habitat)",
        "country": "United States",
        "latitude": 19.82,
        "longitude": -155.47,
        "elevation_m": 3800.0,
        "geological_context": "High-altitude oceanic shield volcano. Features tholeiitic and alkalic basalt lava tubes, cinder cones, weathering tephra, and periglacial stone stripes above the tree line.",
        "real_world_missions": ["HI-SEAS (Hawaii Space Exploration Analog and Simulation) long-duration crew isolation missions", "NASA PSTAR basaltic weathering research", "Artemis lava tube exploration robotics"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Varied basaltic terrain from smooth pahoehoe to treacherous a'a blocks",
            "drilling_isru": "High - Basaltic regolith extraction and sintering experiments",
            "sensor_calibration": "High - High-altitude low water-vapor infrared astronomical calibration"
        },
        "topography": {
            "elevation_mean": 3200.0, "elevation_min": 1800.0, "elevation_max": 4205.0, "elevation_std": 580.0,
            "slope_mean": 9.8, "slope_p90": 22.4, "terrain_roughness": 82.0, "relief_m": 2405.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Oceanic Tholeiitic and Alkalic Basalt, Volcanic Tephra",
            "mineralogy_summary": "Olivine (forsterite), augite pyroxene, calcic plagioclase, palagonite tephra.",
            "volcanic_character": "Active shield volcano hotspot mantle plume",
            "age_era": "Pleistocene to Holocene",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 282.0, "surface_temp_min_k": 260.0, "surface_temp_max_k": 305.0,
            "diurnal_range_k": 45.0, "thermal_inertia_si": 410.0
        },
        "surface": {
            "albedo": 0.12, "bare_ground_ratio": 0.95, "vegetation_ndvi": 0.03, "roughness_submeter": 0.62, "dust_sediment_cover": 0.35
        }
    },
    {
        "id": "earth_ladakh_changthang",
        "name": "Ladakh & Tso Kar Basin (Himalayan Cold Desert)",
        "country": "India",
        "latitude": 33.30,
        "longitude": 78.00,
        "elevation_m": 4530.0,
        "geological_context": "Trans-Himalayan high-altitude cold desert plateau (>4500 m). Features intense UV radiation, low barometric pressure, hyper-saline alkaline lakes (Tso Kar), permafrost patterned ground, and ophiolitic rocks.",
        "real_world_missions": ["ISRO Mars analog field studies", "Astrobiology extreme high-altitude UV survival research", "Cold arid rover mechanical subsystem testing"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Expansive saline gravel plains, scree slopes, and braided outwash fans",
            "drilling_isru": "Exceptional - High-altitude permafrost drilling and borate/sulfate salt extraction",
            "sensor_calibration": "High - Atmospheric boundary layer testing at 0.58 atm pressure"
        },
        "topography": {
            "elevation_mean": 4750.0, "elevation_min": 4200.0, "elevation_max": 5900.0, "elevation_std": 420.0,
            "slope_mean": 12.6, "slope_p90": 28.0, "terrain_roughness": 85.0, "relief_m": 1700.0
        },
        "geology": {
            "lithology_category": "polar_permafrost_ice",
            "rock_type": "Indus Suture Ophiolites, Permafrost Gravels, and Borate-Sulfate Evaporites",
            "mineralogy_summary": "Serpentine, basalt, radiolarian chert, thenardite, borax, gypsum.",
            "volcanic_character": "Cretaceous-Tertiary ophiolite collision zone",
            "age_era": "Cretaceous to Holocene",
            "confidence": 0.95
        },
        "thermal": {
            "surface_temp_mean_k": 268.0, "surface_temp_min_k": 240.0, "surface_temp_max_k": 298.0,
            "diurnal_range_k": 58.0, "thermal_inertia_si": 440.0
        },
        "surface": {
            "albedo": 0.22, "bare_ground_ratio": 0.96, "vegetation_ndvi": 0.04, "roughness_submeter": 0.50, "dust_sediment_cover": 0.65
        }
    },
    {
        "id": "earth_rio_tinto",
        "name": "Rio Tinto (Iberian Pyrite Belt)",
        "country": "Spain",
        "latitude": 37.69,
        "longitude": -6.55,
        "elevation_m": 350.0,
        "geological_context": "Vast massive sulfide deposit naturally oxidized into an extremely acidic river system (pH 1.5 - 2.5). Characterised by iron oxide and jarosite-rich gossans that mirror the mineralogy of Mars Meridiani Planum.",
        "real_world_missions": ["NASA Mars Exploration Rover (MER) Opportunity jarosite analog benchmark", "ESA ExoMars drill testing in gossans", "MARTE (Mars Astrobiology Research and Technology Experiment) autonomous drilling"],
        "exploration_suitability": {
            "rover_mobility": "Moderate - Rocky ferricrete terraces and acidic river margins",
            "drilling_isru": "Exceptional - Acid-resistant robotic drill testing in massive iron gossan",
            "sensor_calibration": "World-Class - Raman and Mössbauer spectrometer calibration for jarosite and goethite"
        },
        "topography": {
            "elevation_mean": 380.0, "elevation_min": 180.0, "elevation_max": 620.0, "elevation_std": 95.0,
            "slope_mean": 8.2, "slope_p90": 18.5, "terrain_roughness": 45.0, "relief_m": 440.0
        },
        "geology": {
            "lithology_category": "acidic_sulfate_gossan",
            "rock_type": "Iron-Sulfate Gossan, Massive Sulfides, and Ferricrete",
            "mineralogy_summary": "Jarosite [KFe3(SO4)2(OH)6], goethite, hematite, copiapite, pyrite.",
            "volcanic_character": "Volcanogenic massive sulfide (VMS) deposits",
            "age_era": "Carboniferous (350 Ma) with active modern oxidation",
            "confidence": 0.99
        },
        "thermal": {
            "surface_temp_mean_k": 293.0, "surface_temp_min_k": 278.0, "surface_temp_max_k": 315.0,
            "diurnal_range_k": 37.0, "thermal_inertia_si": 520.0
        },
        "surface": {
            "albedo": 0.16, "bare_ground_ratio": 0.88, "vegetation_ndvi": 0.12, "roughness_submeter": 0.42, "dust_sediment_cover": 0.40
        }
    },
    {
        "id": "earth_haughton_crater",
        "name": "Haughton Impact Crater (Devon Island, Arctic)",
        "country": "Canada",
        "latitude": 75.38,
        "longitude": -89.67,
        "elevation_m": 250.0,
        "geological_context": "A 23 km diameter meteorite impact crater set in a polar desert. Preserves allogenic impact melt breccias, shattered bedrock, hydrothermal paleolake sediments, and permafrost ice ground.",
        "real_world_missions": ["NASA Haughton-Mars Project (HMP) continuous operational base since 1997", "FMARS (Flashline Mars Arctic Research Station)", "Autonomous planetary rover navigation"],
        "exploration_suitability": {
            "rover_mobility": "Exceptional - Impact crater interior, ejecta blanket, and gullies replicate lunar and Martian crater traverses",
            "drilling_isru": "High - Shattered impact rock and permafrost core sample drilling",
            "sensor_calibration": "Very High - Multi-spectral and LiDAR surveying of crater morphometry"
        },
        "topography": {
            "elevation_mean": 280.0, "elevation_min": 60.0, "elevation_max": 490.0, "elevation_std": 85.0,
            "slope_mean": 7.8, "slope_p90": 17.5, "terrain_roughness": 52.0, "relief_m": 430.0
        },
        "geology": {
            "lithology_category": "impact_breccia",
            "rock_type": "Impact Melt Breccia, Shocked Dolomite, and Paleolake Sediment",
            "mineralogy_summary": "Shocked quartz, calcite, dolomite, gypsum hydrothermal veins, impact glass.",
            "volcanic_character": "Hypervelocity impact structure",
            "age_era": "Eocene (approx 39 Ma)",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 256.0, "surface_temp_min_k": 230.0, "surface_temp_max_k": 285.0,
            "diurnal_range_k": 55.0, "thermal_inertia_si": 450.0
        },
        "surface": {
            "albedo": 0.19, "bare_ground_ratio": 0.98, "vegetation_ndvi": 0.02, "roughness_submeter": 0.55, "dust_sediment_cover": 0.65
        }
    },
    {
        "id": "earth_pilbara_craton",
        "name": "Pilbara Craton (North Pole Dome & Strelley Pool)",
        "country": "Australia",
        "latitude": -21.15,
        "longitude": 119.35,
        "elevation_m": 310.0,
        "geological_context": "One of only two pristine exposed Archean crustal blocks on Earth (3.5 billion years old). Contains Earth's oldest evidence of life: fossilized stromatolites in silicified barite and hydrothermal chert beds.",
        "real_world_missions": ["NASA Mars 2020 / ESA ExoMars Joint Science Team field expedition (2019, 2023)", "Perseverance sample return targeting training"],
        "exploration_suitability": {
            "rover_mobility": "High - Ancient silica-cemented rugged ridges and ironstone plains",
            "drilling_isru": "Exceptional - Micro-coring silicified stromatolite biosignatures",
            "sensor_calibration": "World-Class - SHERLOC, PIXL, and SuperCam equivalent instrument validation"
        },
        "topography": {
            "elevation_mean": 340.0, "elevation_min": 150.0, "elevation_max": 580.0, "elevation_std": 75.0,
            "slope_mean": 9.2, "slope_p90": 20.5, "terrain_roughness": 48.0, "relief_m": 430.0
        },
        "geology": {
            "lithology_category": "silicified_craton",
            "rock_type": "Silicified Chert, Barite, Komatiitic Basalt, and BIF",
            "mineralogy_summary": "Microcrystalline quartz (chert), barite (BaSO4), hematite, magnetite, serpentine.",
            "volcanic_character": "Submarine ultramafic volcanism and hydrothermal chert precipitation",
            "age_era": "Paleoarchean (3.48 - 3.52 Ga) - Exact contemporary to Noachian Mars",
            "confidence": 0.99
        },
        "thermal": {
            "surface_temp_mean_k": 305.0, "surface_temp_min_k": 282.0, "surface_temp_max_k": 328.0,
            "diurnal_range_k": 46.0, "thermal_inertia_si": 510.0
        },
        "surface": {
            "albedo": 0.18, "bare_ground_ratio": 0.92, "vegetation_ndvi": 0.08, "roughness_submeter": 0.48, "dust_sediment_cover": 0.45
        }
    },
    {
        "id": "earth_salar_de_uyuni",
        "name": "Salar de Uyuni",
        "country": "Bolivia",
        "latitude": -20.13,
        "longitude": -67.49,
        "elevation_m": 3656.0,
        "geological_context": "The world's largest salt flat (10,582 km²). Exceptionally flat expanse with elevation variations under 1 meter across the entire plateau, encrusted with a lithium-rich halite and gypsum crust.",
        "real_world_missions": ["NASA ICESat and Envisat radar/laser altimeter orbital calibration", "Planetary radar reflection modeling"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Ultra-flat polygonal salt crust ideal for long-distance high-speed rover traversing",
            "drilling_isru": "Exceptional - Lithium/magnesium brine extraction and salt core profiling",
            "sensor_calibration": "World-Class - Primary global surface benchmark for orbital altimeters and optical radiometers"
        },
        "topography": {
            "elevation_mean": 3656.0, "elevation_min": 3654.0, "elevation_max": 3662.0, "elevation_std": 1.2,
            "slope_mean": 0.3, "slope_p90": 0.8, "terrain_roughness": 3.0, "relief_m": 8.0
        },
        "geology": {
            "lithology_category": "hyperarid_playa_evaporite",
            "rock_type": "Halite, Gypsum, and Lithium-Rich Continental Evaporites",
            "mineralogy_summary": "Halite (NaCl), gypsum, ulexite, lithium carbonate, carnallite.",
            "volcanic_character": "High-Andean endorheic paleolake basin",
            "age_era": "Pleistocene to Holocene (Lake Minchin / Tauca remnants)",
            "confidence": 0.99
        },
        "thermal": {
            "surface_temp_mean_k": 285.0, "surface_temp_min_k": 260.0, "surface_temp_max_k": 310.0,
            "diurnal_range_k": 50.0, "thermal_inertia_si": 390.0
        },
        "surface": {
            "albedo": 0.65, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.00, "roughness_submeter": 0.15, "dust_sediment_cover": 0.95
        }
    },
    {
        "id": "earth_danakil_depression",
        "name": "Danakil Depression & Dallol",
        "country": "Ethiopia",
        "latitude": 14.24,
        "longitude": 40.30,
        "elevation_m": -125.0,
        "geological_context": "A volcanic rift depression located at the Afar Triple Junction, 125 m below sea level. Features hyper-saline, hyper-acidic (pH < 0) boiling hydrothermal pools, sulfur chimneys, and iron-crusted mounds.",
        "real_world_missions": ["Europlanet extreme environment research", "Astrobiology limits of life in multi-extreme environments"],
        "exploration_suitability": {
            "rover_mobility": "Extreme Hazard - Brittle salt crusts over boiling acidic brine muds",
            "drilling_isru": "Moderate - Extreme corrosion resistant sampling tools",
            "sensor_calibration": "High - Multi-spectral detection of native sulfur and iron minerals"
        },
        "topography": {
            "elevation_mean": -110.0, "elevation_min": -155.0, "elevation_max": 120.0, "elevation_std": 65.0,
            "slope_mean": 4.5, "slope_p90": 11.0, "terrain_roughness": 28.0, "relief_m": 275.0
        },
        "geology": {
            "lithology_category": "acidic_sulfate_gossan",
            "rock_type": "Native Sulfur, Potash Evaporites, and Hydrothermal Iron Chimneys",
            "mineralogy_summary": "Sulfur, halite, sylvite, hematite, jarosite, ferric chlorides.",
            "volcanic_character": "Hydrothermal phreatic explosions over active magma rift",
            "age_era": "Holocene to Active",
            "confidence": 0.97
        },
        "thermal": {
            "surface_temp_mean_k": 314.0, "surface_temp_min_k": 298.0, "surface_temp_max_k": 338.0,
            "diurnal_range_k": 40.0, "thermal_inertia_si": 420.0
        },
        "surface": {
            "albedo": 0.35, "bare_ground_ratio": 1.0, "vegetation_ndvi": 0.00, "roughness_submeter": 0.40, "dust_sediment_cover": 0.70
        }
    },
    {
        "id": "earth_craters_of_the_moon",
        "name": "Craters of the Moon National Monument",
        "country": "United States",
        "latitude": 43.46,
        "longitude": -113.56,
        "elevation_m": 1800.0,
        "geological_context": "Vast Holocene flood basalt plain in the Snake River Plain. Preserves pristine volcanic features: cinder cones, spatter ramparts, rafted lava blocks, lava tube caves, and basaltic pahoehoe ropes.",
        "real_world_missions": ["NASA Apollo 14 astronaut geological training (Edgar Mitchell, Alan Shepard)", "NASA FINESSE and SUBX volcanic field robotics projects"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Diverse basalt flows from smooth pahoehoe to rugged spatter mounds",
            "drilling_isru": "High - Basalt sample extraction and subsurface cave exploration",
            "sensor_calibration": "High - LiDAR 3D scanning of lava tubes and collapse pit entrances"
        },
        "topography": {
            "elevation_mean": 1780.0, "elevation_min": 1600.0, "elevation_max": 2005.0, "elevation_std": 68.0,
            "slope_mean": 7.2, "slope_p90": 17.8, "terrain_roughness": 62.0, "relief_m": 405.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Ferrobasalt, Pahoehoe, and Basaltic Andesite",
            "mineralogy_summary": "Plagioclase, augite, olivine, titanomagnetite, basaltic glass.",
            "volcanic_character": "Great Rift volcanic fissure eruptions",
            "age_era": "Holocene (15,000 to 2,000 years BP)",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 284.0, "surface_temp_min_k": 255.0, "surface_temp_max_k": 315.0,
            "diurnal_range_k": 60.0, "thermal_inertia_si": 450.0
        },
        "surface": {
            "albedo": 0.09, "bare_ground_ratio": 0.94, "vegetation_ndvi": 0.06, "roughness_submeter": 0.65, "dust_sediment_cover": 0.20
        }
    },
    {
        "id": "earth_lonar_crater",
        "name": "Lonar Meteorite Crater",
        "country": "India",
        "latitude": 19.98,
        "longitude": 76.51,
        "elevation_m": 560.0,
        "geological_context": "One of only four known hypervelocity impact craters in basaltic rock on Earth. Excavated into the Cretaceous Deccan Traps flood basalts, creating shock-melted glass (maskelynite) and an alkaline saline lake.",
        "real_world_missions": ["Planetary impact geology reference site", "Lunar mare impact cratering analogue studies"],
        "exploration_suitability": {
            "rover_mobility": "High - Steep crater wall rim traverse and basaltic ejecta boulder fields",
            "drilling_isru": "High - Maskelynite shock glass and saline lake sediment coring",
            "sensor_calibration": "Very High - Basalt shock metamorphism spectral signatures"
        },
        "topography": {
            "elevation_mean": 530.0, "elevation_min": 440.0, "elevation_max": 610.0, "elevation_std": 48.0,
            "slope_mean": 14.5, "slope_p90": 29.0, "terrain_roughness": 78.0, "relief_m": 170.0
        },
        "geology": {
            "lithology_category": "impact_breccia",
            "rock_type": "Shocked Basalt, Maskelynite Glass, and Impact Ejecta",
            "mineralogy_summary": "Plagioclase shocked into maskelynite, clinopyroxene, smectite, calcite.",
            "volcanic_character": "Impact excavation into Deccan Trap continental flood basalt",
            "age_era": "Pleistocene (570,000 years BP)",
            "confidence": 0.97
        },
        "thermal": {
            "surface_temp_mean_k": 300.0, "surface_temp_min_k": 280.0, "surface_temp_max_k": 320.0,
            "diurnal_range_k": 40.0, "thermal_inertia_si": 460.0
        },
        "surface": {
            "albedo": 0.14, "bare_ground_ratio": 0.85, "vegetation_ndvi": 0.15, "roughness_submeter": 0.52, "dust_sediment_cover": 0.50
        }
    },
    {
        "id": "earth_kilbourne_hole",
        "name": "Kilbourne Hole & Potrillo Volcanic Field",
        "country": "United States",
        "latitude": 31.97,
        "longitude": -106.96,
        "elevation_m": 1260.0,
        "geological_context": "A volcanic maar crater formed by phreatomagmatic explosions. Features deep crater walls exposing mantle peridotite and granulite xenoliths, basaltic ejecta bombs, and desert sand ramps.",
        "real_world_missions": ["NASA Apollo 12, 13, 14, 15, 16, 17 lunar astronaut geology training", "NASA Artemis astronaut field training exercises (2022-2024)"],
        "exploration_suitability": {
            "rover_mobility": "Very High - Maar rim sand dunes, volcanic ejecta slopes, flat crater floor",
            "drilling_isru": "High - Mantle xenolith and basaltic bomb sampling",
            "sensor_calibration": "High - Olivine and pyroxene spectral calibration"
        },
        "topography": {
            "elevation_mean": 1240.0, "elevation_min": 1150.0, "elevation_max": 1330.0, "elevation_std": 38.0,
            "slope_mean": 9.5, "slope_p90": 24.0, "terrain_roughness": 55.0, "relief_m": 180.0
        },
        "geology": {
            "lithology_category": "basaltic_volcanic",
            "rock_type": "Phreatomagmatic Maar Tephra with Mantle Peridotite Xenoliths",
            "mineralogy_summary": "Forsterite olivine, enstatite, Cr-diopside, spinel peridotite, basaltic tephra.",
            "volcanic_character": "Explosive phreatomagmatic maar volcanism",
            "age_era": "Pleistocene (24,000 - 80,000 years BP)",
            "confidence": 0.98
        },
        "thermal": {
            "surface_temp_mean_k": 298.0, "surface_temp_min_k": 272.0, "surface_temp_max_k": 325.0,
            "diurnal_range_k": 53.0, "thermal_inertia_si": 380.0
        },
        "surface": {
            "albedo": 0.20, "bare_ground_ratio": 0.94, "vegetation_ndvi": 0.06, "roughness_submeter": 0.44, "dust_sediment_cover": 0.70
        }
    }
]
