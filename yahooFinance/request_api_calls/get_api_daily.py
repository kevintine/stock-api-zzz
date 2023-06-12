import requests
import get_api as get

get

id = input("Enter the day of the stock you would like to look up (Enter 0 to get all):")
id = int(id)

response = requests.get('http://localhost:5000/stock/' + get.id + '/' + str(id))
print(response.json())
# response = requests.get('http://localhost:5000/stock/' + get.id + '/' + id)

# print(response.json())