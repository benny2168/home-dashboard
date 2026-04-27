import requests
import json
url = "http://mtcd-server.tail654dd.ts.net:9000/api/endpoints/2/docker/containers/json?all=1"
headers = {"X-API-Key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls=", "Content-Type": "application/json"}
r = requests.get(url, headers=headers, verify=False)
containers = r.json()
homedashboard = next((c for c in containers if "/homedashboard-app" in c.get("Names", [])), None)
print(json.dumps(homedashboard, indent=2))
