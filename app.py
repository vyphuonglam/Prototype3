import streamlit as st
from streamlit_option_menu import option_menu
import feature1
import feature2
import feature3

# Menu
st.image("AquaTech-removebg-preview.png", width=250)  # Increase image width for prominence
selected = option_menu(
    menu_title="",
    options=["Water Testing Kit Locator", "Water Quality Testing", "Water Testing Guide"],
    icons=["", "", ""],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "width": "100%", "background-color": "#247BA0"},
        "icon": {"color": "white", "font-size": "24px"},  # Increase icon font size
        "nav-link": {"color": "white", "font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#006494"},
        "nav-link-selected": {"background-color": "#006494"},
    }
)

# Custom CSS for select boxes
st.markdown(
    """
    <style>
    /* Style for the main select box container */
    div[data-baseweb="select"] > div {
        font-size: 1.25rem;  /* Increase font size */
        background-color: #E8F1F2 !important;  /* Light background color for visibility */
        color: #000000 !important;  /* Ensure text is black for contrast */
        padding: 0.5rem;  /* Add some padding */
    }
    
    /* Style for the dropdown menu options */
    div[data-baseweb="select"] ul {
        background-color: #E8F1F2 !important;  /* Dropdown options background */
        color: #000000 !important;  /* Dropdown text color */
    }
    
    /* Style for the selected option in the dropdown */
    div[data-baseweb="select"] span {
        color: #000000 !important;  /* Selected option text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render the selected page
if selected == "Water Testing Kit Locator":
    feature3.app()
elif selected == "Water Quality Testing":
    feature1.app()
elif selected == "Water Testing Guide":
    feature2.app()
