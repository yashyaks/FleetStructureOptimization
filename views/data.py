import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utilities.my_sql_operations import MySQLOperations

# Initialize SQL operations
try:
    sqlops = MySQLOperations()
except Exception as e:
    st.error(f"Error initializing database connection: {e}")
    st.stop()

st.title("Fleet Data Management & Update Tool", anchor=False)
st.markdown("Manage and update your fleet data across different tables.")
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


# Create tabs
tab1, tab2, tab3 = st.tabs(["📂 Upload New Data", "✏️ Edit Data", "📊 View Tables"])

with tab1:
    st.subheader("📂 Upload New Data")
    table_options = {"vehicles": "vehicles", "vehicles_fuels": "vehicles_fuels", "fuels": "fuels", "cost_profiles": "cost_profiles", "demand": "demand"}
    selected_table = st.selectbox("Select Table to Upload Data:", list(table_options.keys()), key="upload_table")

    uploaded_file = st.file_uploader(f"Upload CSV for {selected_table}", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = df.reset_index(drop=True)  
            
            if df.empty:
                st.warning("Uploaded file is empty. Please check your data.")
            else:
                table_name = table_options[selected_table]  # Get actual table name
                sqlops.push_input_data(df, table_name)  # Insert into the selected table
                st.success(f"✅ Data uploaded successfully to {table_name}!")
                st.rerun()  # Refresh the page
        except pd.errors.EmptyDataError:
            st.error("Uploaded CSV file is empty.")
        except pd.errors.ParserError:
            st.error("Error parsing CSV file. Ensure it is formatted correctly.")
        except Exception as e:
            st.error(f"Error inserting data into the database: {e}")

with tab2:
    st.subheader("✏️ Edit Data")
    table_options = {"vehicles": "vehicles", "vehicles_fuels": "vehicles_fuels", "fuels": "fuels", "cost_profiles": "cost_profiles", "demand": "demand"}
    edit_table = st.selectbox("Select a table to edit:", list(table_options.keys()), key="edit_table")

    if edit_table:
        table_name = table_options[edit_table]  # Get actual table name

        try:
            df = sqlops.fetch_input_data(table_name)  # Fetch table data

            if df.empty:
                st.warning(f"No data available in {edit_table}.")
            else:
                edited_df = st.data_editor(df, num_rows="dynamic")  # Editable table

                if st.button(f"💾 Save Changes to {edit_table}"):
                    try:
                        sqlops.update_table_data(table_name, edited_df)  # Update database
                        st.success(f"✅ {edit_table} table updated successfully!")
                        st.rerun()  # Refresh the page
                    except Exception as e:
                        st.error(f"Error updating {edit_table} table: {e}")

        except Exception as e:
            st.error(f"Error fetching {edit_table} table: {e}")

with tab3:
    st.subheader("📊 View Tables")
    table_options = {"vehicles": "vehicles", "vehicles_fuels": "vehicles_fuels", "fuels": "fuels", "cost_profiles": "cost_profiles", "demand": "demand"}
    view_table = st.selectbox("Select a table to view:", list(table_options.keys()), key="view_table")

    if view_table:
        table_name = table_options[view_table]  # Get actual table name

        try:
            df = sqlops.fetch_input_data(table_name)  # Fetch table data

            if df.empty:
                st.warning(f"No data available in {view_table}.")
            else:
                st.subheader(f"📊 {view_table} Table")
                st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching {view_table} table: {e}")
