import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os

st.set_page_config(
    page_title="Resilience",
    layout="wide")

def header_page():
    st.markdown("<h1 style='text-align: center; padding-top:0px; padding-bottom: 5px;'>Resilience</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; padding-bottom: 20px;'>AI for More Human Cities</h4>", unsafe_allow_html=True)



def generate_popup_html(features):
    name = features["chosen_response"]
    cost = features["suggested_price"]
    first_impact = features["First important positive impact"]
    second_impact = features["Second important positive impact"]
    third_impact = features["Third important positive impact"]

    #cuase of chat, some of these are strings, some of them are a list
    other_possibilities = features["Other possibilities"]
    other_possibilities = other_possibilities.replace("'", "").replace("[", "").replace("]", "")
    
    # Star rating function (1-5)
    def generate_star_rating(impact):
        if isinstance(impact, str):
            level = impact[-1]  # Extracting the number as the rating
            filled_stars = "★" * int(level)
            empty_stars = "☆" * (5 - int(level))
            impact = "".join(i for i in impact[:-2] if i.isalpha() or i == " ")
            return f"{impact} <span style='color: #4CAF50;'><br> {filled_stars}</span><span style='color: #D3D3D3;'>{empty_stars}</span>"
        else:
            return f""

    # Create HTML content for the popup
    html_content = f"""
    <div style="font-family: Arial, sans-serif; width: 250px; font-size: 12px;">
        <h3 style="margin-bottom: 5px; font-size: 16px;">Opportunity Area: Parking Lot</h3>
        <p style="margin-top: 0; margin-bottom: 10px;"><strong>Proposed Remedy: {name}</strong></p>
        
        <div style="background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin-bottom: 10px;">
            <span style="font-size: 1.1em; font-weight: bold;">Estimated Cost: ${cost:,}</span>
        </div>

        <div style="background-color: #e6f7ff; padding: 8px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Top Positive Impacts:</strong>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>{generate_star_rating(first_impact)}</li>
                <li>{generate_star_rating(second_impact)}</li>
                <li>{generate_star_rating(third_impact)}</li>
            </ul>
        </div>

        <div style="background-color: #f9f9f9; padding: 8px; border-radius: 5px;">
            <strong>Other Possibilities:</strong>
            <p>{other_possibilities}</p>
        </div>
    </div>
    """

    return html_content

file_path = os.path.join(os.getcwd(), 'streamlit','data.csv')
data = pd.read_csv(file_path).iloc[:,1:]

header_page()

data.loc[data["chosen_response"]=="Urban Orchards", "chosen_response"] = "Urban Orchard"

color_map = {
    "Urban Orchard": "green",
    "Community Garden": "blue",
    "Urban Wetlands": "brown",
    "Solar Farm": "darkred",
    "Cooling Station":"beige",
    "Pocket Park": "darkpurple"
    }

start_coords = (40.6399, -73.8554)
m = folium.Map(location=start_coords, zoom_start=11.5, control_scale=True)

space, col2, col3 = st.columns([0.5, 3, 1])

for _, row in data.iterrows():
    popup_html = generate_popup_html(row)
    folium.Marker(
        location= (row.latitude,row.longitude),  # Replace with actual coordinates
        popup=folium.Popup(popup_html, max_width=400),
        icon=folium.Icon(color=color_map[row["chosen_response"]], icon="info-sign"),
    ).add_to(m)
    
with col2:
    clicked_data = st_folium(m, width=1500) 

if not clicked_data['last_object_clicked']:
    col3.subheader("Select an Opportunity Area for More Information")
    
if clicked_data and clicked_data['last_object_clicked']:
    clicked_lat = clicked_data['last_object_clicked']["lat"]
    clicked_lon = clicked_data['last_object_clicked']["lng"]

    # Define a similarity threshold for latitude and longitude
    lat_threshold = 0.0001  # Adjust based on your requirements
    long_threshold = 0.0001  # Adjust based on your requirements

    # Compare the clicked coordinates with the DataFrame
    for _, row in data.iterrows():
        if abs(clicked_lat - row['latitude']) <= lat_threshold and \
           abs(clicked_lon - row['longitude']) <= long_threshold:
            # If coordinates are similar, display the reasoning
            col3.subheader(f"Parking Lot")
            col3.write(f"**Proposed Remedy:** {row['chosen_response']}")
            col3.write(f"**Reasoning:** {row['reasoning']}")
