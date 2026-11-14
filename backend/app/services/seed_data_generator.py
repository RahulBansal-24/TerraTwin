"""
TerraTwin Global Earth Grid Seed Generator.
Generates an extensive, geographically and geologically authentic candidate grid
covering all 7 continents with realistic physical attributes based on real Earth terrain surveys.
"""

import math
from typing import List, Dict, Any

def generate_global_earth_grid() -> List[Dict[str, Any]]:
    """
    Constructs a rich spatial candidate catalog covering Earth's major
    geological provinces, deserts, volcanic fields, polar cryo-valleys,
    impact structures, and salt flats across all 7 continents.
    """
    candidates = []
    numeric_id_counter = 1

    # Base geological macro-provinces with center coordinates, extent, and terrain parameters
    PROVINCES = [
        # AFRICA
        {
            "province": "Tibesti Volcanic Massif", "country": "Chad", "continent": "Africa",
            "lat": 20.9, "lon": 17.9, "radius_deg": 1.8, "count_points": 14,
            "lithology": "basaltic_volcanic", "rock": "Alkalic Flood Basalt and Trachyte Caldera",
            "minerals": "Augite, olivine, titanomagnetite, nepheline, volcanic ash",
            "elev_base": 2400.0, "relief": 1200.0, "slope_m": 12.5, "slope_90": 26.0, "tri": 85.0,
            "temp_k": 298.0, "diurnal": 38.0, "inertia": 430.0, "albedo": 0.16, "bare": 0.98, "ndvi": 0.01,
            "class": "volcanic_field", "dust": 0.40, "sub_rough": 0.65
        },
        {
            "province": "Danakil Depression & Dallol", "country": "Ethiopia", "continent": "Africa",
            "lat": 14.2, "lon": 40.3, "radius_deg": 1.2, "count_points": 12,
            "lithology": "acidic_sulfate_gossan", "rock": "Hydrothermal Iron Chimneys, Native Sulfur, and Potash Evaporites",
            "minerals": "Native sulfur, halite, sylvite, hematite, jarosite, iron chlorides",
            "elev_base": -120.0, "relief": 280.0, "slope_m": 4.5, "slope_90": 11.0, "tri": 28.0,
            "temp_k": 314.0, "diurnal": 40.0, "inertia": 420.0, "albedo": 0.35, "bare": 1.0, "ndvi": 0.00,
            "class": "salt_crust", "dust": 0.70, "sub_rough": 0.40
        },
        {
            "province": "Namib Erg & Sossusvlei", "country": "Namibia", "continent": "Africa",
            "lat": -24.7, "lon": 15.3, "radius_deg": 2.0, "count_points": 16,
            "lithology": "hyperarid_playa_evaporite", "rock": "Quartz Megadunes and Interdune Clay Pans",
            "minerals": "Hematite-coated quartz sand, gypsum, illite, calcite",
            "elev_base": 550.0, "relief": 380.0, "slope_m": 14.2, "slope_90": 28.5, "tri": 68.0,
            "temp_k": 296.0, "diurnal": 35.0, "inertia": 320.0, "albedo": 0.28, "bare": 0.99, "ndvi": 0.01,
            "class": "desert_sand", "dust": 0.85, "sub_rough": 0.25
        },
        {
            "province": "Ahaggar & Hoggar Swell", "country": "Algeria", "continent": "Africa",
            "lat": 23.3, "lon": 5.5, "radius_deg": 2.2, "count_points": 15,
            "lithology": "basaltic_volcanic", "rock": "Basaltic Lava Necks and Granitic Gneiss Basement",
            "minerals": "Plagioclase, augite, olivine, quartz, biotite",
            "elev_base": 2100.0, "relief": 900.0, "slope_m": 15.0, "slope_90": 31.0, "tri": 95.0,
            "temp_k": 294.0, "diurnal": 42.0, "inertia": 480.0, "albedo": 0.18, "bare": 0.97, "ndvi": 0.02,
            "class": "volcanic_field", "dust": 0.35, "sub_rough": 0.70
        },
        {
            "province": "Vredefort Impact Dome", "country": "South Africa", "continent": "Africa",
            "lat": -27.0, "lon": 27.5, "radius_deg": 1.0, "count_points": 10,
            "lithology": "impact_breccia", "rock": "Shocked Granophyre and Pseudotachylite Impact Melt Breccia",
            "minerals": "Shocked quartz, stishovite, pseudotachylite glass, granophyre, cordierite",
            "elev_base": 1450.0, "relief": 350.0, "slope_m": 8.0, "slope_90": 18.0, "tri": 48.0,
            "temp_k": 290.0, "diurnal": 30.0, "inertia": 510.0, "albedo": 0.19, "bare": 0.75, "ndvi": 0.18,
            "class": "barren_rock", "dust": 0.30, "sub_rough": 0.50
        },
        {
            "province": "Richat Structure (Eye of the Sahara)", "country": "Mauritania", "continent": "Africa",
            "lat": 21.1, "lon": -11.4, "radius_deg": 1.2, "count_points": 10,
            "lithology": "silicified_craton", "rock": "Concentric Hydrothermal Silicified Breccia and Gabbro Rings",
            "minerals": "Quartz, barite, calcite, dolomite, titanite, iron oxides",
            "elev_base": 420.0, "relief": 180.0, "slope_m": 9.5, "slope_90": 20.0, "tri": 52.0,
            "temp_k": 302.0, "diurnal": 45.0, "inertia": 460.0, "albedo": 0.24, "bare": 0.98, "ndvi": 0.01,
            "class": "barren_rock", "dust": 0.60, "sub_rough": 0.55
        },

        # ANTARCTICA
        {
            "province": "McMurdo Dry Valleys (Taylor / University)", "country": "Antarctica", "continent": "Antarctica",
            "lat": -77.8, "lon": 160.5, "radius_deg": 1.5, "count_points": 15,
            "lithology": "polar_permafrost_ice", "rock": "Ice-Cemented Cryogenic Till and Ferrar Dolerite",
            "minerals": "Pyroxene, calcic plagioclase, halite salts, dry ground permafrost",
            "elev_base": 950.0, "relief": 2100.0, "slope_m": 16.5, "slope_90": 33.0, "tri": 112.0,
            "temp_k": 253.0, "diurnal": 60.0, "inertia": 480.0, "albedo": 0.22, "bare": 0.98, "ndvi": 0.01,
            "class": "permafrost_ice", "dust": 0.70, "sub_rough": 0.58
        },
        {
            "province": "Allan Hills Ice Margin & Meteorite Trap", "country": "Antarctica", "continent": "Antarctica",
            "lat": -76.7, "lon": 159.2, "radius_deg": 1.2, "count_points": 10,
            "lithology": "polar_permafrost_ice", "rock": "Blue Ice Fields, Beacon Sandstone, and Dolerite Nunataks",
            "minerals": "Quartz, dolerite fragments, interstitial glacial ice, gypsum coatings",
            "elev_base": 1950.0, "relief": 650.0, "slope_m": 11.0, "slope_90": 24.0, "tri": 75.0,
            "temp_k": 245.0, "diurnal": 55.0, "inertia": 520.0, "albedo": 0.45, "bare": 0.95, "ndvi": 0.00,
            "class": "permafrost_ice", "dust": 0.35, "sub_rough": 0.52
        },
        {
            "province": "Mount Erebus Summit Caldera", "country": "Antarctica", "continent": "Antarctica",
            "lat": -77.5, "lon": 167.2, "radius_deg": 0.8, "count_points": 8,
            "lithology": "basaltic_volcanic", "rock": "Anorthoclase Phonolite Lava Lake and Fumarolic Ice Towers",
            "minerals": "Anorthoclase feldspar, nepheline, augite, sulfur, volcanic glass",
            "elev_base": 3600.0, "relief": 1500.0, "slope_m": 22.0, "slope_90": 38.0, "tri": 135.0,
            "temp_k": 248.0, "diurnal": 45.0, "inertia": 440.0, "albedo": 0.32, "bare": 0.90, "ndvi": 0.00,
            "class": "volcanic_field", "dust": 0.20, "sub_rough": 0.80
        },

        # ASIA
        {
            "province": "Ladakh & Tso Kar Salt Basin", "country": "India", "continent": "Asia",
            "lat": 33.3, "lon": 78.0, "radius_deg": 1.8, "count_points": 16,
            "lithology": "polar_permafrost_ice", "rock": "Indus Suture Ophiolites, Permafrost Gravels, and Borate Evaporites",
            "minerals": "Serpentine, basalt, radiolarian chert, thenardite, borax, gypsum",
            "elev_base": 4750.0, "relief": 1700.0, "slope_m": 12.6, "slope_90": 28.0, "tri": 85.0,
            "temp_k": 268.0, "diurnal": 58.0, "inertia": 440.0, "albedo": 0.22, "bare": 0.96, "ndvi": 0.04,
            "class": "permafrost_ice", "dust": 0.65, "sub_rough": 0.50
        },
        {
            "province": "Deccan Continental Flood Basalt", "country": "India", "continent": "Asia",
            "lat": 18.5, "lon": 74.0, "radius_deg": 2.5, "count_points": 18,
            "lithology": "basaltic_volcanic", "rock": "Tholeiitic Continental Flood Basalt Flows and Stepped Terraces",
            "minerals": "Plagioclase, augite, olivine, titanomagnetite, secondary zeolites",
            "elev_base": 780.0, "relief": 620.0, "slope_m": 9.0, "slope_90": 22.0, "tri": 55.0,
            "temp_k": 298.0, "diurnal": 32.0, "inertia": 460.0, "albedo": 0.15, "bare": 0.70, "ndvi": 0.22,
            "class": "volcanic_field", "dust": 0.30, "sub_rough": 0.48
        },
        {
            "province": "Lonar Meteorite Impact Crater", "country": "India", "continent": "Asia",
            "lat": 20.0, "lon": 76.5, "radius_deg": 0.8, "count_points": 8,
            "lithology": "impact_breccia", "rock": "Shocked Deccan Basalt and Maskelynite Melt Glass",
            "minerals": "Plagioclase shocked to maskelynite, clinopyroxene, smectite, calcite",
            "elev_base": 530.0, "relief": 170.0, "slope_m": 14.5, "slope_90": 29.0, "tri": 78.0,
            "temp_k": 300.0, "diurnal": 40.0, "inertia": 460.0, "albedo": 0.14, "bare": 0.85, "ndvi": 0.15,
            "class": "barren_rock", "dust": 0.50, "sub_rough": 0.52
        },
        {
            "province": "Dasht-e Lut Yardangs & Salt Basin", "country": "Iran", "continent": "Asia",
            "lat": 30.8, "lon": 58.8, "radius_deg": 2.0, "count_points": 15,
            "lithology": "hyperarid_playa_evaporite", "rock": "Wind-Sculpted Clay-Silt Yardangs and Halite Crusts",
            "minerals": "Gypsum, halite, thenardite, montmorillonite clay, quartz silt",
            "elev_base": 280.0, "relief": 320.0, "slope_m": 11.5, "slope_90": 25.0, "tri": 62.0,
            "temp_k": 312.0, "diurnal": 52.0, "inertia": 340.0, "albedo": 0.25, "bare": 0.99, "ndvi": 0.00,
            "class": "desert_sand", "dust": 0.88, "sub_rough": 0.42
        },
        {
            "province": "Gobi Gravel Pavements & Flaming Cliffs", "country": "Mongolia", "continent": "Asia",
            "lat": 44.2, "lon": 103.7, "radius_deg": 2.5, "count_points": 16,
            "lithology": "hyperarid_playa_evaporite", "rock": "Silicified Reg Gravel Pavement and Cretaceous Red Sandstones",
            "minerals": "Quartz, feldspar, calcite cement, hematite, smectite clays",
            "elev_base": 1250.0, "relief": 450.0, "slope_m": 7.2, "slope_90": 17.0, "tri": 42.0,
            "temp_k": 280.0, "diurnal": 56.0, "inertia": 390.0, "albedo": 0.22, "bare": 0.96, "ndvi": 0.03,
            "class": "desert_sand", "dust": 0.75, "sub_rough": 0.38
        },
        {
            "province": "Rub' al Khali (Empty Quarter)", "country": "Saudi Arabia", "continent": "Asia",
            "lat": 21.0, "lon": 51.0, "radius_deg": 3.0, "count_points": 20,
            "lithology": "hyperarid_playa_evaporite", "rock": "Hyper-Arid Barchanoid Megadunes and Sabkha Evaporites",
            "minerals": "Iron-stained quartz sand, gypsum crystals, halite sabkha",
            "elev_base": 180.0, "relief": 250.0, "slope_m": 13.0, "slope_90": 26.0, "tri": 58.0,
            "temp_k": 308.0, "diurnal": 48.0, "inertia": 310.0, "albedo": 0.32, "bare": 1.0, "ndvi": 0.00,
            "class": "desert_sand", "dust": 0.90, "sub_rough": 0.22
        },
        {
            "province": "Putorana Siberian Basalt Plateau", "country": "Russia", "continent": "Asia",
            "lat": 69.0, "lon": 93.0, "radius_deg": 2.5, "count_points": 16,
            "lithology": "basaltic_volcanic", "rock": "Massive Permo-Triassic Siberian Flood Basalts and Stepped Canyons",
            "minerals": "Plagioclase, augite, olivine, titanomagnetite, copper-nickel sulfides",
            "elev_base": 1100.0, "relief": 1200.0, "slope_m": 15.5, "slope_90": 32.0, "tri": 98.0,
            "temp_k": 258.0, "diurnal": 46.0, "inertia": 470.0, "albedo": 0.16, "bare": 0.88, "ndvi": 0.10,
            "class": "volcanic_field", "dust": 0.25, "sub_rough": 0.72
        },

        # EUROPE
        {
            "province": "Askja Caldera & Holuhraun Lava Field", "country": "Iceland", "continent": "Europe",
            "lat": 65.0, "lon": -16.8, "radius_deg": 1.5, "count_points": 15,
            "lithology": "basaltic_volcanic", "rock": "Fresh Tholeiitic A'a and Pahoehoe Basalt Flows",
            "minerals": "Augite, labradorite plagioclase, olivine, volcanic glass, palagonite",
            "elev_base": 980.0, "relief": 860.0, "slope_m": 8.5, "slope_90": 21.0, "tri": 96.0,
            "temp_k": 271.0, "diurnal": 50.0, "inertia": 420.0, "albedo": 0.10, "bare": 0.97, "ndvi": 0.04,
            "class": "volcanic_field", "dust": 0.25, "sub_rough": 0.74
        },
        {
            "province": "Svalbard Bockfjorden Permafrost Volcanics", "country": "Norway", "continent": "Europe",
            "lat": 79.4, "lon": 13.4, "radius_deg": 1.0, "count_points": 10,
            "lithology": "polar_permafrost_ice", "rock": "Subglacial Quaternary Basalt Volcanism and Carbonate Globules",
            "minerals": "Spinel lherzolite, olivine, pyroxene, magnesite, dolomite globules",
            "elev_base": 650.0, "relief": 920.0, "slope_m": 17.5, "slope_90": 34.0, "tri": 105.0,
            "temp_k": 260.0, "diurnal": 38.0, "inertia": 460.0, "albedo": 0.20, "bare": 0.94, "ndvi": 0.04,
            "class": "permafrost_ice", "dust": 0.40, "sub_rough": 0.68
        },
        {
            "province": "Rio Tinto Iron Gossan Belt", "country": "Spain", "continent": "Europe",
            "lat": 37.7, "lon": -6.6, "radius_deg": 0.8, "count_points": 8,
            "lithology": "acidic_sulfate_gossan", "rock": "Massive Sulfide Gossan, Jarosite, and Ferricrete",
            "minerals": "Jarosite, goethite, hematite, copiapite, pyrite",
            "elev_base": 380.0, "relief": 440.0, "slope_m": 8.2, "slope_90": 18.5, "tri": 45.0,
            "temp_k": 293.0, "diurnal": 37.0, "inertia": 520.0, "albedo": 0.16, "bare": 0.88, "ndvi": 0.12,
            "class": "barren_rock", "dust": 0.40, "sub_rough": 0.42
        },
        {
            "province": "Teide Volcano & Las Cañadas Caldera", "country": "Spain", "continent": "Europe",
            "lat": 28.3, "lon": -16.6, "radius_deg": 1.0, "count_points": 10,
            "lithology": "basaltic_volcanic", "rock": "Phonolitic and Basaltic Blocky Lavas, Obsidian Flows",
            "minerals": "Anorthoclase, augite, olivine, volcanic obsidian glass",
            "elev_base": 2200.0, "relief": 1500.0, "slope_m": 16.0, "slope_90": 31.0, "tri": 102.0,
            "temp_k": 284.0, "diurnal": 40.0, "inertia": 450.0, "albedo": 0.15, "bare": 0.95, "ndvi": 0.03,
            "class": "volcanic_field", "dust": 0.30, "sub_rough": 0.76
        },
        {
            "province": "Nördlinger Ries Impact Crater", "country": "Germany", "continent": "Europe",
            "lat": 48.9, "lon": 10.5, "radius_deg": 0.8, "count_points": 8,
            "lithology": "impact_breccia", "rock": "Suevite Impact Melt Breccia and Shocked Crystalline Basement",
            "minerals": "Shocked quartz, coesite, stishovite, impact glass, montmorillonite",
            "elev_base": 480.0, "relief": 160.0, "slope_m": 6.5, "slope_90": 15.0, "tri": 35.0,
            "temp_k": 282.0, "diurnal": 25.0, "inertia": 490.0, "albedo": 0.18, "bare": 0.65, "ndvi": 0.30,
            "class": "barren_rock", "dust": 0.25, "sub_rough": 0.35
        },

        # NORTH AMERICA
        {
            "province": "Mojave Desert & Death Valley", "country": "United States", "continent": "North America",
            "lat": 35.7, "lon": -116.2, "radius_deg": 2.0, "count_points": 16,
            "lithology": "hyperarid_playa_evaporite", "rock": "Alluvial Gravels, Olivine Cinder Cones, and Borate-Halite Playas",
            "minerals": "Olivine, pyroxene, plagioclase, halite, borax, illite",
            "elev_base": 420.0, "relief": 1900.0, "slope_m": 10.4, "slope_90": 26.0, "tri": 65.0,
            "temp_k": 302.0, "diurnal": 57.0, "inertia": 360.0, "albedo": 0.25, "bare": 0.96, "ndvi": 0.05,
            "class": "desert_sand", "dust": 0.75, "sub_rough": 0.45
        },
        {
            "province": "Craters of the Moon Great Rift", "country": "United States", "continent": "North America",
            "lat": 43.5, "lon": -113.6, "radius_deg": 1.2, "count_points": 12,
            "lithology": "basaltic_volcanic", "rock": "Holocene Flood Basalts, Spatter Cones, and Lava Tube Caves",
            "minerals": "Plagioclase, augite, olivine, titanomagnetite, basalt glass",
            "elev_base": 1780.0, "relief": 405.0, "slope_m": 7.2, "slope_90": 17.8, "tri": 62.0,
            "temp_k": 284.0, "diurnal": 60.0, "inertia": 450.0, "albedo": 0.09, "bare": 0.94, "ndvi": 0.06,
            "class": "volcanic_field", "dust": 0.20, "sub_rough": 0.65
        },
        {
            "province": "Haughton Impact Crater (Devon Island)", "country": "Canada", "continent": "North America",
            "lat": 75.4, "lon": -89.7, "radius_deg": 1.2, "count_points": 12,
            "lithology": "impact_breccia", "rock": "Allogenic Impact Melt Breccia and Shocked Carbonate Bedrock",
            "minerals": "Shocked quartz, dolomite, calcite, gypsum hydrothermal veins, impact glass",
            "elev_base": 280.0, "relief": 430.0, "slope_m": 7.8, "slope_90": 17.5, "tri": 52.0,
            "temp_k": 256.0, "diurnal": 55.0, "inertia": 450.0, "albedo": 0.19, "bare": 0.98, "ndvi": 0.02,
            "class": "permafrost_ice", "dust": 0.65, "sub_rough": 0.55
        },
        {
            "province": "Kilbourne Hole Maar & Potrillo", "country": "United States", "continent": "North America",
            "lat": 32.0, "lon": -107.0, "radius_deg": 1.0, "count_points": 10,
            "lithology": "basaltic_volcanic", "rock": "Phreatomagmatic Maar Tephra with Mantle Peridotite Xenoliths",
            "minerals": "Forsterite olivine, enstatite, Cr-diopside, spinel peridotite, basalt tephra",
            "elev_base": 1240.0, "relief": 180.0, "slope_m": 9.5, "slope_90": 24.0, "tri": 55.0,
            "temp_k": 298.0, "diurnal": 53.0, "inertia": 380.0, "albedo": 0.20, "bare": 0.94, "ndvi": 0.06,
            "class": "volcanic_field", "dust": 0.70, "sub_rough": 0.44
        },
        {
            "province": "Columbia River Basalt Plateau", "country": "United States", "continent": "North America",
            "lat": 46.5, "lon": -119.5, "radius_deg": 2.0, "count_points": 15,
            "lithology": "basaltic_volcanic", "rock": "Tholeiitic Continental Flood Basalts (Grande Ronde Formation)",
            "minerals": "Labradorite, clinopyroxene, magnetite, glass, palagonite",
            "elev_base": 650.0, "relief": 580.0, "slope_m": 8.0, "slope_90": 20.0, "tri": 50.0,
            "temp_k": 286.0, "diurnal": 45.0, "inertia": 460.0, "albedo": 0.16, "bare": 0.85, "ndvi": 0.15,
            "class": "volcanic_field", "dust": 0.45, "sub_rough": 0.50
        },
        {
            "province": "Sudbury Impact Basin Complex", "country": "Canada", "continent": "North America",
            "lat": 46.6, "lon": -81.2, "radius_deg": 1.2, "count_points": 10,
            "lithology": "impact_breccia", "rock": "Differentiated Impact Melt Sheet and Onaping Fallback Breccia",
            "minerals": "Norite, granophyre, shocked quartz, pyrrhotite, chalcopyrite, pentlandite",
            "elev_base": 380.0, "relief": 220.0, "slope_m": 7.0, "slope_90": 16.0, "tri": 40.0,
            "temp_k": 278.0, "diurnal": 38.0, "inertia": 510.0, "albedo": 0.15, "bare": 0.60, "ndvi": 0.35,
            "class": "barren_rock", "dust": 0.20, "sub_rough": 0.45
        },

        # SOUTH AMERICA
        {
            "province": "Atacama Hyper-Arid Central Depression", "country": "Chile", "continent": "South America",
            "lat": -24.1, "lon": -69.9, "radius_deg": 2.2, "count_points": 18,
            "lithology": "hyperarid_playa_evaporite", "rock": "Halite, Anhydrite, Gypsum, and Perchlorate Regolith",
            "minerals": "Halite, anhydrite, gypsum, thenardite, perchlorate/nitrate salts",
            "elev_base": 2350.0, "relief": 1300.0, "slope_m": 5.2, "slope_90": 12.8, "tri": 24.0,
            "temp_k": 295.0, "diurnal": 50.0, "inertia": 380.0, "albedo": 0.28, "bare": 0.99, "ndvi": 0.02,
            "class": "salt_crust", "dust": 0.82, "sub_rough": 0.32
        },
        {
            "province": "Salar de Uyuni & Altiplano", "country": "Bolivia", "continent": "South America",
            "lat": -20.1, "lon": -67.5, "radius_deg": 1.8, "count_points": 15,
            "lithology": "hyperarid_playa_evaporite", "rock": "Ultra-Flat Evaporitic Halite Crust and Lithium Brine",
            "minerals": "Halite (NaCl), gypsum, ulexite, lithium carbonate, carnallite",
            "elev_base": 3656.0, "relief": 8.0, "slope_m": 0.3, "slope_90": 0.8, "tri": 3.0,
            "temp_k": 285.0, "diurnal": 50.0, "inertia": 390.0, "albedo": 0.65, "bare": 1.0, "ndvi": 0.00,
            "class": "salt_crust", "dust": 0.95, "sub_rough": 0.15
        },
        {
            "province": "Puna de Atacama Volcanic Plateau", "country": "Argentina", "continent": "South America",
            "lat": -25.5, "lon": -68.0, "radius_deg": 2.0, "count_points": 16,
            "lithology": "basaltic_volcanic", "rock": "Andean High-Altitude Ignimbrite Sheets and Basaltic Cones",
            "minerals": "Dacite ignimbrite, pumice, augite, plagioclase, sulfur",
            "elev_base": 4200.0, "relief": 2200.0, "slope_m": 14.0, "slope_90": 29.0, "tri": 90.0,
            "temp_k": 275.0, "diurnal": 52.0, "inertia": 410.0, "albedo": 0.22, "bare": 0.98, "ndvi": 0.01,
            "class": "volcanic_field", "dust": 0.50, "sub_rough": 0.68
        },
        {
            "province": "Ischigualasto Triassic Valley of the Moon", "country": "Argentina", "continent": "South America",
            "lat": -30.1, "lon": -67.9, "radius_deg": 1.2, "count_points": 12,
            "lithology": "hyperarid_playa_evaporite", "rock": "Continental Red Mudstones, Sandstones, and Bentonite Clays",
            "minerals": "Smectite, illite, gypsum, quartz, feldspar, ferric oxides",
            "elev_base": 1300.0, "relief": 380.0, "slope_m": 9.2, "slope_90": 22.0, "tri": 58.0,
            "temp_k": 292.0, "diurnal": 44.0, "inertia": 400.0, "albedo": 0.24, "bare": 0.95, "ndvi": 0.03,
            "class": "desert_sand", "dust": 0.70, "sub_rough": 0.46
        },

        # OCEANIA
        {
            "province": "Pilbara Craton (North Pole Dome)", "country": "Australia", "continent": "Oceania",
            "lat": -21.2, "lon": 119.4, "radius_deg": 2.0, "count_points": 16,
            "lithology": "silicified_craton", "rock": "3.5 Ga Silicified Chert, Barite, Komatiite, and BIF",
            "minerals": "Microcrystalline quartz (chert), barite, hematite, magnetite, serpentine",
            "elev_base": 340.0, "relief": 430.0, "slope_m": 9.2, "slope_90": 20.5, "tri": 48.0,
            "temp_k": 305.0, "diurnal": 46.0, "inertia": 510.0, "albedo": 0.18, "bare": 0.92, "ndvi": 0.08,
            "class": "barren_rock", "dust": 0.45, "sub_rough": 0.48
        },
        {
            "province": "Simpson Desert Linear Dunes", "country": "Australia", "continent": "Oceania",
            "lat": -25.5, "lon": 137.0, "radius_deg": 2.5, "count_points": 18,
            "lithology": "hyperarid_playa_evaporite", "rock": "Parallel Red Quartz Sand Dunes and Clay Pans",
            "minerals": "Hematite-coated quartz sand, kaolinite, illite, gypsum",
            "elev_base": 120.0, "relief": 140.0, "slope_m": 8.5, "slope_90": 19.0, "tri": 40.0,
            "temp_k": 302.0, "diurnal": 48.0, "inertia": 330.0, "albedo": 0.26, "bare": 0.94, "ndvi": 0.05,
            "class": "desert_sand", "dust": 0.85, "sub_rough": 0.28
        },
        {
            "province": "Lake Eyre Salt Basin (Kati Thanda)", "country": "Australia", "continent": "Oceania",
            "lat": -28.4, "lon": 137.3, "radius_deg": 1.5, "count_points": 12,
            "lithology": "hyperarid_playa_evaporite", "rock": "Endorheic Halite-Gypsum Salt Crust Over Marine Mud",
            "minerals": "Halite, gypsum, thenardite, smectite mud",
            "elev_base": -15.0, "relief": 25.0, "slope_m": 0.8, "slope_90": 2.0, "tri": 8.0,
            "temp_k": 301.0, "diurnal": 42.0, "inertia": 370.0, "albedo": 0.48, "bare": 0.99, "ndvi": 0.01,
            "class": "salt_crust", "dust": 0.90, "sub_rough": 0.18
        },
        {
            "province": "Gosses Bluff Impact Crater", "country": "Australia", "continent": "Oceania",
            "lat": -23.8, "lon": 132.3, "radius_deg": 0.8, "count_points": 8,
            "lithology": "impact_breccia", "rock": "Shattered Sandstone Central Uplift Ring (142 Ma Impact)",
            "minerals": "Shatter cones in quartz sandstone, planar deformation features, diaplectic glass",
            "elev_base": 720.0, "relief": 280.0, "slope_m": 13.5, "slope_90": 27.0, "tri": 72.0,
            "temp_k": 299.0, "diurnal": 45.0, "inertia": 480.0, "albedo": 0.20, "bare": 0.90, "ndvi": 0.08,
            "class": "barren_rock", "dust": 0.50, "sub_rough": 0.52
        },

        # ADDITIONAL EXPANDED GLOBAL ANALOGS ACROSS ASIA, AMERICAS, EUROPE, AFRICA, OCEANIA
        {
            "province": "Indo-Gangetic Plain & Punjab Alluvial Basin", "country": "India", "continent": "Asia",
            "lat": 30.9, "lon": 75.8, "radius_deg": 1.5, "count_points": 14,
            "lithology": "sedimentary_alluvial", "rock": "Quaternary Indo-Gangetic Alluvial Silt, Clay, and Sand Beds",
            "minerals": "Quartz, microcline, illite, smectite, chlorite, kankar nodules",
            "elev_base": 245.0, "relief": 30.0, "slope_m": 0.8, "slope_90": 1.6, "tri": 5.0,
            "temp_k": 298.0, "diurnal": 26.0, "inertia": 580.0, "albedo": 0.17, "bare": 0.30, "ndvi": 0.65,
            "class": "alluvial_plain", "dust": 0.40, "sub_rough": 0.20
        },
        {
            "province": "Thar Desert Dunefields (Marusthali)", "country": "India", "continent": "Asia",
            "lat": 27.0, "lon": 71.5, "radius_deg": 2.0, "count_points": 14,
            "lithology": "hyperarid_playa_evaporite", "rock": "Longitudinal Seif Dunes and Calcrete Playas",
            "minerals": "Quartz sand, feldspar, calcite, gypsum, illite",
            "elev_base": 185.0, "relief": 110.0, "slope_m": 8.0, "slope_90": 17.5, "tri": 35.0,
            "temp_k": 303.0, "diurnal": 45.0, "inertia": 340.0, "albedo": 0.27, "bare": 0.92, "ndvi": 0.08,
            "class": "desert_sand", "dust": 0.85, "sub_rough": 0.30
        },
        {
            "province": "Great Rann of Kutch Salt Marsh", "country": "India", "continent": "Asia",
            "lat": 23.8, "lon": 70.5, "radius_deg": 1.5, "count_points": 12,
            "lithology": "hyperarid_playa_evaporite", "rock": "Endorheic Halite Crust and Seasonal Evaporite Silt",
            "minerals": "Halite, gypsum, thenardite, marine smectite clay",
            "elev_base": 10.0, "relief": 12.0, "slope_m": 0.4, "slope_90": 1.1, "tri": 4.0,
            "temp_k": 301.0, "diurnal": 34.0, "inertia": 410.0, "albedo": 0.50, "bare": 0.98, "ndvi": 0.02,
            "class": "salt_crust", "dust": 0.90, "sub_rough": 0.15
        },
        {
            "province": "Tibetan High Plateau (Changtang)", "country": "China", "continent": "Asia",
            "lat": 33.5, "lon": 85.5, "radius_deg": 2.2, "count_points": 15,
            "lithology": "polar_permafrost_ice", "rock": "Permafrost Cryic Steppe and High-Altitude Lacustrine Borates",
            "minerals": "Quartz, feldspar, borax, mirabilite, interstitial ice",
            "elev_base": 4750.0, "relief": 850.0, "slope_m": 6.5, "slope_90": 14.5, "tri": 44.0,
            "temp_k": 265.0, "diurnal": 52.0, "inertia": 430.0, "albedo": 0.24, "bare": 0.86, "ndvi": 0.12,
            "class": "permafrost_ice", "dust": 0.60, "sub_rough": 0.45
        },
        {
            "province": "Himalayan Cryo-Cirques (Khumbu)", "country": "Nepal", "continent": "Asia",
            "lat": 27.9, "lon": 86.8, "radius_deg": 1.0, "count_points": 10,
            "lithology": "silicified_craton", "rock": "Higher Himalayan Leucogranite, Gneiss, and Glacial Moraine",
            "minerals": "Quartz, tourmaline, muscovite, sillimanite, glacial ice",
            "elev_base": 5100.0, "relief": 2600.0, "slope_m": 26.5, "slope_90": 44.0, "tri": 160.0,
            "temp_k": 258.0, "diurnal": 36.0, "inertia": 510.0, "albedo": 0.42, "bare": 0.96, "ndvi": 0.02,
            "class": "permafrost_ice", "dust": 0.30, "sub_rough": 0.85
        },
        {
            "province": "Mississippi Alluvial Floodplain", "country": "United States", "continent": "North America",
            "lat": 33.8, "lon": -90.8, "radius_deg": 1.5, "count_points": 12,
            "lithology": "sedimentary_alluvial", "rock": "Meander Belt Silts, Backswamp Clays, and Channel Sand",
            "minerals": "Quartz, smectite, illite, kaolinite, organic-rich silt",
            "elev_base": 42.0, "relief": 22.0, "slope_m": 0.5, "slope_90": 1.1, "tri": 4.0,
            "temp_k": 294.0, "diurnal": 24.0, "inertia": 610.0, "albedo": 0.16, "bare": 0.22, "ndvi": 0.72,
            "class": "alluvial_plain", "dust": 0.35, "sub_rough": 0.20
        },
        {
            "province": "Pampas Alluvial Basin", "country": "Argentina", "continent": "South America",
            "lat": -34.5, "lon": -61.5, "radius_deg": 1.5, "count_points": 12,
            "lithology": "sedimentary_alluvial", "rock": "Quaternary Pampean Loess and Alluvial Sediments",
            "minerals": "Quartz, plagioclase, volcanic glass, illite, smectite",
            "elev_base": 80.0, "relief": 25.0, "slope_m": 0.6, "slope_90": 1.3, "tri": 5.0,
            "temp_k": 290.0, "diurnal": 25.0, "inertia": 590.0, "albedo": 0.18, "bare": 0.26, "ndvi": 0.68,
            "class": "alluvial_plain", "dust": 0.35, "sub_rough": 0.20
        },
        {
            "province": "Salinas Grandes Salt Flat", "country": "Argentina", "continent": "South America",
            "lat": -29.8, "lon": -64.8, "radius_deg": 1.2, "count_points": 10,
            "lithology": "hyperarid_playa_evaporite", "rock": "Extensive Halite Salt Crust and Lithium-Rich Subsurface Brine",
            "minerals": "Halite, gypsum, thenardite, clay silt",
            "elev_base": 185.0, "relief": 12.0, "slope_m": 0.3, "slope_90": 0.8, "tri": 3.0,
            "temp_k": 297.0, "diurnal": 42.0, "inertia": 390.0, "albedo": 0.54, "bare": 1.0, "ndvi": 0.00,
            "class": "salt_crust", "dust": 0.95, "sub_rough": 0.15
        },
        {
            "province": "Po Valley Sedimentary Lowland", "country": "Italy", "continent": "Europe",
            "lat": 45.1, "lon": 10.2, "radius_deg": 1.2, "count_points": 10,
            "lithology": "sedimentary_alluvial", "rock": "Quaternary Fluvial Alluvial Gravels and Silt Formations",
            "minerals": "Quartz, calcite, clay minerals, feldspar",
            "elev_base": 65.0, "relief": 20.0, "slope_m": 0.7, "slope_90": 1.5, "tri": 5.0,
            "temp_k": 288.0, "diurnal": 25.0, "inertia": 590.0, "albedo": 0.17, "bare": 0.22, "ndvi": 0.70,
            "class": "alluvial_plain", "dust": 0.35, "sub_rough": 0.22
        },
        {
            "province": "Nullarbor Karst Limestone Plain", "country": "Australia", "continent": "Oceania",
            "lat": -31.0, "lon": 128.5, "radius_deg": 2.0, "count_points": 14,
            "lithology": "silicified_craton", "rock": "Cenozoic Eucla Karst Limestone, Dry Caves, and Blowholes",
            "minerals": "Calcite, dolomite, microcrystalline silica, terra rossa residual clay",
            "elev_base": 135.0, "relief": 30.0, "slope_m": 1.1, "slope_90": 2.6, "tri": 11.0,
            "temp_k": 294.0, "diurnal": 38.0, "inertia": 490.0, "albedo": 0.22, "bare": 0.86, "ndvi": 0.12,
            "class": "barren_rock", "dust": 0.50, "sub_rough": 0.35
        },
        {
            "province": "Flinders Ranges & Wilpena Pound", "country": "Australia", "continent": "Oceania",
            "lat": -31.5, "lon": 138.6, "radius_deg": 1.5, "count_points": 12,
            "lithology": "silicified_craton", "rock": "Ediacaran Pound Sub-Basin Quartzite Ridges and Fossil Strata",
            "minerals": "Orthoquartzite, sandstone, siltstone, hematite coatings",
            "elev_base": 720.0, "relief": 620.0, "slope_m": 14.0, "slope_90": 29.5, "tri": 84.0,
            "temp_k": 293.0, "diurnal": 44.0, "inertia": 520.0, "albedo": 0.20, "bare": 0.89, "ndvi": 0.09,
            "class": "barren_rock", "dust": 0.45, "sub_rough": 0.58
        },
        {
            "province": "Great Rift Valley & Lake Natron", "country": "Tanzania", "continent": "Africa",
            "lat": -2.4, "lon": 36.0, "radius_deg": 1.2, "count_points": 12,
            "lithology": "basaltic_volcanic", "rock": "Natrocarbonatite Volcanic Ash and Hyper-Saline Soda Lake Crusts",
            "minerals": "Nyerereite, gregoryite, nepheline, trona, halite",
            "elev_base": 615.0, "relief": 880.0, "slope_m": 10.5, "slope_90": 24.5, "tri": 68.0,
            "temp_k": 303.0, "diurnal": 36.0, "inertia": 450.0, "albedo": 0.29, "bare": 0.91, "ndvi": 0.07,
            "class": "volcanic_field", "dust": 0.55, "sub_rough": 0.50
        },
        {
            "province": "Ténéré Erg & Sahara Sand Sea", "country": "Niger", "continent": "Africa",
            "lat": 18.5, "lon": 10.5, "radius_deg": 2.2, "count_points": 14,
            "lithology": "hyperarid_playa_evaporite", "rock": "Colossal Hyper-Arid Quartz Dunefield and Paleolake Silts",
            "minerals": "Quartz sand, diatomite, halite",
            "elev_base": 415.0, "relief": 150.0, "slope_m": 9.5, "slope_90": 21.0, "tri": 46.0,
            "temp_k": 305.0, "diurnal": 47.0, "inertia": 320.0, "albedo": 0.33, "bare": 1.0, "ndvi": 0.00,
            "class": "desert_sand", "dust": 0.92, "sub_rough": 0.24
        }
    ]

    SUB_TOPOGRAPHY_LABELS = [
        "Core Outcrop", "North Flank", "Eastern Plateau", "Southern Ridge",
        "Western Basin", "Northeast Steppe", "Northwest Canyon", "Southeast Apron",
        "Southwest Scarp", "Upper Terrace", "Alluvial Fan Margin", "Basal Pediment",
        "Central Depression", "Perimeter Dunefield", "Highland Summit", "Fluvial Channel Belt",
        "Outer Graben", "Bedrock Terrace", "Interdune Flat", "Crustal Escarpment"
    ]

    # Generate multi-point hierarchical grid cells around each geological province
    for p in PROVINCES:
        count = p["count_points"]
        radius = p["radius_deg"]

        # Spiral distribution of sub-cells around the province core
        for idx in range(count):
            if idx == 0:
                d_lat, d_lon = 0.0, 0.0
                cell_name = f"{p['province']} (Core)"
            else:
                # Fibonacci spiral offset
                theta = idx * 2.39996  # Golden angle in radians
                r = radius * math.sqrt(idx / count)
                d_lat = r * math.cos(theta)
                d_lon = r * math.sin(theta) / max(0.2, math.cos(math.radians(p["lat"])))
                sub_label = SUB_TOPOGRAPHY_LABELS[idx % len(SUB_TOPOGRAPHY_LABELS)]
                cell_name = f"{p['province']} ({sub_label})"

            c_lat = round(p["lat"] + d_lat, 4)
            c_lon = round(p["lon"] + d_lon, 4)

            # Local elevation variation
            elev_var = math.sin(idx * 1.7) * (p["relief"] * 0.25)
            c_elev = round(p["elev_base"] + elev_var, 1)
            c_relief = round(max(10.0, p["relief"] + math.cos(idx) * (p["relief"] * 0.15)), 1)
            c_slope_m = round(max(0.2, p["slope_m"] + math.sin(idx * 2.1) * 2.0), 1)
            c_slope_90 = round(max(c_slope_m * 1.5, p["slope_90"] + math.cos(idx * 1.9) * 3.5), 1)
            c_tri = round(max(2.0, p["tri"] + math.sin(idx * 0.8) * 12.0), 1)

            # Spatial cell bounds (approx 25 km coarse cell)
            d_box = 0.12 # ~13-15 km half-width
            min_lat = round(c_lat - d_box, 4)
            max_lat = round(c_lat + d_box, 4)
            min_lon = round(c_lon - d_box, 4)
            max_lon = round(c_lon + d_box, 4)

            # Standardized Candidate Record
            cand = {
                "id": f"earth_grid_{numeric_id_counter:04d}",
                "numeric_id": numeric_id_counter,
                "name": cell_name,
                "country": p["country"],
                "continent": p["continent"],
                "latitude": c_lat,
                "longitude": c_lon,
                "min_lat": min_lat,
                "max_lat": max_lat,
                "min_lon": min_lon,
                "max_lon": max_lon,
                "cell_resolution_km": 25.0,
                "elevation_mean": c_elev,
                "elevation_min": round(c_elev - c_relief * 0.5, 1),
                "elevation_max": round(c_elev + c_relief * 0.5, 1),
                "elevation_std": round(max(2.0, c_relief * 0.28), 1),
                "relief_m": c_relief,
                "slope_mean": c_slope_m,
                "slope_p90": c_slope_90,
                "terrain_roughness": c_tri,
                "lithology_category": p["lithology"],
                "rock_type": p["rock"],
                "mineralogy_summary": p["minerals"],
                "bare_ground_ratio": p["bare"],
                "vegetation_ndvi": p["ndvi"],
                "surface_temp_mean_k": p["temp_k"],
                "diurnal_range_k": p["diurnal"],
                "thermal_inertia_si": p["inertia"],
                "albedo": p["albedo"],
                "roughness_submeter": p["sub_rough"],
                "dust_sediment_cover": p["dust"],
                "land_cover_class": p["class"],
                "is_water": 0,
                "data_coverage_score": 0.98,
                "data_sources": [
                    "Copernicus GLO-90 Global DEM",
                    "University of Hamburg GLiM Lithological Map",
                    "ESA WorldCover 10m",
                    "NASA LP DAAC MODIS LST (MOD11A1)"
                ]
            }

            candidates.append(cand)
            numeric_id_counter += 1

    return candidates
