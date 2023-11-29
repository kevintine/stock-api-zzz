# Stock Trading Flask App

This is a stock trading analysis appilation. It analyzes stocks based off different recent candlestick patterns.

It pulls data from a SQL database as well as an excel sheet to analyze data. 

I used the yahoo-finance API to grab data from certain stocks I want to watch and store it into the SQL database. There's a .py file that needs to be run basically everyday to update the daily stock data. It's a request library script that just grabs all the days from today and updates the database. 

There's a very bad candlestick chart that displays the stocks I'm watching. Need to fix that up. 

Also this uses flask to setup the server to display the html and talk to the SQL database. 

Overall this still has a lot of work to do but it also has a lot of work put into it and hey, however long it takes, this is a passion project. 

Run it here.
```
python app.py
```


