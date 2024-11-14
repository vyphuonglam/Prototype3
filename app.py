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

# Custom CSS for resizing and reducing spacing
st.markdown(
    """
    <style>
    /* General page styling for font size without altering color */
    .css-18e3th9 {  /* Streamlit's base container class */
        padding: 1rem 2rem;  /* Reduce padding */
    }
    .stMarkdown h1 {  /* Style for the main header */
        font-size: 3rem;  /* Increase header size */
        margin-bottom: 0.5rem;  /* Reduce bottom margin */
    }
    .stMarkdown h2, .stMarkdown h3 {  /* Style for sub-headers */
        font-size: 2rem;
        margin-bottom: 0.25rem;  /* Reduce margin below headers */
    }

    /* Select boxes styling */
    div[data-baseweb="select"] > div {
        font-size: 1.25rem;  /* Increase font size of select box */
        background-color: #E8F1F2 !important;
        padding: 0.5rem;  /* Adjust padding */
    }
    
    /* Adjust padding and margin for buttons and other elements */
    .stButton button {
        font-size: 1.2rem;  /* Increase button font size */
        padding: 0.6rem 1.2rem;  /* Adjust button padding */
        margin-top: 0.5rem;
    }
    
    /* General text size adjustment for the main content without changing color */
    .stMarkdown, .css-1v3fvcr {  /* Adjust font sizes for main content */
        font-size: 1.25rem;  /* General font size */
        line-height: 1.5;  /* Adjust line height for readability */
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
