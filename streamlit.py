import streamlit as st
import duckdb
import pandas as pd
import numpy as np

DATA_COLUMN="order date"
DATA_URL = "data/merchandise-sales.csv"

#con = duckdb.connect()



def load_data(nrows):
    data = pd.read_csv('data/merchandise-sales.csv', nrows=nrows)
    lower = lambda x: x.lower()#remove_space = lambda x: x.strip()
    data.rename(lower, axis='columns', inplace=True)
    data[DATA_COLUMN] = pd.to_datetime(data["order date"])
    return data
      


st.subheader("Data Sample")
data_load = st.title("Weather Station SUmmary")
data_load.text(f"Loading data from {DATA_URL}")  
data = load_data(10000)
data_load.empty()
data_load.title("Data loaded: {data.shape[0]} rows") 
st.subheader("Profiling")
st.write(data.describe())  
data_load.write(data.head())


st.subheader("KPIs: Key Performance Indicators")

total_sales = data["total sales"].sum()
st.subheader(f"Total Sales: ${total_sales:}")

st.subheader("Total Sales Over the Months")
total_sales_per_month = data.groupby(data["order date"].dt.to_period("M"))["total sales"].sum()
total_sales_per_month.index = total_sales_per_month.index.to_timestamp()
st.line_chart(total_sales_per_month)

shippinng_charges = data["shipping charges"].sum()
st.subheader(f"Shipping Charges: ${shippinng_charges:}")

st.subheader("Shipping Charges Over the Year 2024")
shipping_charges_2024 = data[data["order date"].dt.year == 2024].groupby(data["order date"].dt.to_period("M"))["shipping charges"].sum()
shipping_charges_2024.index = shipping_charges_2024.index.to_timestamp()
st.line_chart(shipping_charges_2024)

qty_total_sales = data["total sales"].count()
st.subheader(f"Qty Sales: ${qty_total_sales:}")

total_international_sales = data[data["international shipping"] == "Yes"]["total sales"].sum()
st.subheader(f"Total International Sales: ${total_international_sales:}")

st.subheader("Total International Sales Over the Months")
total_international_sales_per_month = data[data["international shipping"] == "Yes"].groupby(data["order date"].dt.to_period("Y"))["total sales"].sum()
total_international_sales_per_month.index = total_international_sales_per_month.index.to_timestamp()

st.data_editor(
    total_international_sales_per_month.reset_index().rename(columns={"order date": "Month", "total sales": "Sales"}),
    column_config={
        "Sales": st.column_config.LineChartColumn(
            "Total International Sales (Monthly)",
            width="large",
            help="The total international sales volume per month",
            y_min=0,
        ),
    },
    hide_index=True,
)

total_national_shipping = data[data["international shipping"] == "Yes"]["international shipping"].count()
st.subheader(f"Qty International Sales: {total_national_shipping}")

total_national_sales = data[data["international shipping"] == "No"]["total sales"].sum()
st.subheader(f"Total National Sales: ${total_national_sales:}")

total_national_shipping = data[data["international shipping"] == "No"]["international shipping"].count()
st.subheader(f"Qty National Sales: {total_national_shipping}")

qty_sales = data["quantity"].sum()
st.subheader(f"Qty Products Sold: {qty_sales:}")

average_rating = data["rating"].mean()
st.subheader(f"Average Rating: {average_rating:.2f}")

qty_average_rating = data["rating"].count()
st.subheader(f"Qty Rating: {qty_average_rating:}")



if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)


st.subheader("Data Visualization")
st.write("Histogram")
hist_values = np.histogram(data["order date"].dt.month, bins=12, range=(1,13))[0]
#hist_values = np.histogram(data[DATA_COLUMN].dt.days, bins=31, range=(0,31))[0]
st.bar_chart(hist_values)


st.subheader("Most and Least Popular Products")
   # Group by product id and sum the total sales
product_sales = data.groupby("product id")["total sales"].sum()
    # Sort the product sales in descending order
sorted_product_sales = product_sales.sort_values(ascending=True)
    # Display the horizontal bar chart
st.bar_chart(sorted_product_sales)




month_filter = st.slider("Month", 1, 12, 7)
# Assuming the data has 'latitude' and 'longitude' columns
filtered_data = data[data[DATA_COLUMN].dt.month == month_filter]

st.subheader("Map for month {}:".format(month_filter))
if 'latitude' in filtered_data.columns and 'longitude' in filtered_data.columns:
    filtered_data['latitude'] = filtered_data['latitude'].str.replace(',', '').astype(float)
    filtered_data['longitude'] = filtered_data['longitude'].str.replace(',', '').astype(float)
    st.map(filtered_data)
else:
    st.write("No latitude and longitude data available for mapping.")


