import streamlit as st
import pandas as pd
import plotly.express as px
from utilities.my_sql_operations import MySQLOperations

# Fetch data
sqlops = MySQLOperations()
df = sqlops.fetch_output_data('combined_multi_objective_fleet_allocation_eval')

# Streamlit page configuration
# st.set_page_config(layout="wide")
# st.markdown("# <span style='color: #FF5722;'>Fleet Report</span>", unsafe_allow_html=True)
# Remove extra space above the title
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)
with col1:    
    st.title("Analytics Dashboard", anchor=False)
with col2:
    year = st.selectbox("Year", df['Operating Year'].unique())
    
df_filtered = df[df['Operating Year']== int(year)]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cost", f"{df_filtered['Total_Cost'].sum():,.2f}", border=True)
col2.metric("Total Carbon Emissions", f"{df_filtered['Total_CE'].sum():,.2f}", border=True)

df_grouped = df_filtered.groupby(['size', 'Distance_demand'])['DemandFulfillment'].sum().reset_index()
col3.metric("Demand Fulfillment", f"{df_grouped['DemandFulfillment'].mean()*100:.2f}%", border=True)

col4.metric("Utilization Percentage", f"{df_filtered['Utilization'].mean():.2f}%", border=True)


fuel_demand = df_filtered.groupby("fuel")["demand"].sum().reset_index()
fig1 = px.pie(fuel_demand, values='demand', names='fuel', hole=0.6, title='Fuel by Demand Fulfillment')

# Total Cost & Carbon by Fuel
fuel_metrics = df_filtered.groupby("fuel")[['Total_Cost', 'Total_CE']].sum().reset_index()
fig2 = px.bar(fuel_metrics, x="fuel", y=['Total_Cost', 'Total_CE'], barmode='group', title='Total Cost & Carbon by Fuel')

# Fuel by Vehicles Allocated
fuel_vehicles = df_filtered.groupby("fuel")["No_of_vehicles"].sum().reset_index()
fig3 = px.pie(fuel_vehicles, values='No_of_vehicles', names='fuel', hole=0.6, title='Fuel by Vehicles Allocated')

# Total Distance by Fuel Type
distance_fuel = df_filtered.groupby("fuel")["demand"].sum().reset_index()
fig4 = px.bar(distance_fuel, x="fuel", y="demand", title="Total Distance by Fuel", color="fuel")

# Distribution of Total Cost & Carbon Emissions
# fig5 = px.scatter(df_filtered, x="Total_Cost", y="Total_CE", size="Distance_demand", title="Distribution of Total Cost & Total CE")

# Layout
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
col3.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

col2.plotly_chart(fig4, use_container_width=True)

# st.plotly_chart(fig5, use_container_width=True)
