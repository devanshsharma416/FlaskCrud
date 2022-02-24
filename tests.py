import requests
import random


BASE = 'http://127.0.0.1:5000/'

data = [{"name": "Tim", "address": "New York", "mobile": random.randint(9000000000, 9900000000), "designation": "Software Engineer"},
        {"name": "Joe", "address": "Bihar", "mobile": random.randint(9000000000, 9900000000), "designation": "Banker"},
        {"name": "Mathew", "address": "Europe", "mobile": random.randint(9000000000, 9900000000), "designation": "Tester"}]


for i in range(len(data)):
    response = requests.post(BASE + "employee/" + str(i), data[i])
    print(response.json())
input()

# response = requests.delete(BASE + "video/2")
# print(response)

response = requests.get(BASE + "employee/1")
print(response.json())

input()
response = requests.patch(BASE + "employee/0", {'name': "Bhikari", 'designation': 'HR'})
print(response.json())



