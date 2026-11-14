# TERRATWIN (NASA Space Apps Challenge)
### AI-Powered Earth Analog Discovery Platform for Lunar and Martian Exploration

**TerraTwin** is a planetary analog discovery engine that identifies geographical locations on Earth whose measurable geological, topographical, and environmental characteristics resemble selected exploration regions on the Moon or Mars.

The platform answers the core question:
> *"Which locations on Earth most closely resemble a selected region of the Moon or Mars in terms of measurable surface and environmental characteristics, and why?"*

---

## 🚀 Key Features

1. **Interactive 3D Planetary Exploration**:
   - **Earth Globe**: Rendered via CesiumJS with global satellite imagery, terrain elevation, candidate analog pinpoints, and selected radius boundary overlays.
   - **Moon & Mars Globes**: Rendered via Three.js with NASA LROC, Clementine, and Viking global texture maps, atmospheric glow shaders, raycasting coordinate picking, and predefined exploration hotspots.
2. **Raycasting Surface Coordinate Selection**:
   - Click anywhere on the 3D Moon or Mars sphere to calculate the exact latitude and longitude via raycasting.
   - Dynamically adjust the exploration radius (10 km to 250 km).
3. **Scientific Geospatial Feature Extraction**:
   - Quantitative topographic metrics: Mean slope, peak slope (90th percentile), Terrain Ruggedness Index (TRI), elevation standard deviation, and topographic relief.
   - Petrological and lithological classification: Basaltic volcanics, cryogenic polar permafrost, hyperarid playa evaporites, acid sulfate gossans, and impact breccias.
   - Thermal observations: Diurnal temperature amplitude ($\Delta T$) and thermal inertia.
   - Surface optical properties: Albedo, bare ground fraction, and sub-meter rock obstacle density.
4. **Multidimensional Scientific Similarity Engine**:
   - Robust Z-score feature scaling using empirical population standard deviations across planetary bodies.
   - Weighted Euclidean distance metric:
     $$D(A, B) = \sqrt{\sum w_i \cdot \left(\frac{A_i - B_i}{\sigma_i}\right)^2}$$
   - Exponential similarity mapping: $S = 100 \cdot \exp(-D / \tau)$.
   - Domain-specific petrological compatibility matrix modeling geochemical affinities.
   - Configurable scientific weighting between Topography, Geology, Thermal, and Surface attributes.
5. **3D Side-by-Side Comparison Dashboard**:
   - Dual-globe synchronized visualization displaying the extraterrestrial site and terrestrial analog side by side.
   - SVG Multidimensional Radar Chart comparing Topography, Geology, Thermal, Surface, and Roughness congruence.
   - Topographic cross-section elevation profile charts comparing regional morphological relief slices.
   - Full parameter comparison matrix with physical measurement units.
6. **AI Scientific Research Assistant**:
   - Grounded mission suitability assessments:
     - **Rover Mobility & Terramechanics**: Slope hazards, wheel slip risks, rock boulder obstacle density.
     - **Robotic Drilling & Regolith Sampling (ISRU)**: Rotary-percussive penetration, bit abrasion, sample caching.
     - **Optical & Spectrometric Sensor Calibration**: Radiometer and hyperspectral ground-truthing.
   - Explicit scientific disclaimers regarding non-reproducible parameters (partial gravity, vacuum, cosmic radiation).
   - Interactive Q&A chat for mission researchers.
7. **Automated Publication-Grade PDF Report Generation**:
   - One-click compilation of comprehensive PDF research reports powered by ReportLab and Pillow.
   - Formatted with NASA Space Apps academic styling, metadata tables, radar similarity charts, parameter comparison tables, mission suitability recommendations, and data citations.

---

## 🛰️ Ingested Planetary Datasets

| Dataset | Body | Type | Resolution | Citation / Provenance |
| :--- | :--- | :--- | :--- | :--- |
| **NASA LRO LOLA** | Moon | Topography & DEM | 64-128 ppd (~15-30m) | Smith et al., Space Sci. Rev. (2010) |
| **NASA LRO Diviner** | Moon | Thermal & Rock Abundance | 1 km grid | Paige et al., Space Sci. Rev. (2010) |
| **NASA MGS MOLA** | Mars | Topography & DEM | 128 ppd (MEGDR) | Zuber et al., J. Geophys. Res. (1992) |
| **NASA Odyssey THEMIS** | Mars | Thermal IR & Inertia | 100 m / 1 km | Christensen et al., Space Sci. Rev. (2004) |
| **USGS SRTM** | Earth | Digital Elevation Model | 1 arc-sec (30m) | Farr et al., Rev. Geophys. (2007) |
| **NASA MODIS MOD11A1** | Earth | Land Surface Temp | 1 km daily grid | Wan et al., Remote Sens. Environ. (2014) |
| **University of Hamburg GLiM** | Earth | Global Lithological Map | Polygonal global units | Hartmann & Moosdorf, G-cubed (2012) |

---

## 🛠️ Technology Stack

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons, Three.js, CesiumJS.
- **Backend**: Python 3.13, FastAPI, Pydantic, NumPy, SciPy, Scikit-learn, ReportLab, Pillow, Uvicorn.
- **Data & Testing**: Python `unittest`, automated verification suite for scientific feature extraction and similarity ranking.

---

## 💻 Setup and Execution Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run automated scientific verification tests
python -m unittest discover backend/tests

# Start the FastAPI server
python -m uvicorn backend.app.main:app --port 8000 --reload
```
API documentation will be accessible at: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
Open `http://localhost:5173` in your browser.

### 3. Integrated Production Mode (Single Server)
```bash
# Build frontend distribution
cd frontend && npm run build && cd ..

# Launch FastAPI (automatically serves frontend and API simultaneously)
python -m uvicorn backend.app.main:app --port 8000
```
Open `http://localhost:8000` to access the full integrated application.

---

## 🔬 Scientific Limitations & Disclaimers

TerraTwin distinguishes between an **analog environment** and an **exact replica**:
1. **Reduced Gravity**: Earth surface gravity (9.81 m/s²) is substantially higher than the Moon (1.62 m/s²; 16.5%) and Mars (3.72 m/s²; 38%). Rover suspension travel, slip angles, and ejecta dynamics must be adjusted using gravity offloading counterweights.
2. **Atmospheric Density**: Earth's ambient pressure (~1013 hPa) cannot replicate the hard vacuum of the Moon (<10⁻¹⁰ hPa) or the thin CO₂ atmosphere of Mars (6.4 hPa). Volatile sublimation and thruster plume interactions require thermal-vacuum chambers (TVAC).
3. **Cosmic Radiation**: Earth's ~45 µT geomagnetic dipole and thick atmospheric column shield against galactic cosmic rays (GCR) and solar energetic particles (SEP).
