import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import pydeck as pdk

# Title and subtitle
st.title("Water Testing Information Hub")
st.write("Welcome to the Water Testing Information Hub!")

# User input for zip code
zip_code = st.text_input("Enter your zip code to find the nearest water testing kit location:")

# Load Target and Walmart locations data with specified encoding
try:
    # Read the CSV files with ISO-8859-1 encoding to handle special characters
    target_locations = pd.read_csv("target.csv", encoding="ISO-8859-1")
    walmart_locations = pd.read_csv("walmartstreamlit run feature3.py.csv", encoding="ISO-8859-1")
    
    # Standardize column names for consistency
    target_locations = target_locations.rename(columns={"Address.Latitude": "latitude", "Address.Longitude": "longitude", "Name": "location_name", "Address.Street": "address"})
    walmart_locations = walmart_locations.rename(columns={"latitude": "latitude", "longitude": "longitude", "name": "location_name"})
    
    # If 'address' column is missing in Walmart data, add a placeholder address
    if 'address' not in walmart_locations.columns:
        walmart_locations['address'] = "Address not available"

     # If 'address' column is missing in Target data, add a placeholder address
    if 'address' not in target_locations.columns:
        target_locations['address'] = "Address not available"    
    
    # Concatenate Target and Walmart locations into a single DataFrame
    water_testing_locations = pd.concat([target_locations, walmart_locations], ignore_index=True)
    
except FileNotFoundError as e:
    st.error(f"Error loading store location data: {e}")
    st.stop()  # Stop further execution if files are not found
except UnicodeDecodeError as e:
    st.error(f"Encoding error loading store location data: {e}")
    st.stop()

# Button to submit zip code and display map
if st.button("Find Nearby Water Testing Kit"):
    try:
        # Initialize geolocator
        geolocator = Nominatim(user_agent="water_testing_locator")
        location = geolocator.geocode({"postalcode": zip_code, "country": "United States"})

        if location:
            st.write(f"Showing nearest water testing kit locations for zip code {zip_code}")

            # Calculate distances and filter for nearby locations (simulated within ~20 miles)
            water_testing_locations["distance"] = ((water_testing_locations["latitude"] - location.latitude) ** 2 + 
                                                   (water_testing_locations["longitude"] - location.longitude) ** 2) ** 0.5
            # Sort by distance and select the top 3 nearest locations
            nearby_locations = water_testing_locations.nsmallest(3, "distance")

            if not nearby_locations.empty:
                # Display the top 3 nearest locations with names and addresses
                st.write("Top 3 Nearest Water Testing Kit Locations:")
                for _, row in nearby_locations.iterrows():
                    st.write(f"{row['location_name']} - Address: {row['address']}")

                # Map display using Pydeck with tooltips
                st.subheader("Map of Nearest Water Testing Kit Locations")
                nearby_locations_map = pdk.Deck(
                    map_style="mapbox://styles/mapbox/streets-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=location.latitude,
                        longitude=location.longitude,
                        zoom=12,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=nearby_locations,
                            get_position='[longitude, latitude]',
                            get_color='[200, 30, 0, 160]',
                            get_radius=200,
                            pickable=True,
                        )
                    ],
                    tooltip={"html": "<b>{location_name}</b><br>Address: {address}", "style": {"color": "white"}}
                )
                st.pydeck_chart(nearby_locations_map)

            else:
                st.write("No water testing kit locations found nearby.")

        else:
            st.warning("Could not find a location for the entered zip code. Please try again.")
    except Exception as e:
        st.error(f"Error finding location: {e}")
else:
    # Display a message if no zip code is entered yet
    st.write("Enter a valid U.S. zip code and click 'Find Nearby Water Testing Kit' to see the map.")
