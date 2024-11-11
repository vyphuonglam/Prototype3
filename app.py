import streamlit as st
from streamlit_option_menu import option_menu
import M4_Feature_1
import feature2
import feature3




# Menu
st.image("AquaTech-removebg-preview.png", width=200)
selected = option_menu(
    menu_title="",
    options=["Water Testing Information Hub", "Water Quality Testing", "WATER TESTING GUIDE"],
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



# Render the selected page
if selected == "Water Testing Information Hub":
    feature3.app()
elif selected == "Water Quality Testing":
    M4_Feature_1.app()
elif selected == "WATER TESTING GUIDE":
    feature2.app()