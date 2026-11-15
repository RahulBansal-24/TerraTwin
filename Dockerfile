# ==============================================================================
# Multi-Stage Dockerfile for TerraTwin (NASA Space Apps Challenge)
# Builds Vite React frontend and serves via FastAPI Python backend
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build React Frontend SPA
# ------------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Production Python Backend & SPA Static Server
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install runtime dependencies for scientific computing (NumPy, SciPy, Pillow, ReportLab)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend codebase
COPY backend/ ./backend/

# Copy built frontend distribution from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port (default 8000, compatible with Cloud Run, Railway, Render)
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
