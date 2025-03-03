import streamlit as st  
import pandas as pd
import plotly.express as px
from typing import List, Tuple

# Define constants for data column and data URL
DATA_COLUMN = "order date"
DATA_URL = "data/merchandise-sales.csv"

@st.cache_resource
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lower = lambda x: x.lower()
    data.rename(lower, axis='columns', inplace=True)
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
    data.rename(columns={'order location': 'location', 'product id': 'product', 'product category':'category', 'buyer gender':'gender','buyer age':'age'}, inplace=True)
    data['latitude'] = data['latitude'].str.replace(',', '.').astype(float)
    data['longitude'] = data['longitude'].str.replace(',', '.').astype(float)
    return data

def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

def calculate_kpis(df):
    total_sales = df["total sales"].sum()
    total_international_sales = df[df["international shipping"] == "Yes"]["total sales"].sum()
    total_national_sales = df[df["international shipping"] == "No"]["total sales"].sum()
    total_international_shipping = df[df["international shipping"] == "Yes"]["international shipping"].count()
    total_national_shipping = df[df["international shipping"] == "No"]["international shipping"].count()
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
    return kpis, kpi_names

def display_kpi_metrics(kpis: List[Tuple[str, str]], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, (kpi_value, delta))) in enumerate(zip(st.columns(5), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value, delta=delta)

def display_sidebar_filters(df):
    st.sidebar.title("Filters")
    info_sidebar = st.sidebar.empty()
    st.sidebar.subheader("Table")
    table = st.sidebar.empty()
    year_filter = st.sidebar.slider("Year", 2023, 2024, 2024)
    age_filter = st.sidebar.slider("Age", 18, 35)
    labelsprod = df['product'].unique().tolist()
    labelscat = df["category"].unique().tolist()
    labelsgend = df["gender"].unique().tolist()
    labels = df.location.unique().tolist()
    label_prod = st.sidebar.multiselect("Product", labelsprod, default=labelsprod)
    label_cat = st.sidebar.multiselect("Category", labelscat, default=labelscat)
    label_gen = st.sidebar.multiselect("Gender", labelsgend, default=labelsgend)
    label_filter = st.sidebar.multiselect("Location", labels, default=labels)
    filtered_df = df[(df[DATA_COLUMN].dt.year == year_filter) & 
                     (df["product"].isin(label_prod)) & 
                     (df["location"].isin(label_filter))& 
                     (df["category"].isin(label_cat))& 
                     (df["gender"].isin(label_gen))]
    info_sidebar.info("{} Data loaded.".format(filtered_df.shape[0], year_filter))
    table.dataframe(filtered_df)
    return filtered_df

def display_main_content(filtered_df):
    st.title("Merchandise Sales")
    st.markdown("### Data Sample")
    st.write(filtered_df.head())
    st.markdown("### Profiling")
    st.write(filtered_df.describe())
    st.markdown("### All data")
    st.markdown(f'''
                Merchant Sales Data for ***{",".join(filtered_df["location"].unique())}*** 
                in the year of ***{filtered_df[DATA_COLUMN].dt.year.unique()[0]}***.
                ''')
    if st.checkbox("Show Raw Data"):
        st.write(filtered_df)
    st.subheader("Sales Map")  
    fig = px.scatter_geo(filtered_df, lat="latitude", lon="longitude", color="total sales", 
                         hover_name="location", size="total sales", 
                         projection="natural earth", title="Qty of Sales by Location")
    st.plotly_chart(fig)

def main():
    set_page_config()
    df = load_data(5000)
    kpis, kpi_names = calculate_kpis(df)
    display_kpi_metrics(kpis, kpi_names)
    filtered_df = display_sidebar_filters(df)
    display_main_content(filtered_df)

if __name__ == "__main__":
    main()
