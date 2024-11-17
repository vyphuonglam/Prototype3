import os
import pandas as pd
import streamlit as st
import altair as alt
from openai import OpenAI

# Initialize the OpenAI client with API key from st.secrets
client = OpenAI(api_key=st.secrets["MY_API_KEY"])

# Define the app function
def app():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Custom styling (same as provided) */
        </style>
        """,
        unsafe_allow_html=True
    )

    # Load the dataset
    file_path = "updated_synthetic_water_testing_data.csv"

    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        st.error(f"Data file not found! Expected path: {file_path}")
        return

    st.title("Water Quality Analyzer Hub")
    st.write("Learn about the interpretation of your water testing results!")

    # Water Source Selection
    source_options = st.selectbox(
        "Select the Water Source!",
        ["Select Water Source"] + list(data["Water Source"].unique()),
        key="water_source_selectbox"
    )
    if source_options == "Select Water Source":
        st.warning("Please select a valid water source!")
        return

    # Contaminant Selection
    contaminants_options = st.multiselect(
        "Select the tested Contaminants!",
        ["Lead (ppb)", "Chlorine (ppm)", "Nitrates/Nitrites (ppm)", 
         "Bacteria (e.g., E. coli)", "Pesticides (ppm)", "Herbicides (ppm)"],
        key="contaminants_multiselect"
    )
    if not contaminants_options:
        st.warning("Please select at least one contaminant.")
        return

    # Filter dataset
    filtered_data = data[data["Water Source"] == source_options]
    if contaminants_options:
        filtered_data = filtered_data.dropna(subset=contaminants_options)

    if filtered_data.empty:
        st.warning("No data available for the selected criteria.")
        return

    # Chatbox for user input
    with st.form(key="water_testing_chat"):
        user_prompt = st.text_input(
            "Input your water testing results (e.g., 'Chlorine: 7, Lead: 5')",
            key="user_prompt_input"
        )
        submitted = st.form_submit_button("Submit", key="form_submit_button")

        if submitted:
            # Safe levels reference
            safe_levels = {
                "Lead (ppb)": 15,
                "Chlorine (ppm)": 4,
                "Nitrates/Nitrites (ppm)": 10,
                "Bacteria (e.g., E. coli)": 0,
                "Pesticides (ppm)": 3,
                "Herbicides (ppm)": 1,
            }

            # Parse user input
            user_results = {}
            for item in user_prompt.split(","):
                key_value = item.split(":")
                if len(key_value) == 2:
                    input_name, input_value = key_value[0].strip(), key_value[1].strip()
                    contaminant = next(
                        (c for c in contaminants_options if input_name.lower() in c.lower()), 
                        None
                    )
                    if contaminant:
                        try:
                            user_results[contaminant] = float(input_value.split()[0])
                        except ValueError:
                            st.error(f"Invalid numeric value for {input_name}.")

            # Prepare visualization data
            contaminant_data = {
                "Contaminant": [],
                "Safe Level": [],
                "User Level": []
            }
            for contaminant in contaminants_options:
                safe_value = safe_levels.get(contaminant, 0)
                user_value = user_results.get(contaminant, 0)
                contaminant_data["Contaminant"].append(contaminant)
                contaminant_data["Safe Level"].append(safe_value)
                contaminant_data["User Level"].append(user_value)

            chart_data = pd.DataFrame(contaminant_data)
            chart_data = pd.melt(chart_data, id_vars="Contaminant", var_name="Level Type", value_name="Value")

            # Display bar chart
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Contaminant:N", title="Contaminant"),
                y=alt.Y("Value:Q", title="Level (ppm or ppb)"),
                color=alt.Color("Level Type:N"),
                column=alt.Column("Level Type:N", spacing=10)
            ).properties(width=150, height=200)
            st.altair_chart(chart, use_container_width=True)

            # Generate OpenAI response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            st.markdown(response.choices[0].message.content)

# Run the app
app()
