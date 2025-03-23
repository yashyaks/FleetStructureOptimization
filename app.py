import streamlit as st

st.set_page_config(page_title="Fleet Selection", page_icon="🚚", layout="wide")
hide_streamlit_style = """
<style>
    [data-testid="stDecoration"] {background: #FFFFFF;}
    div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: auto;
    }
    
    div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
    div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
        display: flex;
        align-items: center;
    }
    [data-testid="stSidebarNavLink"] {
        font-size: 20px !important;
        text-align: center;
    }
    [data-testid="stIconMaterial"] {
        font-size: 20px !important;
        text-align: center;
    }

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.logo("assets/logo.png", size="large")


p0 = st.Page(
    "views/home.py", 
    title="Home", 
    icon=":material/home:",
    default=True,
)

p1 = st.Page(
    "views/data.py", 
    title="Data", 
    icon=":material/database:",
)
p2 = st.Page(
    "views/optimization.py", 
    title="Optimization", 
    icon=":material/cognition:",
)
p3 = st.Page(
    "views/dashboard.py", 
    title="Dashboard", 
    icon=":material/analytics:",
)
pg = st.navigation(pages = [p0, p1, p2, p3])
pg.run()
