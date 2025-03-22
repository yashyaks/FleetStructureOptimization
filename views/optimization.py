import streamlit as st
import time
import pandas as pd
import base64
from utilities.my_sql_operations import MySQLOperations
from main_tradeoff_topsis import main

# Function to fetch data from SQL database
# def fetch_data(years):
#     conn = sqlite3.connect("database.db")  # Update with your database connection
#     query = "SELECT * FROM fleet_data WHERE year IN ({})".format(",".join("?" * len(years)))
#     df = pd.read_sql_query(query, conn, params=years)
#     conn.close()
#     return df

# Function to create custom animation
# def get_flowchart_gif():
#     file_path = "flowchart.gif"  # Replace with actual path to your GIF
#     with open(file_path, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode("utf-8")
sqlops = MySQLOperations()
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

# UI Layout
st.title("Algorithm Parameter Tuning")

# Info button with popup
if "help_popup" not in st.session_state:
    st.session_state.help_popup = True

if st.session_state.help_popup:
    with st.popover("ℹ️ Help"):
        st.write("Use the tabs to configure parameters for the algorithm. Adjust sliders and text fields as needed. Click 'Run Algorithm' to execute and display results.")
        if st.button("Close"):
            st.session_state.help_popup = False
            
# Tabs for parameter selection
tabs = st.tabs(["Graphical", "Manual Config"])
with tabs[0]:
    # Objective selection
    task_type = st.radio("Select Optimization Type", ["Multiobjective", "Single Objective"], horizontal=True)

    # Tabs for parameter selection
    if task_type == "Multiobjective":
        col1, col2 = st.columns(2)
        with col1:
            cost_weight = st.slider("Cost Weight", 0.1, 0.9, 0.5)
            carbon_emissions_weight = st.slider("Carbon Emissions Weight", 0.1, 0.9, 0.5)
            parallel = st.checkbox("Enable Parallel Execution")
        with col2:
            prev_years = st.number_input("Previous Years", min_value=1, value=3)
            generations = st.number_input("Generations", min_value=1, value=50)
            population_size = st.number_input("Population Size", min_value=1, value=100)
            
    elif task_type == "Single Objective":
        objective = st.radio("Optimization Goal", ["Cost", "Carbon Emissions"], horizontal=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            prev_years = st.number_input("Previous Years", min_value=1, value=3)
        with col2:
            generations = st.number_input("Generations", min_value=1, value=50)
        with col3:
            population_size = st.number_input("Population Size", min_value=1, value=100)
        parallel = st.checkbox("Enable Parallel Execution")

        
with tabs[1]:
    param3 = st.text_area("Advanced Parameter")
    

# Run button
if st.button("Run Algorithm"):
    st.markdown("### Running Algorithm...")
    # gif_base64 = get_flowchart_gif()
    # st.markdown(
    #     f'<img src="data:image/gif;base64,{gif_base64}" width="500">',
    #     unsafe_allow_html=True
    # )
    # main()
    st.success("Algorithm Completed!")

    # Fetching and displaying data
    years = st.multiselect("Select Years", options=["2023", "2024", "2025"], default=["2023"])
    if years:
        df = sqlops.fetch_input_data('cost_profiles')
        st.dataframe(df)