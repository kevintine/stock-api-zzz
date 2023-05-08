import requests

BASE = "http://localhost:5000/"

response = requests.get(BASE + "helloworld/kevin/1")

print(response.json())