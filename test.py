import requests

BASE = "http://127.0.0.1:5000"

response2 = requests.put(BASE + "/video/32", json={"name": "fun", "likes": 3333, "views": 44})

print(response2.json())

input()

response = requests.get(f"{BASE}/video/3")

print(response.json())
