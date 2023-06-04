import requests
import get_api as get

get

id = input("Enter the day of the stock you would like to look up:")

response = requests.get('http://localhost:5000/stock/' + get.id + '/' + id)

print(response.json())