import requests
import get_api as get

get

id = input("Enter the day of the stock you would like to look up (Enter 0 to get all):")
id = int(id)

if id == 0:
    print("working")
    for i in range(len(get.response.json())):
        day_id = i + 1
        print(day_id)
        print((len(get.response.json())))
        response = requests.get('http://localhost:5000/stock/' + get.id + '/' + str(day_id))
        print(response.json())
# response = requests.get('http://localhost:5000/stock/' + get.id + '/' + id)

# print(response.json())