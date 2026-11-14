import subprocess
import time
import urllib.request
import json
import sys

print('Starting FastAPI uvicorn server in subprocess...')
proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--port', '8000', '--host', '127.0.0.1'])

try:
    time.sleep(3)
    print('1. Testing /health...')
    with urllib.request.urlopen('http://127.0.0.1:8000/health') as resp:
        print('Health status:', resp.read().decode())

    print('2. Testing /api/planets...')
    with urllib.request.urlopen('http://127.0.0.1:8000/api/planets') as resp:
        planets = json.loads(resp.read().decode())
        planet_names = [p['name'] for p in planets]
        print('Available planets:', planet_names)

    print('3. Testing /api/analysis/start for Mars Jezero Crater...')
    req_data = json.dumps({
        'planet': 'mars',
        'latitude': 18.38,
        'longitude': 77.58,
        'radius_km': 50.0
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/analysis/start', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Analysis ID: {res['analysis_id']}")
        print(f"Ranked {len(res['candidates'])} Earth analog candidates in {res['computation_time_ms']} ms")
        top = res['candidates'][0]
        print(f"Top Earth Analog: {top['name']} ({top['country']}) - {top['overall_similarity']}% Match")

    print('4. Testing /api/reports/generate for Top Analog...')
    rep_data = json.dumps({
        'analysis_id': res['analysis_id'],
        'candidate_id': top['candidate_id']
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/reports/generate', data=rep_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        rep_res = json.loads(resp.read().decode())
        print("Generated PDF report:", rep_res['filename'], f"({rep_res['file_size_bytes']} bytes)")

    print('5. Testing /api/reports/{id}/download...')
    with urllib.request.urlopen(f"http://127.0.0.1:8000{rep_res['download_url']}") as resp:
        pdf_bytes = resp.read()
        print(f"Successfully downloaded report: {len(pdf_bytes)} bytes")

    print('\nALL FASTAPI INTEGRATION TESTS PASSED PERFECTLY!')

finally:
    proc.terminate()
    proc.wait()
    print('Server stopped.')
