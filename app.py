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

#############
#File upload#
# with st.sidebar:
#    st.title("Configuration")
#    uploaded_file = st.file_uploader("Choose a file")
#
#if uploaded_file is None:
#    st.info("Please upload a file")
#    st.stop()
#
#df = load_data(uploaded_file)

with st.expander("Show Data Preview"):
    data = load_data()
    st.dataframe(data.iloc[:, :-1],use_container_width=True
                 #,column_config={
                     #"Order Date": st.column_config.NumberColumn(format="%d"),}
                 )


    c1, c2 = st.columns((1,2))

    c3, c4, c5 = st.columns((1,2,2))

    c6, c7, c8 = st.columns((1,1,1))


    # Convert 'Order Date' to datetime
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN], format='%d/%m/%Y')

    # Group by 'Product Category' and resample by month to get the sum of 'Total Sales'
    sales_by_location = data.groupby('Product Category').resample('ME', on=DATA_COLUMN)['Total Sales'].sum().reset_index()

    # Plot the bar chart
    c1.bar_chart(sales_by_location.pivot(index=DATA_COLUMN, columns='Product Category', values='Total Sales'))



    # Group by 'Product Category' and resample by month to get the sum of 'Total Sales'
    sales_by_location = data.groupby('Product Category').resample('ME', on=DATA_COLUMN)['Total Sales'].sum().reset_index()

    # Plot the line chart
    c2.line_chart(sales_by_location.pivot(index=DATA_COLUMN, columns='Product Category', values='Total Sales'))


    # Group by 'Product Category' and resample by month to get the sum of 'Total Sales'
    # Sum of 'Total Sales' by 'Product Category'
    total_sales_by_category = data.groupby('Product Category')['Total Sales'].sum()

    # Plot the pie chart
    st.write("### Total Sales by Product Category")
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
    st.write("### How Shipping Charges Impact Sales")
    fig = px.bar(total_shipping_charges, x='Total Shipping Charges', y='Shipping Charges', orientation='h', title="How Shipping Charges Impact Sales", text='Total Shipping Charges')
    fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showticklabels=False)
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_yaxes(type='category')  # Ensure y-axis shows unique Shipping Charges values
    c4.plotly_chart(fig)

    # Plot the bar chart
    st.write("### Total Sales by Product ID")
    # Highlight the most and least popular products
    total_sales_by_product['color'] = 'blue'
    total_sales_by_product.loc[total_sales_by_product['Total Sales'].idxmax(), 'color'] = 'green'
    total_sales_by_product.loc[total_sales_by_product['Total Sales'].idxmin(), 'color'] = 'red'

    fig = px.bar(total_sales_by_product, x='Total Sales', y='Product ID', orientation='h', color='color', title="Total Sales by Product ID", text='Total Sales', color_discrete_map={'green': 'green', 'red': 'red', 'blue': 'blue'})
    fig.update_layout(xaxis_title='', yaxis_title='')
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    c5.plotly_chart(fig)


    # Plot the bar chart
    st.write("### Total Sales by Locations")
    fig = px.bar(total_sales_locat, x='Total Sales', y='Order Location', orientation='h', title="Total Sales by Location", text='Total Sales')
    fig.update_layout(xaxis_title='', yaxis_title='', height=(fig.layout.height or 400) * 1.5)
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', textfont_size=14)
    c6.plotly_chart(fig)


    # Calculate the average sales price by product
    avg_sales_price_by_product = data.groupby('Product ID')['Sales Price'].mean().reset_index()

    # Merge the total sales and average sales price dataframes
    total_sales_with_avg_price = pd.merge(total_sales_by_product, avg_sales_price_by_product, on='Product ID')

    # Plot the scatter plot
    st.write("### Total Sales vs. Average Sales Price by Product ID")
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
    st.write("### Sales by Buyer Age Group and Gender")
    fig = px.bar(total_sales_by_age_gender, x='Total Sales', y='Age Group', color='Buyer Gender', orientation='h', barmode='relative', title="", text='Total Sales', color_discrete_map={'Female': 'pink', 'Male': 'blue'})
    fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showticklabels=False, legend=dict(title=None, orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.1))  # Move legend to the top
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    c8.plotly_chart(fig)



   
    # Plot the bar chart
    st.write("### Total Sales by Buyer Age Group and Gender")
    fig = px.bar(total_sales_by_age_gender, x='Age Group', y='Total Sales', color='Buyer Gender', barmode='group', title="Total Sales by Buyer Age Group and Gender", text='Total Sales', color_discrete_map={'Female': 'pink', 'Male': 'orange'})
    fig.update_layout(xaxis_title='Age Group', yaxis_title='Total Sales')
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    st.plotly_chart(fig)