import requests
import random

def c():
        print("hello World")

BASE = 'http://127.0.0.1:5000/'

data = [{"name": "Tim", "likes": 10000, "views": random.randint(1000, 1000000)},
        {"name": "Joe", "likes": 10020, "views": random.randint(1000, 1000000)},
        {"name": "Mathew", "likes": 30000, "views": random.randint(1000, 1000000)}]


# for i in range(len(data)):
#     response = requests.post(BASE + "video/" + str(i), data[i])
#     print(response.json())
# input()

response = requests.delete(BASE + "video/2")
print(response)

response = requests.get(BASE + "video/2")
print(response.json())

input()
response = requests.patch(BASE + "video/1", {'likes': 99})
print(response.json())



