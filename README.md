Steps to run the service:
1. Clone the repo
2. cd `PC-PayoutService`
3. Add virtual env by `python3 -m venv venv`
4. Activate the virtual env by `source venv/bin/activate`
5. Run `pip install -r requirements.txt` to install the libraries
6. Run `run.py` to start the Flask app.
7. Flask will app run on `http://127.0.0.1:5010`

Endpoints:
1. `http://127.0.0.1:5010/payout?strike=300&tMax=40&year=2000`: gives annual payout information in JSON. <br />
URL Arguments: Strike, Temp Max, and Year
2. `http://127.0.0.1:5010/future_price`: runs web scrapper on Chromedriver and stores the future price `Data_Source/Future_Price.txt`.


Data Sources:
1. Future Price data has been scrapped from https://www.asxenergy.com.au/futures_au. Q423 data has been scrapped. Scrapper can be found at `scripts/scraper.py` and data is loaded in `Data_Source/Future_Price.txt`.
2. Historical Price Data is from https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data. All the data has been downloaded into the folder `Data_Source/Historical_Price_Data`.
Also, data has been combined into a single csv and stored in `Data_Source/Historical_Price_Data/Combined_Price_Data/Combined_Data_q4.csv`. This data has been transformed to have only Q4 prices (since future price data is for Q4) and for months for which we only have price in 30 mins interval, same price is loaded at 5 mins interval.<br>
Script to load the historical data is placed in `scripts/historical_electricity_price_data.py`.
3. Historical Weather data is loaded in `Data_Source/Sydney_Airport_Tmax.csv`.

