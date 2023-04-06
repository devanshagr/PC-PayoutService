import io
import glob
import logging
import os
import pandas as pd
import requests
import time

from datetime import date, datetime
from dateutil import relativedelta

logging.basicConfig(level="INFO")

API_URL = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{}_NSW1.csv"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}
HISTORICAL_PRICE_DATA_PATH = "Data/Historical_Price_Data"
Q4_MONTHS = [10, 11, 12]
START_DATE = date(1998, 1, 1)
SLEEP_FOR = 0

def save_file(content, year_month):
    """
        Saves the fetched data from an API response to a CSV file.

        Args:
        response (requests.Response): A requests Response object containing the API response data.
        year_month (str): A string representing the year and month in 'YYYYMM' format for which the data needs to be saved.

        Returns:
        None
    """
    response_data = pd.read_csv(io.StringIO(content))
    if not os.path.exists(HISTORICAL_PRICE_DATA_PATH):
        os.mkdir(HISTORICAL_PRICE_DATA_PATH)
    file_path = f"{HISTORICAL_PRICE_DATA_PATH}/{year_month}.csv"
    # response_data.to_csv(file_path, index=None)

def extract_content_from_response(response):
    """
        Extracts file content from response object.

        Args:
        response (requests.Response): A requests Response object containing the API response data.

        Returns:
        response text
    """
    return response.content.decode('utf-8')
    
def transform_data(df):
    df["datetime"] = pd.to_datetime(df["SETTLEMENTDATE"])
    df = df.append(
        {"datetime": df["datetime"].min() - pd.DateOffset(minutes = 25)},
        ignore_index=True
    )
    output = df.resample("5min", on="datetime")[["RRP"]].last().div(1).bfill().reset_index()
    output["SETTLEMENTDATE"] = output["datetime"]
    output = output.drop("datetime", axis=1)[[ "SETTLEMENTDATE", "RRP"]]
    # output = output[output["SETTLEMENTDATE"].dt.month.isin(Q4_MONTHS)]
    return output

def get_data(year_month):
    """
        Fetches data for a given year and month from an API and saves the response to a file.
        If the response fails, it logs a warning message.

        Args:
        year_month (str): A string representing the year and month in 'YYYYMM' format for which the data needs to be fetched.

        Returns:
        response object or None
    """

    url = API_URL.format(year_month)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        # logging.warning(f"Response failed with reason {response.reason} and error {response.content}")
        logging.warning(f"Request not completed for {year_month} ")
        return
    return response

def format_year_month(date_obj):
    """
        Takes a date object as input and,
        returns a string representing the year and month of the input date in the format 'YYYYMM'.

        Args:
        date_obj (datetime.date):
            A datetime date object representing the date for which the year and month needs to be formatted.

        Returns:
        str: A string representing the year and month of the input date in the format 'YYYYMM'.
    """

    year = date_obj.year
    month = str(date_obj.month).zfill(2)
    return f"{year}{month}"

def get_historical_data():

    """
        Fetches historical data for a given range of years and months.
        It starts from the start date and iterates over each month till the current date.
        It fetches data for each month by calling the get_data function and then waits for 3 seconds before moving on to the next month.

        Args:
        None

        Returns:
        None
    """

    logging.info("Historical Data Fetch Starting")

    today_date = datetime.today().date()

    today_year_month = format_year_month(today_date)

    current_year_month = format_year_month(START_DATE)

    while current_year_month <= today_year_month:
        logging.info(f"Getting data for {current_year_month}")
        response = get_data(current_year_month)
        if response:
            content = extract_content_from_response(response)
            save_file(content, year_month=current_year_month)
        next_date = datetime.strptime(current_year_month, '%Y%m') + relativedelta.relativedelta(months=1)
        current_year_month = format_year_month(next_date)
        time.sleep(SLEEP_FOR)

    logging.info("Historical Data Fetch Completed")

def combine_historical_data():
    all_files = glob.glob(os.path.join(HISTORICAL_PRICE_DATA_PATH , "*.csv"))

    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    
    combined_df = pd.concat(li, axis=0, ignore_index=True)
    transformed_df = transform_data(combined_df)
    dir_to_save = f"{HISTORICAL_PRICE_DATA_PATH}/Combined_Price_Data"
    if not os.path.exists(dir_to_save):
        os.mkdir(dir_to_save)
    path_to_save = os.path.join(dir_to_save, "Combined_Data.csv")
    transformed_df.to_csv(path_to_save, index=False)

if __name__ == "__main__":
    get_historical_data()
    combine_historical_data()
