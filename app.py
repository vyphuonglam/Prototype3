import streamlit as st
from streamlit_option_menu import option_menu
import feature1
import feature2
import feature3



st.image("AquaTech-removebg-preview.png", width=250)  # Increase image width for prominence
selected = option_menu(
    menu_title="",
    options=["Water Testing Kit Locator", "Water Testing Guide", "Water Quality Analyzer"],
    icons=["", "", ""],
    menu_icon="",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "width": "100%", "background-color": "#247BA0", },
        "icon": {"color": "white", "font-size": "24px"},  # Increase icon font size
        "nav-link": {"color": "white", "font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#006494", },
        "nav-link-selected": {"background-color": "#006494"},
    }
)

# Render the selected page
if selected == "Water Testing Kit Locator":
    feature3.app()
elif selected == "Water Testing Guide":
    feature2.app()
elif selected == "Water Quality Analyzer":
    feature1.app()


