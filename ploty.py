
import streamlit as st  
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple

# Define constants for data column and data URL
DATA_COLUMN = "order date"
DATA_URL = "data/merchandise-sales.csv"

# Function to load data with caching to improve performance
#@st.cache
@st.cache_resource
def load_data(nrows):
    # Read the CSV file
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # Convert column names to lowercase
    lower = lambda x: x.lower()
    data.rename(lower, axis='columns', inplace=True)
    # Convert the order date column to datetime
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
    # Rename 'order location' column to 'location'
    data.rename(columns={'order location': 'location', 'product id': 'product', 'product category':'category', 'buyer gender':'gender','buyer age':'age'}, inplace=True)
    # Convert latitude and longitude columns to float
    # Replace commas with dots in latitude and longitude columns
    data['latitude'] = data['latitude'].str.replace(',', '.').astype(float)
    data['longitude'] = data['longitude'].str.replace(',', '.').astype(float)
    qty_total_sales = data["total sales"].count()
    return data


def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)
set_page_config()


# Load data with a limit of 1000 rows
df = load_data(5000)
# Get unique locations for the filter
labels = df.location.unique().tolist()

# Get unique products for the filter
labelsprod = df['product'].unique().tolist()

# Get unique products for the filter
labelsgend = df["gender"].unique().tolist()

labelscat = df["category"].unique().tolist()



#KPISSSSSSSSSSSSSSSSSSSSSSSS
# Calculate total sales
total_sales = df["total sales"].sum()
# Calculate total international sales
total_international_sales = df[df["international shipping"] == "Yes"]["total sales"].sum()
# Calculate total national sales
total_national_sales = df[df["international shipping"] == "No"]["total sales"].sum()
# Calculate quantity of international sales
total_international_shipping = df[df["international shipping"] == "Yes"]["international shipping"].count()
# Calculate quantity of national sales
total_national_shipping = df[df["international shipping"] == "No"]["international shipping"].count()

# Define KPI values and names
kpis = [
    (f"${total_sales:,.2f}", "5%"),
    (f"${total_international_sales:,.2f}", "-4%"),
    (f"${total_national_sales:,.2f}", "7%"),
    (total_international_shipping, "-3%"),
    (total_national_shipping, "4%")
]
kpi_names = [
    "Total Sales",
    "Total International Sales",
    "Total National Sales",
    "Qty International Sales",
    "Qty National Sales"
]

def display_kpi_metrics(kpis: List[Tuple[str, str]], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, (kpi_value, delta))) in enumerate(zip(st.columns(5), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value, delta=delta)

# Display KPI metrics
display_kpi_metrics(kpis, kpi_names)



# Sidebar filters
st.sidebar.title("Filters")
info_sidebar = st.sidebar.empty()



# Table placeholder in the sidebar
st.sidebar.subheader("Table")
table = st.sidebar.empty()

# Year filter
st.sidebar.title("Year")
year_filter = st.sidebar.slider("Year", 2023, 2024, 2024)

st.sidebar.title("Buyer Age")
age_filter = st.sidebar.slider("Age", 18, 35)

# Product filter
# Product filter
label_prod = st.sidebar.multiselect("Product", labelsprod, default=labelsprod)
label_cat = st.sidebar.multiselect("Category", labelscat, default=labelscat)
label_gen = st.sidebar.multiselect("Gender", labelsgend, default=labelsgend)

# Location filter
label_filter = st.sidebar.multiselect("Location", labels, default=labels)

# Filter the dataframe based on the selected year, products, and locations
filtered_df = df[(df[DATA_COLUMN].dt.year == year_filter) & 
                 (df["product"].isin(label_prod)) & 
                 (df["location"].isin(label_filter))& 
                 (df["category"].isin(label_cat))& 
                 (df["gender"].isin(label_gen))]

# Display the number of rows loaded after filtering
info_sidebar.info("{} Data loaded.".format(filtered_df.shape[0], year_filter))
# Display the filtered dataframe in the sidebar
table.dataframe(filtered_df)




# Sidebar section for KPIs
st.sidebar.markdown("##Key Performance Indicators")

# Main section of the app
st.title("Merchandise Sales")
st.markdown("### Data Sample")
# Display the first few rows of the filtered dataframe
st.write(filtered_df.head())
st.markdown("### Profiling")
st.write(filtered_df.describe())



# Option to show raw data of the filtered dataframe
st.markdown("### All data")
st.markdown(f'''
            Merchant Sales Data for ***{",".join(label_filter)}*** 
            in the year of ***{year_filter}***.
            ''')
if table.checkbox("Show Raw Data"):
    st.write(filtered_df)

#map
st.subheader("Sales Map")  
# Create a scatter plot of the filtered dataframe
fig = px.scatter_geo(filtered_df, lat="latitude", lon="longitude", color="total sales", 
                     hover_name="location", size="total sales", 
                     projection="natural earth", title="Qty of Sales by Location")
st.plotly_chart(fig)


