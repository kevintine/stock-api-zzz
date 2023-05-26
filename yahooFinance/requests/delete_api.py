import requests

id = input("Enter the id of the stock you would like to delete: ")
response =requests.delete('http://localhost:5000/stock/' + id)
print(response.json())
