import streamlit as st  
import pandas as pd
import plotly.express as px
from typing import List, Tuple
import plotly as py

# Define constants for data column and data URL
DATA_COLUMN = "Order Date"
DATA_URL = "data/merchandise-sales.csv"

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
  #  initial_sidebar_state="expanded",
)
st.title("Sales Dashboard")
st.markdown("Welcome to the Sales Dashboard! Here you can find insights about the sales data.")





@st.cache_resource
def load_data():
    data = pd.read_csv(DATA_URL)
    
    return data

# Load data
data = load_data()


st.write(f"Data loaded: {data.shape[0]} rows")

st.subheader("Silver Data Sample")
# Display first few rows of data
st.write(data.head())
# Display subheader for profiling
st.subheader("Profiling")
# Display data description
st.write(data.describe().iloc[2:])



if st.checkbox("Show raw data"):
   st.subheader("Bronze Data")    
   st.dataframe(data.iloc[:, :-1],use_container_width=True)

with st.expander("Dashboard"):
    st.subheader("Gold Data")  
    #st.write(data)

####### KPIs ########################
    kpi1, kpi2, kpi4, kpi5, kpi6, kpi7 = st.columns(6)
    #= st.columns(3)

    with kpi1:
        # Calculate the sum of total sales
        total_sales = data['Total Sales'].sum()
        # Calculate the total sales of the last month
        last_month_sales = data[data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1))]['Total Sales'].sum()
        # Calculate the percentage of the total sales of the last month
        delta_percentage = (last_month_sales / total_sales) * 100
        # Display the KPI using st.metric
        st.metric(label="Total Sales", value=f"${total_sales:,.0f}", delta=f"{delta_percentage:.2f}%")

    with kpi2:
        # Calculate the sum of total international sales where international shipping is 'Yes'
        total_international_sales = data[data['International Shipping'] == 'Yes']['Total Sales'].sum()
        # Calculate the total international sales of the last month
        last_month_international_sales = data[(data['International Shipping'] == 'Yes') & (data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1)))]['Total Sales'].sum()
        # Calculate the percentage of the total international sales of the last month
        delta_international_percentage = (last_month_international_sales / total_international_sales) * 100
        # Display the KPI using st.metric
        st.metric(label="Total International Sales", value=f"${total_international_sales:,.0f}", delta=f"{delta_international_percentage:.2f}%")

    with kpi4:
        # Calculate the sum of total shipping charges
        total_shipping_charges = data['Shipping Charges'].sum()
        # Calculate the total shipping charges of the last month
        last_month_shipping_charges = data[data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1))]['Shipping Charges'].sum()
        # Calculate the percentage of the total shipping charges of the last month
        delta_shipping_percentage = (last_month_shipping_charges / total_shipping_charges) * 100
        # Display the KPI using st.metric
        st.metric(label="Total Shipping Charges", value=f"${total_shipping_charges:,.0f}", delta=f"{delta_shipping_percentage:.2f}%")

    with kpi5:
        # Calculate the sum of Order IDs
        total_order_ids = data['Order ID'].nunique()
        # Calculate the total Order IDs of the last month
        last_month_order_ids = data[data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1))]['Order ID'].nunique()
        # Calculate the percentage of the total Order IDs of the last month
        delta_order_ids_percentage = (last_month_order_ids / total_order_ids) * 100
        # Display the KPI using st.metric
        st.metric(label="Total Order IDs", value=f"{total_order_ids:,}", delta=f"{delta_order_ids_percentage:.2f}%")

    with kpi6:
        # Calculate the sum of total quantity
        total_quantity = data['Quantity'].sum()
        # Calculate the total quantity of the last month
        last_month_quantity = data[data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1))]['Quantity'].sum()
        # Calculate the percentage of the total quantity of the last month
        delta_quantity_percentage = (last_month_quantity / total_quantity) * 100
        # Display the KPI using st.metric
        st.metric(label="Total Quantity", value=f"{total_quantity:,}", delta=f"{delta_quantity_percentage:.2f}%")

    with kpi7:
        # Calculate the average rating
        avg_rating = data['Rating'].mean()
        # Calculate the average rating of the last month
        last_month_avg_rating = data[data[DATA_COLUMN] >= (data[DATA_COLUMN].max() - pd.DateOffset(months=1))]['Rating'].mean()
        # Calculate the percentage of the average rating of the last month
        delta_rating_percentage = (last_month_avg_rating / avg_rating) * 100
        # Display the KPI using st.metric
        st.metric(label="Average Rating", value=f"{avg_rating:.2f}", delta=f"{delta_rating_percentage:.2f}%")
    


    c1, c2 = st.columns((2,1))
    c3, c4, c5 = st.columns((1,2,2))
    c6, c7, c8 = st.columns((1,1,1))


    # Convert 'Order Date' to datetime
    # Group by 'Order Date' to get the sum of 'Total Sales'
    sales_over_time = data.resample('ME', on=DATA_COLUMN)['Total Sales'].sum().reset_index()

    # Calculate month-over-month percentage change
    sales_over_time['MoM Change'] = sales_over_time['Total Sales'].pct_change() * 100

    # Format the percentage change for display
    sales_over_time['MoM Change'] = sales_over_time['MoM Change'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")

    # Define a function to color the percentage change
    def color_mom_change(val):
        if val == "N/A":
            return val
        elif float(val[:-1]) > 0:
            return f"<span style='color:green'>{val}</span>"
        else:
            return f"<span style='color:red'>{val}</span>"

    # Apply the color function to the 'MoM Change' column
    sales_over_time['MoM Change'] = sales_over_time['MoM Change'].apply(color_mom_change)

    # Calculate the average total sales
    avg_total_sales = sales_over_time['Total Sales'].mean()

    # Abbreviate the average total sales
    avg_total_sales_abbr = f"{avg_total_sales / 1000:.1f}K"

    # Format the 'Order Date' to use month abbreviation names and last 2 years digits
    sales_over_time[DATA_COLUMN] = sales_over_time[DATA_COLUMN].dt.strftime('%b %y')

    # Plot the bar chart with title
    fig = px.bar(sales_over_time, x=DATA_COLUMN, y='Total Sales', title="Total Sales Over Time", text='Total Sales')
    # Add a dotted line for the average total sales
    fig.add_shape(
        type="line",
        x0=sales_over_time[DATA_COLUMN].min(),
        x1=sales_over_time[DATA_COLUMN].max(),
        y0=avg_total_sales,
        y1=avg_total_sales,
        line=dict(color="RoyalBlue", width=2, dash="dot"),
    )
    # Add annotation for the average total sales
    fig.add_annotation(
        x=sales_over_time[DATA_COLUMN].max(),
        y=avg_total_sales,
        text=f"Avg: ${avg_total_sales_abbr}",
        showarrow=False,
        font=dict(color="RoyalBlue", size=12),
        align="right",
        xanchor="right",
        yanchor="bottom"
    )

    # Update the layout and traces to include the percentage change
    fig.update_layout(xaxis_title='', yaxis_title='')
    fig.update_traces(marker=dict(line=dict(width=0.5)), texttemplate='%{customdata[0]}', textposition='outside', customdata=sales_over_time[['MoM Change']])
    # Render the chart with HTML formatting for the custom data
    c1.plotly_chart(fig, use_container_width=True)



    # Group by 'Product Category' and resample by month to get the sum of 'Total Sales'
    #sales_by_location = data.groupby('Product Category').resample('ME', on=DATA_COLUMN)['Total Sales'].sum().reset_index()
    # Plot the line chart
    #c4.line_chart(sales_by_location.pivot(index=DATA_COLUMN, columns='Product Category', values='Total Sales'))


    # Group by 'Product Category' and resample by month to get the sum of 'Total Sales'
    # Sum of 'Total Sales' by 'Product Category'
    total_sales_by_category = data.groupby('Product Category')['Total Sales'].sum()
    # Plot the pie chart
    #st.write("### Total Sales by Product Category")
    fig = px.pie(total_sales_by_category, values='Total Sales', names=total_sales_by_category.index, title="Total Sales by Product Category")
    c3.plotly_chart(fig)

    # Plot the bar chart
    # Sum of 'Total Sales' by 'Product ID' and sort by descending total
    total_sales_by_product = data.groupby('Product ID')['Total Sales'].sum().reset_index().sort_values(by='Total Sales', ascending=True)

# Sum of 'Total sales' by 'shipp' and sort by descending total
# Sum of 'Total location' by 'Product ID' and sort by descending total
    total_sales_locat = data.groupby('Order Location')['Total Sales'].sum().reset_index().sort_values(by='Total Sales', ascending=True) if 'Order Location' in data.columns else pd.DataFrame(columns=['Order Location', 'Total Sales'])

    total_shipping_charges = data.groupby('Shipping Charges')['Shipping Charges'].sum().reset_index(name='Total Shipping Charges').sort_values(by='Total Shipping Charges', ascending=False)

    # Plot the bar chart
    #st.write("### How Shipping Charges Impact Sales")
    total_shipping_charges = total_shipping_charges.sort_values(by='Shipping Charges', ascending=False)
    fig = px.bar(total_shipping_charges, x='Total Shipping Charges', y='Shipping Charges', orientation='h', title="How Shipping Charges Impact Sales", text='Total Shipping Charges')
    fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showticklabels=False)
    fig.update_traces(texttemplate='$ %{text:.0f}', textposition='outside')
    fig.update_yaxes(type='category')  # Ensure y-axis shows unique Shipping Charges values
    c8.plotly_chart(fig)


    # Sum of 'Total Sales' and 'Quantity' by 'Product ID' and sort by descending total sales
    total_sales_by_product = data.groupby('Product ID').agg({'Total Sales': 'sum', 'Quantity': 'sum'}).reset_index().sort_values(by='Total Sales', ascending=True)
    # Plot the bar chart
    #st.write("### Total Sales by Product ID")
    fig = px.bar(total_sales_by_product, x='Total Sales', y='Product ID', orientation='h', title="Total Sales by Products", text='Total Sales')
    # Add quantity as text next to total sales
    fig.update_traces(texttemplate='$ %{text:.0f} | ∑ %{customdata[0]}', textposition='outside', customdata=total_sales_by_product[['Quantity']])
    # Add quantity to the hover information
    fig.update_traces(hovertemplate='<b>%{y}</b><br>Total Sales: $%{x:.0f}<br>Quantity: %{customdata[0]}<extra></extra>')
    # Adjust layout to give more space for better visualization and reduce bar lengths
    fig.update_layout(xaxis_title='', yaxis_title='', margin=dict(l=50, r=50, t=50, b=50))
    c2.plotly_chart(fig)


    # Plot the bar chart
    #st.write("### Total Sales by Locations")
    fig = px.bar(total_sales_locat, x='Total Sales', y='Order Location', orientation='h', title="Total Sales by Location", text='Total Sales')
    fig.update_layout(xaxis_title='', yaxis_title='', height=(fig.layout.height or 400) * 1.5)
    fig.update_traces(texttemplate='$ %{text:.0f}', textposition='outside', textfont_size=14)
    c5.plotly_chart(fig)


    # Calculate the average sales price by product
    avg_sales_price_by_product = data.groupby('Product ID')['Sales Price'].mean().reset_index()
    # Merge the total sales and average sales price dataframes
    total_sales_with_avg_price = pd.merge(total_sales_by_product, avg_sales_price_by_product, on='Product ID')
    # Plot the scatter plot
    #st.write("### Total Sales vs. Average Sales Price by Product ID")
    fig = px.scatter(total_sales_with_avg_price, x='Sales Price', y='Total Sales', text='Product ID', title="Total Sales vs. Average Sales Price by Product ID")
    fig.update_traces(textposition='top center')
    c7.plotly_chart(fig)


    # Define age bins and labels
    age_bins = [18, 21, 24, 27, 30, 33, 36]
    age_labels = ['18-20', '21-23', '24-26', '27-29', '30-32', '33-35']
    # Create a new column for age segmentation
    data['Age Group'] = pd.cut(data['Buyer Age'], bins=age_bins, labels=age_labels, right=False)
     # Group by 'Age Group' and calculate the sum of 'Total Sales'
    total_sales_by_age_gender = data.groupby(['Age Group', 'Buyer Gender'])['Total Sales'].sum().reset_index()
    # Sort the total_sales_by_age_gender by 'Age Group' in ascending order
    total_sales_by_age_gender = total_sales_by_age_gender.sort_values(by='Age Group',ascending=False)
    # Create a tornado bar chart
    #st.write("### Sales by Buyer Age Group and Gender")
    fig = px.bar(total_sales_by_age_gender, x='Total Sales', y='Age Group', color='Buyer Gender', orientation='h', barmode='relative', title="", text='Total Sales', color_discrete_map={'Female': 'pink', 'Male': 'blue'})
    fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showticklabels=False, legend=dict(title=None, orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.1))  # Move legend to the top
    fig.update_traces(texttemplate='$ %{text:.0f}', textposition='outside')
    c6.plotly_chart(fig)



    #info_sidebar.info("{} Data loaded.".format(filtered_df.shape[0], year_filter))

#### MAP ###########
    data['Latitude'] = data['Latitude'].astype(str).str.replace(',', '.').astype(float)
    data['Longitude'] = data['Longitude'].astype(str).str.replace(',', '.').astype(float)

    #st.subheader("Sales Map")  
    fig = px.scatter_geo(data, lat="Latitude", lon="Longitude", color="Total Sales", 
                         hover_name="Order Location", size="Total Sales", 
                         projection="natural earth", title="Qty of Sales by Location")
    fig.update_layout(height=650)  # Increase the map size to 600
    c4.plotly_chart(fig)



