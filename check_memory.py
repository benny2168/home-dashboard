import requests, urllib3, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PORTAINER_URL = "https://docker.server.mtcd.org"
HEADERS = {"X-API-Key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="}

def mb(b): return round(b / 1024 / 1024, 1)

resp = requests.get(f"{PORTAINER_URL}/api/endpoints", headers=HEADERS, verify=False, timeout=30)
endpoints = resp.json()

all_results = []

for ep in endpoints:
    env_id = ep["Id"]
    env_name = ep["Name"]
    
    cnt_resp = requests.get(
        f"{PORTAINER_URL}/api/endpoints/{env_id}/docker/containers/json?all=0",
        headers=HEADERS, verify=False, timeout=30
    )
    if cnt_resp.status_code != 200:
        continue

    containers = cnt_resp.json()
    print(f"\n=== {env_name} ({len(containers)} running containers) ===")

    for c in containers:
        name = c["Names"][0].lstrip("/")
        cid = c["Id"]

        try:
            stat_resp = requests.get(
                f"{PORTAINER_URL}/api/endpoints/{env_id}/docker/containers/{cid}/stats?stream=false",
                headers=HEADERS, verify=False, timeout=15
            )
            if stat_resp.status_code != 200:
                continue

            stats = stat_resp.json()
            mem = stats.get("memory_stats", {})
            used = mem.get("usage", 0) - mem.get("stats", {}).get("cache", 0)
            limit = mem.get("limit", 0)
            pct = round(used / limit * 100, 1) if limit else 0

            all_results.append((env_name, name, used, limit, pct))
        except Exception as e:
            print(f"  [{name}] Error: {e}")

# Sort by memory used descending
all_results.sort(key=lambda x: x[2], reverse=True)

print("\n\n{'='*70}")
print(f"{'CONTAINER':<40} {'USED':>8} {'LIMIT':>8} {'%':>6}  ENV")
print("="*70)
for env_name, name, used, limit, pct in all_results:
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    flag = " ⚠️" if pct > 75 else (" 🔴" if pct > 90 else "")
    print(f"{name:<40} {mb(used):>6}MB {mb(limit):>6}MB {pct:>5}%  [{bar}]{flag}  ({env_name})")
