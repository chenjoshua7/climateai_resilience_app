import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import mapping

st.set_page_config(
    page_title="Resilience",
    layout="wide")

color_map = {
    "Urban Orchard": "orange",      
    "Community Garden": "green",    
    "Urban Wetlands": "blue",
    "Solar Farm": "beige",  
    "Cooling Station": "lightblue",
    "Pocket Park": "darkgreen"     
}

def generate_legend_html(color_map):
    legend_html = ""
    for label, color in color_map.items():
        legend_html += f"""
        <li style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 15px; height: 15px; background-color: {color}; margin-right: 10px; border: 1px solid black;"></div>
            <span>{label}</span>
        </li>
        """
    legend_html += "</ul></div>"
    
    return legend_html

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

## data with gpt responses
data.loc[data["chosen_response"]=="Urban Orchards", "chosen_response"] = "Urban Orchard"
data = gpd.GeoDataFrame(data)

## geospatial data
shp_data = gpd.read_file(os.path.join(os.getcwd(),'streamlit', 'final_data','final_data.shp')).iloc[:, 1:]
shp_data = shp_data.sort_values("area", ascending = False).reset_index()
data["geometry"] = shp_data.loc[:100, "geometry"]

## Filter sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Filters</h1>", unsafe_allow_html=True)
    c1, c2= st.columns(2)
    remedies = st.multiselect("Remedies", data["chosen_response"].value_counts().keys())
    legend_html = generate_legend_html(color_map)
    st.markdown(legend_html, unsafe_allow_html=True)

if not remedies:
    remedies = data["chosen_response"].value_counts().keys()

data = data[data["chosen_response"].isin(remedies)]

header_page()

start_coords = (40.645717282767706, -73.95609863714381)
m = folium.Map(location=start_coords, zoom_start=11.5, control_scale=True)

space, col2, col3 = st.columns([0.2, 3, 1])



for _, row in data.iterrows():
    ## Get html tag
    popup_html = generate_popup_html(row)
    #marker
    folium.Marker(
        location= (row.latitude,row.longitude),
        popup=folium.Popup(popup_html, max_width=400),
        icon=folium.Icon(color=color_map[row["chosen_response"]], icon="info-sign"),
    ).add_to(m)
    
    geojson_data = mapping(row.geometry)
    folium.GeoJson(
        data=geojson_data,
        style_function=lambda x: {
            'color': 'black',
            'weight': 3
        }
    ).add_to(m)


with col2:
    clicked_data = st_folium(m, width=700, height=700) 

if not clicked_data['last_object_clicked']:
    col3.subheader("Select an Opportunity Area for More Information")
    
if clicked_data and clicked_data['last_object_clicked']:
    clicked_lat = clicked_data['last_object_clicked']["lat"]
    clicked_lon = clicked_data['last_object_clicked']["lng"]

    # Define a similarity threshold for latitude and longitude
    lat_threshold = 0.0001
    long_threshold = 0.0001

    # Compare the clicked coordinates with the DataFrame
    for _, row in data.iterrows():
        if abs(clicked_lat - row['latitude']) <= lat_threshold and \
           abs(clicked_lon - row['longitude']) <= long_threshold:
            
            col3.subheader(f"Parking Lot")
            col3.write(f"**Proposed Remedy:** {row['chosen_response']}")
            col3.write(f"**Reasoning:** {row['reasoning']}")


with st.expander(label="About This Project"):
    st.write("""
        This demo is the final submission for the September 2024 Climate AI Hackathon, an event bringing 
        together individuals passionate about using new technologies to address the current climate challenges.

        The Resilience App is designed to leverage geospatial data and Generative AI to assist policymakers 
        and green developers in identifying key areas for sustainable development, community building, and 
        financially efficient resource allocation. This demo includes features such as air quality, district 
        median income, and heat vulnerability, with a focus on analyzing parking lots as potential development areas.

        Please note: This is a demo and should not be used for actual decision-making. Its purpose is to explore 
        the potential of Generative AI in tasks like this. Furthermore, lived experience is irreplaceable—community 
        members are always the best source of insight for community-building decisions. We hope this app contributes 
        to the ongoing discussion about the role of Generative AI in these processes.
    """)
