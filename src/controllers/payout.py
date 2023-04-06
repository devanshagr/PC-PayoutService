import json
import logging
import numpy as np
import pandas as pd
import traceback

from flask import abort
from pydantic import validate_arguments, ValidationError

from src.data.models.payout_request import PayoutRequest

log = logging.getLogger(__name__)

HISTORICAL_PRICE_DATA_PATH = "Data/Historical_Price_Data/Combined_Price_Data/Combined_Data_q4.csv"
TMAX_DATA_PATH = "Data/Sydney_Airport_Tmax.csv"
FUTURE_PRICE_FILE = "Data/Future_Price.txt"
Q4_MONTHS = [10, 11, 12]


def read_historical_data():
    return pd.read_csv(HISTORICAL_PRICE_DATA_PATH, index_col=None, header=0)

def read_tmax_data():
    return pd.read_csv(TMAX_DATA_PATH, index_col=None, header=0)

def read_future_price_data():
    with open(FUTURE_PRICE_FILE) as f:
        lines = f.readlines()
    if not lines:
        raise Exception("Future Price Data not found")
    future_price_json = json.loads(lines[0])
    return float(future_price_json.get("future_price"))

def filter_historical_price_data(hist_price_df, year):
    hist_price_df["SETTLEMENTDATE"] = pd.to_datetime(hist_price_df["SETTLEMENTDATE"])
    hist_price_df = hist_price_df[hist_price_df["SETTLEMENTDATE"].dt.year >= year]
    return hist_price_df[hist_price_df["SETTLEMENTDATE"].dt.month.isin(Q4_MONTHS)]

def filter_tmax_data(tmax_df, year):
    tmax_df["Dates"] = pd.to_datetime(tmax_df["Dates"])
    return tmax_df[tmax_df["Dates"].dt.year >= year]

def scale_price_data(hist_price_df, future_price):
    hist_price_df['RRP_mean'] = hist_price_df.groupby(hist_price_df.SETTLEMENTDATE.dt.year).RRP.transform(lambda s: s.mean())
    hist_price_df['Scaled_Price'] = (hist_price_df["RRP"] * future_price) / hist_price_df["RRP_mean"]
    return hist_price_df

def payout_formula(hist_price_df, tmax_df, strike, tmax_trigger):
    
    hist_price_df["Date"] = hist_price_df["SETTLEMENTDATE"].dt.date
    tmax_df["Date"] = tmax_df["Dates"].dt.date
    hist_price_df = hist_price_df.set_index('Date').join(tmax_df.set_index("Date"), on="Date")
    
    hist_price_df["Scaled-Strike"] = hist_price_df["Scaled_Price"] - strike
    hist_price_df["Scaled0"] = 0
    hist_price_df["Payout_5min"] = hist_price_df[["Scaled-Strike", "Scaled0"]].max(axis=1)
    hist_price_df["Payout_5min"] = np.where(hist_price_df['Tmax'] >= tmax_trigger, hist_price_df["Payout_5min"], 0)


    hist_price_df = hist_price_df.drop(columns=['Scaled-Strike', 'Scaled0', 'RRP_mean', 'Scaled_Price', 'Tmax'], axis = 1)


    hist_price_df["Year"] = hist_price_df["SETTLEMENTDATE"].dt.year
    return hist_price_df.groupby(["Year"])["Payout_5min"].sum().round(2)

@validate_arguments
def calculate_payout(data: PayoutRequest):
    try:
        future_price = read_future_price_data()
    except FileNotFoundError as fne:
        error = "Historical file not found"
        log.error(traceback.format_exc())
        abort(500, description=str(error))
    try:
        hist_price_df = read_historical_data()
    except FileNotFoundError as fne:
        error = "Historical file not found"
        log.error(traceback.format_exc())
        abort(500, description=str(error))
    try:
        tmax_df = read_tmax_data()
    except FileNotFoundError as fne:
        error = "tmax_df file not found"
        log.error(traceback.format_exc())
        abort(500, description=str(error))

    hist_price_df = filter_historical_price_data(hist_price_df, data.year)
    tmax_df = filter_tmax_data(tmax_df, data.year)
    hist_price_df = scale_price_data(hist_price_df, future_price)
    hist_price_df = payout_formula(hist_price_df, tmax_df, data.strike, data.tMax)
    year_payout_data = hist_price_df.to_dict()
    return [
        { "year" : year, "payout": payout } for year, payout in year_payout_data.items()
    ]

def payout(data):
    try:
        return calculate_payout(data)
    except ValidationError as e:
        log.exception(str(e))
        abort(400, description=str(e))
    except Exception as e:
        log.error(str(e))
        abort(500, description=str(e))