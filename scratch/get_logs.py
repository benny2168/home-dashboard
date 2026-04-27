import urllib.request
import json
import ssl
import sys

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

base = "http://100.100.57.37:9000"
token = "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="
endpoint_id = 2

# 1. Get Containers
url = f"{base}/api/endpoints/{endpoint_id}/docker/containers/json?all=1"
req = urllib.request.Request(url, headers={"x-api-key": token})
try:
    with urllib.request.urlopen(req, context=ssl_context) as r:
        containers = json.loads(r.read().decode())
        
        homedashboard_container = None
        for c in containers:
            for name in c.get('Names', []):
                if 'homedashboard-app' in name:
                    homedashboard_container = c['Id']
                    break
            if homedashboard_container:
                break
                
        if not homedashboard_container:
            print("homedashboard container not found.")
            sys.exit(1)
            
        # 2. Get Logs
        log_url = f"{base}/api/endpoints/{endpoint_id}/docker/containers/{homedashboard_container}/logs?stderr=1&stdout=1&tail=50"
        log_req = urllib.request.Request(log_url, headers={"x-api-key": token})
        with urllib.request.urlopen(log_req, context=ssl_context) as lr:
            print(lr.read().decode(errors="replace"))
            
except Exception as e:
    print(f"Error: {e}")
