import streamlit as st
from streamlit_option_menu import option_menu
import feature1
import feature2
import feature3




# Menu
st.image("AquaTech-removebg-preview.png", width=200)
selected = option_menu(
    menu_title="",
    options=["Water Testing Kit Locator", "Water Quality Testing", "Water Testing Guide"],
    icons=["", "", ""],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "width": "100%", "background-color": "#247BA0"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {"color": "white", "font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#006494"},
        "nav-link-selected": {"background-color": "#006494"},
    }
)

# Custom CSS for select boxes
st.markdown(
    """
    <style>
    /* Select boxes styling */
    div[data-baseweb="select"] > div {
        background-color: #E8F1F2 !important;  /* Background color for the select box */
        color: #333333 !important;  /* Text color */
    }
    
    /* Dropdown menu options */
    div[data-baseweb="select"] > div > ul {
        background-color: #E8F1F2 !important;
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
