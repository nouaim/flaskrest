import requests
'''Testing different requests the API can perform'''

BASE = "http://127.0.0.1:5000"


# Put a video of a Car, its id is 35
response = requests.put(BASE + "/video/35", json={"name": "Car", "likes": 2321, "views": 99999})

print(response.json())

# unnecessary input to seperate exucution of responses
input()
# Get the data of the car video
response = requests.get(f"{BASE}/video/35")
print(response.json())

# Test if the server crashes if we try to get an id that doesn't exist
input()
response = requests.get(f"{BASE}/video/39")
print(response.json())

# Update the name of the car
input()
response = requests.patch(
    BASE + "/video/35", json={"name": "Football"})
print(response.json())

# Update the likes
input()
response = requests.patch(
    BASE + "/video/35", json={"likes": "5000"})
print(response.json())