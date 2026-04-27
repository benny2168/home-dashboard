import urllib.request, json, ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
req = urllib.request.Request("http://100.100.57.37:9000/api/stacks/58/file", headers={"x-api-key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="})
with urllib.request.urlopen(req, context=ssl_context) as r:
    print(json.loads(r.read().decode())["StackFileContent"])
