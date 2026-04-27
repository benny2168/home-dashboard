import urllib.request
import json
import ssl
import tarfile
import os
import sys

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

base = "http://100.100.57.37:9000"
token = "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="
cid = "d887fa33bd97756fee8e1ae1bde3ca9eb6a4740804d833c47a1c46d30a70c36e"

def create_tar():
    print("Creating tarball...")
    with tarfile.open("scratch/deploy.tar.gz", "w:gz") as tar:
        for f in ["src", "public", "prisma", "package.json", "package-lock.json", "Dockerfile", "docker-compose.yml", "next.config.ts", "entrypoint.sh", "tsconfig.json", "postcss.config.mjs", "tailwind.config.ts"]:
            if os.path.exists(f):
                tar.add(f)
    print(f"Tarball created: {os.path.getsize('scratch/deploy.tar.gz')} bytes")

def build_image():
    print("Uploading to Portainer Build API...")
    url = f"{base}/api/endpoints/2/docker/build?t=mtcdtech/homedashboard:latest"
    with open("scratch/deploy.tar.gz", "rb") as f:
        data = f.read()
    
    req = urllib.request.Request(url, data=data, headers={
        "x-api-key": token,
        "Content-Type": "application/x-tar"
    })
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as r:
            lines = r.read().decode().splitlines()
            for l in lines[-5:]:
                print("Build log:", l)
    except urllib.error.HTTPError as e:
        print(f"Build failed: {e.code}")
        print(e.read().decode(errors="replace")[:500])
        sys.exit(1)

def recreate_container():
    print("Recreating container by restarting it? Wait, portainer might not use the new image just on restart.")
    # Actually, we need to stop, remove, and start a new container with the same config, OR update the stack.
    print("To recreate, we will send a container stop and start.")
    # Stop:
    req_stop = urllib.request.Request(f"{base}/api/endpoints/2/docker/containers/{cid}/stop", data=b"", headers={"x-api-key": token}, method="POST")
    try:
        urllib.request.urlopen(req_stop, context=ssl_context)
    except Exception as e:
        print("Stop error:", e)

    # Start:
    req_start = urllib.request.Request(f"{base}/api/endpoints/2/docker/containers/{cid}/start", data=b"", headers={"x-api-key": token}, method="POST")
    try:
        urllib.request.urlopen(req_start, context=ssl_context)
        print("Started.")
    except Exception as e:
        print("Start error:", e)

if __name__ == "__main__":
    create_tar()
    build_image()
    # Note: Just restarting might not pull the newly built image if the container is not recreated.
    # We will try just restarting first to see if it works, otherwise I will use the Stack Update API.
    recreate_container()
