import urllib.request
import json
import ssl
import sys

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

base = "http://100.100.57.37:9000"
token = "YOUR_PORTAINER_TOKEN_HERE"
stack_id = 58 

# The compose file to deploy — includes persistent uploads volume
STACK_FILE = """services:
  app:
    image: mtcdtech/homedashboard:latest
    container_name: homedashboard-app
    command: node server.js
    ports:
      - "4001:4000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:password@homedashboard-db:5432/dashboard?schema=public
      - NEXTAUTH_URL=https://home.server.mtcd.org
      - AUTH_URL=https://home.server.mtcd.org
      - AUTH_TRUST_HOST=true
      - AUTH_MICROSOFT_ENTRA_ID_ID=a82f1c71-902e-4b86-a257-8e4948f1a141
      - AUTH_MICROSOFT_ENTRA_ID_SECRET=YOUR_ENTRA_ID_SECRET_HERE
      - AUTH_MICROSOFT_ENTRA_ID_TENANT_ID=e4d1ae10-59a0-4640-bbd4-d88df4b9636b
      - AUTH_SECRET=YOUR_AUTH_SECRET_HERE
    volumes:
      - homedashboard_uploads:/app/public/uploads
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: homedashboard-db
    restart: always
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dashboard
    volumes:
      - homedashboard_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d dashboard"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  homedashboard_db_data:
  homedashboard_uploads:
"""

def get_stack():
    url = f"{base}/api/stacks/{stack_id}"
    req = urllib.request.Request(url, headers={"x-api-key": token})
    with urllib.request.urlopen(req, context=ssl_context) as r:
        return json.loads(r.read().decode())

def update_stack():
    stack = get_stack()
    
    payload = {
        "StackFileContent": STACK_FILE,
        "Env": stack.get("Env", []),
        "Prune": False,
        "PullImage": True
    }
    
    url = f"{base}/api/stacks/{stack_id}?endpointId={stack['EndpointId']}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": token,
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as r:
            print("Stack Redeployed Successfully!")
            print(r.read().decode())
    except urllib.error.HTTPError as e:
        print("Update Failed:", e.code)
        print(e.read().decode(errors="replace"))
        sys.exit(1)

if __name__ == "__main__":
    update_stack()
