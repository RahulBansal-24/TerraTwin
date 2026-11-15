import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { ExplorationRegion } from '../types';
import { RotateCw, Compass, ZoomIn, ZoomOut, Eye, Layers } from 'lucide-react';

interface ThreeGlobeProps {
  planet: 'earth' | 'moon' | 'mars';
  selectedCoords?: { lat: number; lon: number } | null;
  radiusKm?: number;
  featuredRegions?: ExplorationRegion[];
  onSelectCoords?: (lat: number, lon: number) => void;
  onSelectRegion?: (region: ExplorationRegion) => void;
  height?: string;
  className?: string;
  showControls?: boolean;
  defaultAutoRotate?: boolean;
}

export const ThreeGlobe: React.FC<ThreeGlobeProps> = ({
  planet,
  selectedCoords,
  radiusKm = 50,
  featuredRegions = [],
  onSelectCoords,
  onSelectRegion,
  height = '600px',
  className = '',
  showControls = true,
  defaultAutoRotate = true,
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [autoRotate, setAutoRotate] = useState<boolean>(defaultAutoRotate);
  const autoRotateRef = useRef<boolean>(defaultAutoRotate);
  const prevCoordsRef = useRef<{ lat: number; lon: number } | null>(null);
  const ignoreNextCenterRef = useRef<boolean>(false);
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);

  // References to keep across renders
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const globeMeshRef = useRef<THREE.Mesh | null>(null);
  const markerGroupRef = useRef<THREE.Group | null>(null);
  const selectionGroupRef = useRef<THREE.Group | null>(null);
  const controlsState = useRef({
    isDragging: false,
    previousMousePosition: { x: 0, y: 0 },
    rotationSpeed: 0.005,
    zoom: 2.4,
  });

  const PLANET_TEXTURES: Record<string, string> = {
    moon: '/textures/moon_map.jpg',
    mars: '/textures/mars_map.jpg',
    earth: '/textures/earth_map.jpg',
  };

  const PLANET_COLORS: Record<string, number> = {
    moon: 0x94a3b8,
    mars: 0xfb923c,
    earth: 0x38bdf8,
  };

  // Convert (lat, lon) to 3D Cartesian coordinates on a sphere of radius R
  const latLonToVector3 = (lat: number, lon: number, radius: number): THREE.Vector3 => {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const z = radius * Math.sin(phi) * Math.sin(theta);
    const y = radius * Math.cos(phi);

    return new THREE.Vector3(x, y, z);
  };

  // Convert 3D intersection vector to (lat, lon)
  const vector3ToLatLon = (vec: THREE.Vector3): { lat: number; lon: number } => {
    const normal = vec.clone().normalize();
    const lat = 90 - (Math.acos(normal.y) * 180 / Math.PI);
    let lon = ((Math.atan2(normal.z, -normal.x) * 180 / Math.PI) - 180);
    while (lon < -180) lon += 360;
    while (lon > 180) lon -= 360;
    return {
      lat: Math.round(lat * 100) / 100,
      lon: Math.round(lon * 100) / 100,
    };
  };

  // Re-orient the 3D globe so any given (lat, lon) is positioned front and center facing the camera
  const orientToCoordinates = (lat: number, lon: number) => {
    if (!globeMeshRef.current) return;
    const qY = new THREE.Quaternion().setFromAxisAngle(
      new THREE.Vector3(0, 1, 0),
      -THREE.MathUtils.degToRad(lon + 90)
    );
    const qX = new THREE.Quaternion().setFromAxisAngle(
      new THREE.Vector3(1, 0, 0),
      THREE.MathUtils.degToRad(lat)
    );
    globeMeshRef.current.quaternion.copy(qX.multiply(qY));
  };

  useEffect(() => {
    if (!mountRef.current) return;
    const container = mountRef.current;
    const width = container.clientWidth;
    const heightPx = container.clientHeight || 500;

    // 1. Scene setup
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // 2. Camera setup
    const camera = new THREE.PerspectiveCamera(45, width / heightPx, 0.1, 1000);
    camera.position.z = controlsState.current.zoom;
    cameraRef.current = camera;

    // 3. Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, heightPx);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // 4. Lighting setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.55);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xffffff, 1.8);
    sunLight.position.set(5, 3, 5);
    scene.add(sunLight);

    const rimLight = new THREE.DirectionalLight(PLANET_COLORS[planet] || 0x38bdf8, 0.6);
    rimLight.position.set(-5, -2, -5);
    scene.add(rimLight);

    // 5. Globe geometry and texture
    const radius = 1.0;
    const geometry = new THREE.SphereGeometry(radius, 64, 64);

    const textureLoader = new THREE.TextureLoader();
    const textureUrl = PLANET_TEXTURES[planet] || PLANET_TEXTURES.mars;
    const texture = textureLoader.load(textureUrl);
    texture.colorSpace = THREE.SRGBColorSpace;

    const material = new THREE.MeshStandardMaterial({
      map: texture,
      roughness: 0.85,
      metalness: 0.1,
    });

    const globeMesh = new THREE.Mesh(geometry, material);
    scene.add(globeMesh);
    globeMeshRef.current = globeMesh;

    if (selectedCoords) {
      orientToCoordinates(selectedCoords.lat, selectedCoords.lon);
      prevCoordsRef.current = { lat: selectedCoords.lat, lon: selectedCoords.lon };
    }

    // Atmosphere glow layer for Mars and Earth
    if (planet === 'mars' || planet === 'earth') {
      const glowGeo = new THREE.SphereGeometry(radius * 1.02, 32, 32);
      const glowMat = new THREE.MeshBasicMaterial({
        color: PLANET_COLORS[planet],
        transparent: true,
        opacity: planet === 'mars' ? 0.15 : 0.22,
        side: THREE.BackSide,
      });
      const glowMesh = new THREE.Mesh(glowGeo, glowMat);
      scene.add(glowMesh);
    }

    // Groups for markers
    const markerGroup = new THREE.Group();
    globeMesh.add(markerGroup);
    markerGroupRef.current = markerGroup;

    const selectionGroup = new THREE.Group();
    globeMesh.add(selectionGroup);
    selectionGroupRef.current = selectionGroup;

    // Starfield background
    const starsGeo = new THREE.BufferGeometry();
    const starCount = 600;
    const starCoords = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i += 3) {
      starCoords[i] = (Math.random() - 0.5) * 50;
      starCoords[i + 1] = (Math.random() - 0.5) * 50;
      starCoords[i + 2] = (Math.random() - 0.5) * 50;
    }
    starsGeo.setAttribute('position', new THREE.BufferAttribute(starCoords, 3));
    const starsMat = new THREE.PointsMaterial({ color: 0x94a3b8, size: 0.08, transparent: true, opacity: 0.5 });
    const starField = new THREE.Points(starsGeo, starsMat);
    scene.add(starField);

    // 6. Interaction Handlers
    let isMouseDown = false;
    let mouseStart = { x: 0, y: 0 };
    let hasMoved = false;

    const onMouseDown = (e: MouseEvent) => {
      isMouseDown = true;
      hasMoved = false;
      mouseStart = { x: e.clientX, y: e.clientY };
      controlsState.current.previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isMouseDown || !globeMeshRef.current) return;
      const deltaX = e.clientX - controlsState.current.previousMousePosition.x;
      const deltaY = e.clientY - controlsState.current.previousMousePosition.y;

      if (Math.abs(deltaX) > 2 || Math.abs(deltaY) > 2) {
        hasMoved = true;
      }

      globeMeshRef.current.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), deltaX * controlsState.current.rotationSpeed);
      globeMeshRef.current.rotateOnWorldAxis(new THREE.Vector3(1, 0, 0), deltaY * controlsState.current.rotationSpeed);

      controlsState.current.previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = (e: MouseEvent) => {
      isMouseDown = false;
      if (!hasMoved && onSelectCoords) {
        // Raycast to find clicked coordinate
        const rect = container.getBoundingClientRect();
        const mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        const mouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1;

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(new THREE.Vector2(mouseX, mouseY), camera);

        if (globeMeshRef.current) {
          const intersects = raycaster.intersectObject(globeMeshRef.current);
          if (intersects.length > 0) {
            // Convert intersection point in globe's local space to lat/lon
            const localPoint = globeMeshRef.current.worldToLocal(intersects[0].point.clone());
            const coords = vector3ToLatLon(localPoint);
            ignoreNextCenterRef.current = true;
            onSelectCoords(coords.lat, coords.lon);
          }
        }
      }
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      const zoomFactor = e.deltaY * 0.0015;
      controlsState.current.zoom = Math.max(1.4, Math.min(4.5, controlsState.current.zoom + zoomFactor));
      if (cameraRef.current) {
        cameraRef.current.position.z = controlsState.current.zoom;
      }
    };

    container.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    container.addEventListener('wheel', onWheel, { passive: false });

    // 7. Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      if (autoRotateRef.current && !isMouseDown && globeMeshRef.current) {
        globeMeshRef.current.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), 0.0012);
      }

      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      if (!container || !renderer || !camera) return;
      const w = container.clientWidth;
      const h = container.clientHeight || 500;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      container.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      container.removeEventListener('wheel', onWheel);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    };
  }, [planet]);

  // Update predefined feature markers
  useEffect(() => {
    if (!markerGroupRef.current) return;
    const group = markerGroupRef.current;

    // Clear previous
    while (group.children.length > 0) {
      group.remove(group.children[0]);
    }

    featuredRegions.forEach((reg) => {
      const pos = latLonToVector3(reg.latitude, reg.longitude, 1.01);

      // Pin base sphere
      const pinGeo = new THREE.SphereGeometry(0.02, 16, 16);
      const pinMat = new THREE.MeshBasicMaterial({
        color: planet === 'mars' ? 0xff4500 : (planet === 'moon' ? 0x38bdf8 : 0x10b981),
      });
      const pinMesh = new THREE.Mesh(pinGeo, pinMat);
      pinMesh.position.copy(pos);

      // Outer pulsing ring
      const ringGeo = new THREE.RingGeometry(0.028, 0.038, 24);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.7,
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.position.copy(pos.clone().multiplyScalar(1.002));
      ringMesh.lookAt(new THREE.Vector3(0, 0, 0));

      pinMesh.add(ringMesh);
      group.add(pinMesh);
    });
  }, [featuredRegions, planet]);

  // Update selected coordinates marker & exploration radius circle
  useEffect(() => {
    if (!selectionGroupRef.current) return;
    const group = selectionGroupRef.current;

    while (group.children.length > 0) {
      group.remove(group.children[0]);
    }

    if (selectedCoords) {
      const pos = latLonToVector3(selectedCoords.lat, selectedCoords.lon, 1.015);

      // Selected coordinate marker
      const markerGeo = new THREE.ConeGeometry(0.025, 0.07, 16);
      markerGeo.rotateX(Math.PI);
      const markerMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
      const markerMesh = new THREE.Mesh(markerGeo, markerMat);
      markerMesh.position.copy(pos.clone().multiplyScalar(1.03));
      markerMesh.lookAt(new THREE.Vector3(0, 0, 0));
      group.add(markerMesh);

      // Exploration radius indicator ring on globe surface
      const planetRadiusKm = planet === 'moon' ? 1737.4 : (planet === 'mars' ? 3389.5 : 6371.0);
      const angularRadiusRad = (radiusKm / planetRadiusKm);
      const ringRadius = Math.sin(angularRadiusRad) * 1.01;

      const circleGeo = new THREE.RingGeometry(Math.max(0.015, ringRadius * 0.95), ringRadius, 48);
      const circleMat = new THREE.MeshBasicMaterial({
        color: 0x38bdf8,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.65,
      });
      const circleMesh = new THREE.Mesh(circleGeo, circleMat);
      circleMesh.position.copy(pos);
      circleMesh.lookAt(new THREE.Vector3(0, 0, 0));
      group.add(circleMesh);

      // Re-orient rotating globe model so that the selected coordinate is facing directly towards the user
      const isNewCoord = !prevCoordsRef.current || 
        prevCoordsRef.current.lat !== selectedCoords.lat || 
        prevCoordsRef.current.lon !== selectedCoords.lon;

      if (isNewCoord && globeMeshRef.current) {
        prevCoordsRef.current = { lat: selectedCoords.lat, lon: selectedCoords.lon };
        if (!ignoreNextCenterRef.current) {
          orientToCoordinates(selectedCoords.lat, selectedCoords.lon);
        }
        ignoreNextCenterRef.current = false;
      }
    }
  }, [selectedCoords, radiusKm, planet]);

  const handleToggleAutoRotate = () => {
    const nextState = !autoRotate;
    setAutoRotate(nextState);
    autoRotateRef.current = nextState;
  };

  const handleResetCamera = () => {
    if (globeMeshRef.current && cameraRef.current) {
      if (selectedCoords) {
        orientToCoordinates(selectedCoords.lat, selectedCoords.lon);
      } else {
        globeMeshRef.current.quaternion.identity();
      }
      controlsState.current.zoom = 2.4;
      cameraRef.current.position.z = 2.4;
    }
  };

  const handleZoom = (delta: number) => {
    if (cameraRef.current) {
      controlsState.current.zoom = Math.max(1.4, Math.min(4.5, controlsState.current.zoom + delta));
      cameraRef.current.position.z = controlsState.current.zoom;
    }
  };

  return (
    <div className={`relative overflow-hidden rounded-xl border border-sky-900/40 bg-[#070a14] ${className}`}>
      {/* 3D Canvas Mount */}
      <div ref={mountRef} style={{ height }} className="w-full cursor-grab active:cursor-grabbing" />

      {/* Surface Coordinate Telemetry Overlay */}
      {selectedCoords && (
        <div className="absolute top-4 left-4 z-10 glass-panel rounded-lg px-3 py-2 text-xs text-sky-200 pointer-events-none">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-sky-400 animate-pulse" />
            <span className="font-mono font-bold tracking-wide">
              {selectedCoords.lat.toFixed(2)}°{selectedCoords.lat >= 0 ? 'N' : 'S'},{' '}
              {selectedCoords.lon.toFixed(2)}°{selectedCoords.lon >= 0 ? 'E' : 'W'}
            </span>
          </div>
          <div className="text-[10px] text-slate-400 mt-0.5">
            Exploration Radius: <span className="text-sky-300 font-semibold">{radiusKm} km</span>
          </div>
        </div>
      )}

      {/* Floating 3D Controls */}
      {showControls && (
        <div className="absolute bottom-4 right-4 z-10 flex flex-col gap-1.5 glass-panel p-1.5 rounded-lg">
          <button
            onClick={handleToggleAutoRotate}
            title={autoRotate ? "Pause Rotation" : "Resume Rotation"}
            className={`p-2 rounded text-xs transition ${autoRotate ? 'bg-sky-500/20 text-sky-300' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <RotateCw size={14} className={autoRotate ? "animate-spin" : ""} />
          </button>
          <button
            onClick={handleResetCamera}
            title="Reset Perspective"
            className="p-2 rounded text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition"
          >
            <Compass size={14} />
          </button>
          <button
            onClick={() => handleZoom(-0.3)}
            title="Zoom In"
            className="p-2 rounded text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition"
          >
            <ZoomIn size={14} />
          </button>
          <button
            onClick={() => handleZoom(0.3)}
            title="Zoom Out"
            className="p-2 rounded text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition"
          >
            <ZoomOut size={14} />
          </button>
        </div>
      )}

      {/* Predefined Features Quick Selector */}
      {featuredRegions.length > 0 && (
        <div className="absolute bottom-4 left-4 z-10 flex items-center gap-1.5 overflow-x-auto max-w-[calc(100%-110px)] pb-1">
          {featuredRegions.map((reg) => (
            <button
              key={reg.id}
              onClick={() => {
                orientToCoordinates(reg.latitude, reg.longitude);
                prevCoordsRef.current = { lat: reg.latitude, lon: reg.longitude };
                if (onSelectRegion) onSelectRegion(reg);
                if (onSelectCoords) onSelectCoords(reg.latitude, reg.longitude);
              }}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-md glass-panel text-slate-300 hover:text-white hover:border-sky-400/60 transition flex items-center gap-1.5 shadow-sm"
            >
              <span className={`w-1.5 h-1.5 rounded-full ${planet === 'mars' ? 'bg-orange-400' : 'bg-sky-400'}`} />
              {reg.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
