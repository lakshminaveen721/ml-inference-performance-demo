import time
import requests
import sys

URL = "http://localhost:8000/health"
TIMEOUT = 60  # seconds

start = time.time()

while time.time() - start < TIMEOUT:
    try:
        r = requests.get(URL, timeout=1)
        if r.status_code == 200:
            print("✅ Service is ready")
            sys.exit(0)
    except Exception:
        pass

    time.sleep(1)

print("❌ Service did not become ready in time")
sys.exit(1)
