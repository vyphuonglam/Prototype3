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
        /* Change text color inside the selectbox */
        div[data-baseweb="select"] > div {
            color: white;  /* Change this to your preferred color */
        }

        /* Change background color of the selectbox dropdown options */
        div[data-baseweb="select"] > div > div {
            background-color: #247ba0; /* Background color for the dropdown */
            color: white; /* Text color for the options */
        }

        /* Style for selectbox text color (selected option) */
        div[data-baseweb="select"] > div {
            color: white;  /* Text color for selected option */
            background-color: #247BA0;  /* Background color of the selectbox */
            border-radius: 5px;
            padding: 0px;
        }

        /* Style for text_input */
        input[type="text"] {
            background-color: #247ba0;  /* Input background color */
            color: #FFFFFF;  /* Input text color */
            border: 1px solid #2b6cb0;  /* Optional: Input border color */
            border-radius: 5px;  /* Optional: Rounding the corners */
            padding: 8px;  /* Padding inside the input box */
        }

        /* Style for the placeholder "Choose an option" in the multiselect */
        div[data-baseweb="select"] .css-14jk2my {
            color: white;  /* Placeholder text color */
        }

        /* Style the st.write output boxes */
        .streamlit-expander {
            background-color: #e0f7fa;  /* Light cyan background */
            border-radius: 5px;
            padding: 10px;
            color: white;  /* Dark teal text color */
            font-weight: bold;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Optional box shadow */
        }

        /* Style other generic st.write containers */
        .css-1n76uvr {
            background-color: #e0f7fa; /* Background color */
            color: white; /* Text color */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Load the dataset
    file_path = "updated_synthetic_water_testing_data.csv"  # Update to reflect the correct file location

    # Check if the file exists and load it
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
    else:
        st.error(f"Data file not found! Expected path: {file_path}")
        return  # Exit the function if the file is not found

    # Streamlit components
    st.title("Water Quality Analyzer Hub")
    st.write("Learn about the interpretation of your water testing results! Select the water type and contaminants!")

    # Water Source Selection
    source_options = st.selectbox(
        "Select the Water Source!",
        data["Water Source"].unique()
    )

    # Contaminant Selection
    contaminants_options = st.multiselect(
        "Select the tested Contaminants!",
        ["Lead (ppb)", "Chlorine (ppm)", "Nitrates/Nitrites (ppm)", 
         "Bacteria (e.g., E. coli)", "Pesticides (ppm)", "Herbicides (ppm)"]
    )

    # Filter the dataset
    filtered_data = data[data["Water Source"] == source_options]

    # Further filter by selected contaminants
    if contaminants_options:
        filtered_data = filtered_data.dropna(subset=contaminants_options)

    # Show filtered data warning if empty
    if filtered_data.empty:
        st.warning("No data available for the selected criteria.")

    # Chatbox and analysis
    with st.form(key="water_testing_chat"):
        user_prompt = st.text_input("Input your water testing results as follows: (e.g., 'Chlorine: 5, Lead: 5')")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Safe levels for reference
            safe_levels = {
                "Lead (ppb)": 15,
                "Chlorine (ppm)": 4,
                "Nitrates/Nitrites (ppm)": 10,
                "Bacteria (e.g., E. coli)": 0,
                "Pesticides (ppm)": 3,
                "Herbicides (ppm)": 1,
            }

            # Parse user input to extract contaminant levels
            user_results = {}
            for item in user_prompt.split(","):
                key_value = item.split(":")
                if len(key_value) == 2:
                    input_name, input_value = key_value[0].strip(), key_value[1].strip()
                    # Match the input name to the exact contaminant name in contaminants_options
                    contaminant = next(
                        (c for c in contaminants_options if input_name.lower() in c.lower()), 
                        None
                    )
                    if contaminant:
                        try:
                            user_results[contaminant] = float(input_value.split()[0])  # Extract numeric value
                        except ValueError:
                            st.error(f"Invalid numeric value for {input_name}. Please enter a valid number.")

            # Prepare data for visualization
            contaminant_data = {
                "Contaminant": [],
                "Safe Level": [],
                "User Level": []
            }

            for contaminant in contaminants_options:
                safe_value = safe_levels.get(contaminant, 0)
                user_value = user_results.get(contaminant, None)  # If not found, it will remain None
                if user_value is None:
                    st.warning(f"User input missing for {contaminant}. Defaulting to 0.")
                    user_value = 0  # Default to 0 if user input is missing
                contaminant_data["Contaminant"].append(contaminant)
                contaminant_data["Safe Level"].append(safe_value)
                contaminant_data["User Level"].append(user_value)

            chart_data = pd.DataFrame(contaminant_data)

            # Reshape data for multi-series bar chart
            chart_data = pd.melt(chart_data, id_vars="Contaminant", var_name="Level Type", value_name="Value")

            # Create the bar chart with altair
            st.write("Comparison of Safe Levels vs User Levels")
            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Contaminant:N", title="Contaminant", axis=alt.Axis(labelAngle=0)),  # Contaminants on X-axis
                y=alt.Y("Value:Q", title="Level (ppm or ppb)"),  # Levels on Y-axis
                color=alt.Color("Level Type:N", legend=alt.Legend(title="Level Type")),  # Separate colors for Safe/User levels
                column=alt.Column("Level Type:N", title=None, spacing=10)  # Reduce spacing for compactness
            ).properties(
                width=200,  # Width of each bar group
                height=200  # Reduce height for better fit
            )

            st.altair_chart(chart, use_container_width=False)  # Ensures it fits within the Streamlit container

            # Generate response using OpenAI
            full_prompt = f"""
            Please interpret the following water testing results:\n\n{user_prompt}
            
            Structure your response as follows:
            
            1. **Safety Assessment**: Clearly state if the result is "Safe!" or "Dangerous!".
            2. **Explanation**: Briefly explain why the result is considered safe or dangerous, referencing acceptable limits if relevant.
            3. **Next Steps**: If the result is dangerous, provide recommendations for actions the user can take to improve water safety.
            
            Additional Information:
            - Water Source: {source_options}
            - Contaminants: {', '.join(contaminants_options)}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            completion = response.choices[0].message.content

            # Highlight "Safe" and "Dangerous" with colors
            formatted_response = completion.replace("Safe!", "<span style='color:green;font-weight:bold;'>Safe</span>")
            formatted_response = completion.replace("Dangerous!", "<span style='color:red;font-weight:bold;'>Dangerous</span>")
            st.markdown(formatted_response, unsafe_allow_html=True)


