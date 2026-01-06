import time
import requests
import statistics

URL = "http://localhost:8000/predict"
REQUESTS = 50
LATENCIES = []

payload = {"data": [1, 2, 3]}

for _ in range(REQUESTS):
    start = time.time()
    r = requests.post(URL, json=payload, timeout=2)
    r.raise_for_status()
    LATENCIES.append(time.time() - start)

avg_latency = statistics.mean(LATENCIES)
p95_latency = statistics.quantiles(LATENCIES, n=20)[18]

print(f"AVG_LATENCY={avg_latency:.4f}")
print(f"P95_LATENCY={p95_latency:.4f}")

# ---- Performance Gates ----
MAX_AVG_LATENCY = 0.25   # 250 ms
MAX_P95_LATENCY = 0.50   # 500 ms

if avg_latency > MAX_AVG_LATENCY:
    raise SystemExit("❌ Avg latency regression")

if p95_latency > MAX_P95_LATENCY:
    raise SystemExit("❌ P95 latency regression")

print("✅ Performance checks passed")
