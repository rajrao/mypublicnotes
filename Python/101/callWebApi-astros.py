import requests

apiUrl = "http://api.open-notify.org/astros.json"
request = requests.get(apiUrl)
json = request.json()
for k,v in json.items():
    print(f"{k}:{v}")

for astro in json.get("people"):
    print(astro["name"])