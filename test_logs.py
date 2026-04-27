import requests
url = "http://mtcd-server.tail654dd.ts.net:9000/api/endpoints/2/docker/containers/120444bd10af5d460b297b50431f1a8fd08ad777958f816e689c3ac83d0ff423/logs?stdout=1&stderr=1&tail=50"
headers = {"X-API-Key": "ptr_caKh16OVXC+3G4shu9s7TXtumDZY04R6wwaOYkq+Pls="}
r = requests.get(url, headers=headers, verify=False)
print(r.text)
