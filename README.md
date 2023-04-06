Steps to run the service:

1. Clone the repo
2. cd `PC-PayoutService`
3. Add virtual env by `python3 -m venv venv`
4. Activate the virtual env by `source venv/bin/activate`
5. Run `pip install -r requirements.txt` to install the libraries
6. Flask will app run on `http://127.0.0.1:5010`

Endpoint:
    `http://127.0.0.1:5010/payout?strike=300&tMax=40&year=2000`: gives annual payout information in JSON
    URL Arguments: Strike, Temp Max, and Year


Data Sources:
1. Future Price data has been scrapped from https://www.asxenergy.com.au/futures_au. As instructed, Q423 has data has been scrapped. Scrapper can be found at `scripts/scraper.py`
2. Historical Price Data is from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data. All the data has been downloaded into the folder `Data_Source/Historical_Price_Data`.
Also, data has been combined into a single csv and stored in  `Data_Source/Historical_Price_Data/Combined_Price_Data/Combined_Data_q4.csv`. Script to load the historical data is placed in `scripts/historical_electricity_price_data.py`
3. Historical Weather data is loaded in `Data_Source/Sydney_Airport_Tmax.csv`

