"""
TerraTwin Main FastAPI Application.
NASA Space Apps Challenge: AI-Powered Earth Analog Discovery Platform.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from .routes.api import router as api_router

app = FastAPI(
    title="TerraTwin Scientific API",
    description="AI-Powered Planetary Analog Discovery for Lunar and Martian Exploration",
    version="1.0.0"
)

# CORS setup for local and deployment environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount frontend production build if available
frontend_dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_dir, "assets")), name="assets")
    if os.path.exists(os.path.join(frontend_dist_dir, "textures")):
        app.mount("/textures", StaticFiles(directory=os.path.join(frontend_dist_dir, "textures")), name="textures")
    if os.path.exists(os.path.join(frontend_dist_dir, "cesium")):
        app.mount("/cesium", StaticFiles(directory=os.path.join(frontend_dist_dir, "cesium")), name="cesium")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dist_dir, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist_dir, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "project": "TerraTwin",
            "description": "AI-Powered Earth Analog Discovery Platform for Lunar and Martian Exploration",
            "status": "online",
            "version": "1.0.0",
            "docs_url": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
