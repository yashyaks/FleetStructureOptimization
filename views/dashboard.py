import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utilities.my_sql_operations import MySQLOperations

# Fetch data
sqlops = MySQLOperations()
df = sqlops.fetch_output_data('combined_multi_objective_fleet_allocation_eval')
summary_df = sqlops.fetch_output_data('multiobjective_summary')

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
summary_df_filtered = summary_df[summary_df['Year']== int(year)]

# KPI Metrics
col1, col2 = st.columns(2)
col1.metric("Total Cost", f"₹ {summary_df_filtered['TotalCost'].iloc[0]}", border=True)
col2.metric("Total Carbon Emissions", f"{summary_df_filtered['TotalCarbonEmissions'].iloc[0]} kgs of CO2", border=True)

df_grouped = df_filtered.groupby(['size', 'Distance_demand'])['DemandFulfillment'].sum().reset_index()
col1, col2 = st.columns(2)
col1.metric("Demand Fulfillment", f"{df_grouped['DemandFulfillment'].mean()*100:.2f}%", border=True)

col2.metric("Utilization Percentage", f"{df_filtered['Utilization'].mean():.2f}%", border=True)


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

# df_ranked = df_filtered.pivot(index='Operating Year', columns='vehicle', values='Rank')
# fig5 = go.Figure(data=go.Heatmap(z=df_ranked.values, x=df_ranked.columns, y=df_ranked.index, colorscale='Viridis', colorbar_title='Rank'))
# fig5.update_layout(title='Best Fleet Selection (Heatmap)')

df_filtered['total_fuel_costs'] = df_filtered['fuel_costs_per_km'] * (df_filtered['DemandFulfillment'] * df_filtered['demand'])

# Group by vehicle type and sum the costs
cost_breakdown = df_filtered.groupby('vehicle')[['total_fuel_costs', 'insurance_cost', 'maintenance_cost']].sum().reset_index()

# Reshape the data for stacked bar format
cost_breakdown_melted = cost_breakdown.melt(id_vars=['vehicle'], var_name='Cost Component', value_name='Amount')

# Create a stacked bar chart
fig6 = px.bar(cost_breakdown_melted, 
              x='vehicle', 
              y='Amount', 
              color='Cost Component',
              title='Cost Breakdown by Vehicle Type',
              barmode='stack')


# Calculate total carbon emissions per vehicle type
df_filtered['total_carbon_emissions'] = df_filtered['No_of_vehicles'] * df_filtered['carbon_emissions_per_km'] * (df_filtered['DemandFulfillment'] * df_filtered['demand'])

# Group by vehicle type and sum the emissions
carbon_breakdown = df_filtered.groupby('vehicle')['total_carbon_emissions'].sum().reset_index()

# Create a bar chart
fig7 = px.bar(carbon_breakdown, 
              x='vehicle', 
              y='total_carbon_emissions', 
              title='Total Carbon Emissions by Vehicle Type', 
              labels={'total_carbon_emissions': 'Total Carbon Emissions'},
              color='vehicle')

# Distribution of Total Cost & Carbon Emissions
# fig5 = px.scatter(df_filtered, x="Total_Cost", y="Total_CE", size="Distance_demand", title="Distribution of Total Cost & Total CE")

# Layout
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
col3.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

# col1.plotly_chart(fig5, use_container_width=True)
col2.plotly_chart(fig6, use_container_width=True)
col1.plotly_chart(fig7, use_container_width=True)

# st.plotly_chart(fig5, use_container_width=True)

