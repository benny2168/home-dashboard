#!/usr/bin/env python3

import os
import time
import requests
import re

# Update stack58.yml with current timestamp
with open("stack58.yml", "r") as f:
    content = f.read()

new_content = re.sub(r'REDEPLOY_DATE=\d+', f'REDEPLOY_DATE={int(time.time())}', content)

with open("stack58.yml", "w") as f:
    f.write(new_content)

print("Updated REDEPLOY_DATE in stack58.yml")

url = "http://mtcd-server.tail654dd.ts.net:9000/api/stacks/58?endpointId=2"
headers = {"X-API-Key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls=", "Content-Type": "application/json"}

data = {
    "StackFileContent": new_content,
    "Env": [],
    "Prune": False,
    "PullImage": True
}

try:
    r = requests.put(url, headers=headers, json=data, verify=False)
    print(r.status_code, r.text)
except Exception as e:
    print("Error:", e)
