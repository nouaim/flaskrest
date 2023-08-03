import requests

BASE = "http://127.0.0.1:5000"

response = requests.put(BASE + "/video/35", json={"name": "fun", "likes": 3333, "views": 44})

print(response.json())

# unnecessary input to seperate exucution of responses
input()

response = requests.get(f"{BASE}/video/33")

print(response.json())
