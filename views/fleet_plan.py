import streamlit as st
import pandas as pd
import os
from utilities.my_sql_operations import MySQLOperations
from buysell import generate_buy_sell_use_plan

st.title("Fleet Plan", anchor=False)
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

sqlops = MySQLOperations()
df = sqlops.fetch_output_data('combined_multi_objective_fleet_allocation_eval')

connection_string = os.getenv('OUTPUT_STRING')

if df.empty:
    st.warning("No data found. Please check your database.")
else:
    years = df["Operating Year"].unique()
    selected_year = st.selectbox("Select Year", sorted(years))
    
    plan_df = generate_buy_sell_use_plan(df)
            
    engine = sqlops.create_sqlalchemy_engine(connection_string)
    plan_df.to_sql(f'fleet_plan', con=engine, if_exists='replace')
    
    filtered_plan_df = plan_df[plan_df["Operating Year"] == selected_year]
    df_filtered = df[df["Operating Year"] == selected_year]
    col1, col2 = st.columns(2)
    col1.metric("Total Cost of Vehicle Acquisition for the year", f"₹ {df_filtered['Total_Cost'].sum():,.2f}", border=True)
    col2.metric("Total Carbon Emissions for the year", f"{df_filtered['Total_CE'].sum():,.2f} kgs of CO2", border=True)

    st.subheader(f"Generated Buy, Sell, and Use Plan for {selected_year}")
    st.dataframe(filtered_plan_df, use_container_width=True)
    
    csv = plan_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Plan for all years",
        data=csv,
        file_name=f"fleet_plan.csv",
        mime="text/csv"
    )
