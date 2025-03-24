import streamlit as st
import time
import pandas as pd
from utilities.my_sql_operations import MySQLOperations
from main_tradeoff_topsis import optimization

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

    if task_type == "Multiobjective":
        col1, col2 = st.columns(2)
        with col1:
            # Initialize session state
            if "cost_weight" not in st.session_state:
                st.session_state.cost_weight = 0.5
            if "carbon_emissions_weight" not in st.session_state:
                st.session_state.carbon_emissions_weight = 1 - st.session_state.cost_weight

            # Function to update cost weight
            def update_cost():
                st.session_state.carbon_emissions_weight = 1 - st.session_state.cost_weight

            # Function to update carbon emissions weight
            def update_carbon():
                st.session_state.cost_weight = 1 - st.session_state.carbon_emissions_weight

            # Sliders with dynamic updates
            cost_weight = st.slider("Cost Weight", 0.1, 0.9, key="cost_weight", on_change=update_cost)
            carbon_emissions_weight = st.slider("Carbon Emissions Weight", 0.1, 0.9, key="carbon_emissions_weight", on_change=update_carbon)


            # cost_weight = st.slider("Cost Weight", 0.1, 0.9, 0.5)
            # carbon_emissions_weight = st.slider("Carbon Emissions Weight", 0.1, 0.9, 0.5)
            parallel = st.checkbox("Enable Parallel Execution")
        with col2:
            prev_years = st.number_input("Previous Years", min_value=1, value=7)
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
        cost_weight, carbon_emissions_weight = (1, 0) if objective == "Cost" else (0, 1)

with tabs[1]:
    param3 = st.text_area("Advanced Parameter")

# Initialize session state for output data
if "df_output" not in st.session_state:
    st.session_state.df_output = None
if "success_message" not in st.session_state:
    st.session_state.success_message = None


# Function to display loading modal
@st.dialog("Running Algorithm...", width="small")
def show_loading():
    st.image("assets/loading.gif", use_container_width=True)
    st.write("Usually takes upto 150 secs")
def run_algorithm():
    show_loading()  # Open modal with GIF
    st.markdown("### Running Algorithm")
    query = """
        SELECT 
        MIN(year) AS min_value,
        MAX(year) AS max_value
        FROM demand;    
    """
    years = sqlops.fetch_data(query)
    min_year, max_year = years[0][0]
    st.session_state.min_year = min_year
    st.session_state.max_year = max_year

    start_time = time.time()  # Start timer

    # Run your algorithm
    optimization(cost_weight, carbon_emissions_weight, generations, population_size, prev_years, min_year, max_year)
    # time.sleep(20)

    execution_time = time.time() - start_time  # Calculate duration

    st.session_state.df_output = sqlops.fetch_output_data('combined_multi_objective_fleet_allocation_eval')
    st.session_state.success_message = f"Algorithm Completed in {execution_time:.2f} seconds!"

    st.rerun()  # Close modal after execution

    st.success(f"Algorithm Completed in {execution_time:.2f} seconds!")

# Run Algorithm Button
if st.button("Run Algorithm"):
    run_algorithm()

# Display success message after rerun
if st.session_state.success_message:
    st.success(st.session_state.success_message)
    st.session_state.success_message = None  # Reset message after displaying

# Check if output data exists
if st.session_state.df_output is not None:
    year = st.selectbox("Select Year", options=list(range(st.session_state.min_year, st.session_state.max_year + 1)), index=0)

    # Filter and display the DataFrame
    df_filtered = st.session_state.df_output[st.session_state.df_output['Operating Year'] == int(year)]
    st.dataframe(df_filtered)
