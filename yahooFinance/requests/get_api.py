import requests

id = input("Enter the id of the stock you would like to look up: ")
response =requests.get('http://localhost:5000/stock/' + id)
print(response.json())