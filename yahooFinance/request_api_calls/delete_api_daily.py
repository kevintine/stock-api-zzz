import requests
import get_api as get
import get_api_daily as get_daily

get
get_daily
id = input("Enter the id of the daily stock data you would like to delete (Enter 0 to delete all): ")

response =requests.delete('http://localhost:5000/stock/' + get.id + '/' + id)
