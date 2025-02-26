import pydeck
import streamlit as st  
import pandas as pd
import pydeck as pdk

# Define constants for data column and data URL
DATA_COLUMN = "order date"
DATA_URL = "data/merchandise-sales.csv"

# Function to load data with caching to improve performance
#@st.cache
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
    return data

# Load data with a limit of 1000 rows
df = load_data(5000)
# Get unique locations for the filter
labels = df.location.unique().tolist()

# Get unique products for the filter
labelsprod = df['product'].unique().tolist()

# Get unique products for the filter
labelsgend = df["gender"].unique().tolist()

labelscat = df["category"].unique().tolist()



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
label_prod = st.sidebar.multiselect("Product", labelsprod, default=["BF1548"])

# Location filter
label_filter = st.sidebar.multiselect("Location", labels, default=["Sydney", "Toronto"])

label_cat = st.sidebar.multiselect("Category", labelscat, default=labelscat)

label_gen = st.sidebar.multiselect("Gender", labelsgend, default=labelsgend)

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

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=36.18811,
        longitude=-115.176468,
        zoom=1,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            radius=1000,
            get_fill_color=[255, 140, 0, 140],
            get_line_color=[0, 0, 0],
            auto_highlight=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))




st.map(filtered_df)
