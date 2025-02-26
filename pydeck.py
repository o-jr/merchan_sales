import streamlit as st  
import pandas as pd
import pydeck as pdk

DATA_PATH = "data/merchandise-sales.csv"

def load_data(nrows):
    columns = {"Order Date": "order_date", "Product Name": "product_name", "Order ID": "order_id", "Quantity": "quantity"}

    data = pd.read_csv(DATA_PATH, index_col='code')
    data.data = data.rename(columns=columns)
    data.data = pd.to_datetime(data.data)
    data = data(list(columns.values()))
    return data

    #44m