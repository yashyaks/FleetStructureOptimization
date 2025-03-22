import streamlit as st

st.title("About Fleet Selection Tool")

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


st.markdown(
    """
    The **Fleet Selection Tool** is designed to help optimize fleet management decisions 
    by analyzing various parameters like cost, demand, and carbon emissions. 
    
    ### Features:
    - Upload CSV data containing fleet details
    - Analyze vehicle performance metrics
    - Optimize buy/sell/use decisions for fleet management
    - Ensure compliance with carbon emission constraints
    
    This tool aims to simplify fleet decision-making and enhance efficiency.
    """
)