import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PORTAINER_URL = "http://mtcd-server.tail654dd.ts.net:9000"
HEADERS = {"X-API-Key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="}

resp = requests.get(f"{PORTAINER_URL}/api/endpoints", headers=HEADERS, verify=False)
endpoints = resp.json()

for ep in endpoints:
    env_id = ep["Id"]
    env_name = ep["Name"]
    print(f"Scanning: {env_name} (ID: {env_id})")
    cnt_resp = requests.get(f"{PORTAINER_URL}/api/endpoints/{env_id}/docker/containers/json?all=1", headers=HEADERS, verify=False)
    if cnt_resp.status_code != 200:
        continue
    for c in cnt_resp.json():
        names = c.get("Names", [])
        image = c.get("Image", "")
        if "homedashboard" in image.lower() or any("homedashboard" in n.lower() for n in names):
            cid = c["Id"]
            print(f"  Found: {names} | Image: {image} | Status: {c['State']}")
            print("  Pulling latest image...")
            pull = requests.post(f"{PORTAINER_URL}/api/endpoints/{env_id}/docker/images/create?fromImage={image}", headers=HEADERS, verify=False)
            print(f"  Pull response: {pull.status_code}")
            print("  Restarting container...")
            restart = requests.post(f"{PORTAINER_URL}/api/endpoints/{env_id}/docker/containers/{cid}/restart", headers=HEADERS, verify=False)
            print(f"  Restart response: {restart.status_code} - {'OK' if restart.status_code == 204 else restart.text}")
