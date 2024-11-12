import os
import pandas as pd
import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["MY_API_KEY"])

# Define the app function
def app():
    # Construct the file path using a relative path
    file_path = os.path.join(os.path.dirname(__file__), "data", "updated_synthetic_water_testing_data.csv")

    # Check if the CSV file exists before loading it
    if os.path.exists(file_path):
        # Load the CSV data
        data = pd.read_csv(file_path)
    else:
        # Display an error message in Streamlit if the file is not found
        st.error(f"Data file not found at path: {file_path}")
        data = pd.DataFrame()  # Empty DataFrame as a fallback

    # Function to get completion from OpenAI API
    def get_completion(prompt, model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content

    st.title("Water Testing Information Hub")
    st.write("Learn about interpreting water testing results! Select your water type, contaminants, and testing method!")

    # Select box for water source
    source_options = st.selectbox(
        "What type is the Water Source?",
        ["Tap water", "Filtered water", "Bottled water", "Rainwater Collection", "Well water", "Ocean water"],
    )

    # Multiselect for contaminants
    contaminants_options = st.multiselect(
        "What contaminants are you testing for?",
        ["Lead (ppb)", "Chlorine (ppm)", "Nitrates/Nitrites (ppm)", "Bacteria (e.g., E. coli)", "Pesticides (ppm)", "Herbicides (ppm)"]
    )

    # Filter the dataset based on user inputs
    filtered_data = data[(data["Water Source"] == source_options)]

    # Further filter by contaminants if specified
    if contaminants_options:
        filtered_data = filtered_data[filtered_data[contaminants_options].notna().any(axis=1)]

    # Summarize filtered data
    filtered_data_summary = filtered_data.to_dict(orient="records") if not filtered_data.empty else "No matching data found."

    # Form for submitting results
    with st.form(key="water_testing_chat"):
        # Prompt user to input water testing results
        user_prompt = st.text_input("Input your water testing results (e.g., 'Chlorine level: 7 ppm', 'Nitrate level: 5 ppm')")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Update the prompt for a structured response
            full_prompt = f"""
            Please interpret the following water testing results:\n\n{user_prompt}
            
            Structure your response as follows:
            
            1. **Safety Assessment**: Clearly state if the result is "Safe!" or "Dangerous!".
            2. **Explanation**: Briefly explain why the result is considered safe or dangerous, referencing acceptable limits if relevant.
            3. **Next Steps**: If the result is dangerous, provide recommendations for actions the user can take to improve water safety.
            
            Additional Information:
            - Water Source: {source_options}
            - Contaminants: {', '.join(contaminants_options)}
            - Data Summary: {filtered_data_summary}
            """

            # Get response from OpenAI API
            response = get_completion(full_prompt)

            # Apply color coding only in the final rendered output
            formatted_response = response.replace("Safe!", "<span style='color:green;font-weight:bold;'>Safe</span>")
            formatted_response = formatted_response.replace("Dangerous!", "<span style='color:red;font-weight:bold;'>Dangerous</span>")

            # Display the formatted response with HTML styling
            st.markdown(formatted_response, unsafe_allow_html=True)
