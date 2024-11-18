import streamlit as st
from streamlit_option_menu import option_menu
import feature1
import feature2
import feature3

st.markdown(
    """
    <style>
    /* Override Streamlit's default body styling */
    .stApp {
        background: linear-gradient(to bottom, #E8F1F2 0%, #1B98E0 40%, #247BA0 60%, #006494 100%);
        height: 100vh;
        margin: 0;
        padding: 0;
    }
     /* Make the option-menu container seamless */
    .nav-container {
        margin: 0 auto;
        padding: 0;
        width: 100%;
        border-radius: 0px; /* Remove all rounded corners */
        background-color: transparent; /* Same as the gradient section */
        box-shadow: none; /* Avoid unnecessary shadows */
        overflow: hidden; /* Prevent any overflow issues */
    }

    /* Option menu navigation links styling */
    .nav-link {
        color: white !important; /* Text color */
        font-size: 20px !important; /* Font size */
        text-align: center !important; /* Center align */
        margin: 0 !important; /* No extra gaps */
        --hover-color: #006494; /* Hover color */
    }

    /* Active/selected menu item styling */
    .nav-link-selected {
        background-color: #006494 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("AquaTech-removebg-preview.png", width=250)  # Increase image width for prominence
selected = option_menu(
    menu_title="",
    options=["Water Testing Kit Locator", "Water Quality Analyzer", "Water Testing Guide"],
    icons=["", "", ""],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "width": "100%", "background-color": "#247BA0", "border-radius": "0px", "margin": "0"},
        "icon": {"color": "white", "font-size": "24px"},  # Increase icon font size
        "nav-link": {"color": "white", "font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#006494", "border-radius": "0px"},
        "nav-link-selected": {"background-color": "#006494"},
    }
)

# Render the selected page
if selected == "Water Testing Kit Locator":
    feature3.app()
elif selected == "Water Quality Analyzer":
    feature1.app()
elif selected == "Water Testing Guide":
    feature2.app()
