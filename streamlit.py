import streamlit as st
import pandas as pd
import numpy as np

# Define constants for data column and URL
DATA_COLUMN = "order date"
DATA_URL = "data/merchandise-sales.csv"

# Function to load data with caching
#@st.cache
def load_data(nrows):
    # Read CSV file
    data = pd.read_csv('data/merchandise-sales.csv', nrows=nrows)
    # Convert column names to lowercase
    lower = lambda x: x.lower()
    data.rename(lower, axis='columns', inplace=True)
    # Convert order date column to datetime
    data[DATA_COLUMN] = pd.to_datetime(data["order date"])
    return data

# Display subheader
st.subheader("Data Sample")
# Display title
data_load = st.title("Weather Station Summary")
# Display loading text
data_load.text(f"Loading data from {DATA_URL}")
# Load data
data = load_data(10000)
# Clear loading text
data_load.empty()
# Display data loaded message
data_load.title(f"Data loaded: {data.shape[0]} rows")
# Display subheader for profiling
st.subheader("Profiling")
# Display data description
st.write(data.describe())
# Display first few rows of data
data_load.write(data.head())

# Display subheader for KPIs
st.subheader("KPIs: Key Performance Indicators")

# Calculate total sales
total_sales = data["total sales"].sum()
# Display total sales
st.subheader(f"Total Sales: ${total_sales:}")

# Display subheader for total sales over the months
st.subheader("Total Sales Over the Months")
# Calculate total sales per month
total_sales_per_month = data.groupby(data["order date"].dt.to_period("M"))["total sales"].sum()
total_sales_per_month.index = total_sales_per_month.index.to_timestamp()
# Display line chart for total sales per month
st.line_chart(total_sales_per_month)

# Calculate shipping charges
shipping_charges = data["shipping charges"].sum()
# Display shipping charges
st.subheader(f"Shipping Charges: ${shipping_charges:}")

# Display subheader for shipping charges over the year 2024
st.subheader("Shipping Charges Over the Year 2024")
# Calculate shipping charges for 2024
shipping_charges_2024 = data[data["order date"].dt.year == 2024].groupby(data["order date"].dt.to_period("M"))["shipping charges"].sum()
shipping_charges_2024.index = shipping_charges_2024.index.to_timestamp()
# Display line chart for shipping charges in 2024
st.line_chart(shipping_charges_2024)

# Calculate quantity of total sales
qty_total_sales = data["total sales"].count()
# Display quantity of total sales
st.subheader(f"Qty Sales: ${qty_total_sales:}")

# Calculate total international sales
total_international_sales = data[data["international shipping"] == "Yes"]["total sales"].sum()
# Display total international sales
st.subheader(f"Total International Sales: ${total_international_sales:}")

# Display subheader for total international sales over the months
st.subheader("Total International Sales Over the Months")
# Calculate total international sales per month
total_international_sales_per_month = data[data["international shipping"] == "Yes"].groupby(data["order date"].dt.to_period("Y"))["total sales"].sum()
total_international_sales_per_month.index = total_international_sales_per_month.index.to_timestamp()

# Display data editor for total international sales per month
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

# Calculate quantity of international sales
total_national_shipping = data[data["international shipping"] == "Yes"]["international shipping"].count()
# Display quantity of international sales
st.subheader(f"Qty International Sales: {total_national_shipping}")

# Calculate total national sales
total_national_sales = data[data["international shipping"] == "No"]["total sales"].sum()
# Display total national sales
st.subheader(f"Total National Sales: ${total_national_sales:}")

# Calculate quantity of national sales
total_national_shipping = data[data["international shipping"] == "No"]["international shipping"].count()
# Display quantity of national sales
st.subheader(f"Qty National Sales: {total_national_shipping}")

# Calculate quantity of products sold
qty_sales = data["quantity"].sum()
# Display quantity of products sold
st.subheader(f"Qty Products Sold: {qty_sales:}")

# Calculate average rating
average_rating = data["rating"].mean()
# Display average rating
st.subheader(f"Average Rating: {average_rating:.2f}")

# Calculate quantity of ratings
qty_average_rating = data["rating"].count()
# Display quantity of ratings
st.subheader(f"Qty Rating: {qty_average_rating:}")

# Checkbox to show raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# Display subheader for data visualization
st.subheader("Data Visualization")
# Display histogram
st.write("Histogram")
# Calculate histogram values for order date month
hist_values = np.histogram(data["order date"].dt.month, bins=12, range=(1, 13))[0]
# Display bar chart for histogram values
st.bar_chart(hist_values)

# Display subheader for most and least popular products
st.subheader("Most and Least Popular Products")
# Group by product id and sum the total sales
product_sales = data.groupby("product id")["total sales"].sum()
# Sort the product sales in descending order
sorted_product_sales = product_sales.sort_values(ascending=True)
# Display the horizontal bar chart
st.bar_chart(sorted_product_sales)

# Slider to filter data by month
month_filter = st.slider("Month", 1, 12, 7)
# Filter data by selected month
filtered_data = data[data[DATA_COLUMN].dt.month == month_filter]

# Display subheader for map
st.subheader("Map for month {}:".format(month_filter))
# Check if latitude and longitude columns exist
if 'latitude' in filtered_data.columns and 'longitude' in filtered_data.columns:
    # Convert latitude and longitude columns to float
    filtered_data['latitude'] = filtered_data['latitude'].str.replace(',', '').astype(float)
    filtered_data['longitude'] = filtered_data['longitude'].str.replace(',', '').astype(float)
    # Display map
    st.map(filtered_data)
else:
    # Display message if no latitude and longitude data available
    st.write("No latitude and longitude data available for mapping.")
