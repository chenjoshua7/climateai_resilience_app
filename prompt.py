prompt_template = """Given the following features of this parking lot in New York, select the best green or sustainable use of the land. Make a culturally, physically, engineering, and financially informed decision. The final output should be in JSON format with the following fields:
1. **chosen_response**: The selected land use option.
2. **reasoning**: A brief explanation (within 200 words) of why this solution is the best, based on cultural, physical, engineering, and financial aspects.
3. **suggested_price**: The estimated cost of implementing the solution.
4. **top_3_positive_impacts**: The top 3 positive impacts of this solution.

### Features:
- Length of the area: {length} meters
- Area: {area} square meters
- Latitude: {latitude}
- Longitude: {longitude}
- Borough: {borough}
- Community Name: {community_name}
- Heat Vulnerability Index: {heat_vulnerability} (scale of 1-10)
- Flood Risk Index: {flood_risk} (scale of 1-10)
- Proximity to Schools: {school_proximity} kilometers
- Median Household Income: {median_income} USD
- Air Quality Index: {air_quality} (higher values indicate worse air quality)

### Green and Sustainable Land Use Options:
1. **Community Garden**
2. **Green Roof**
3. **Permeable Pavement**
4. **Pocket Park**
5. **Solar Farm**
6. **Bioswale**
7. **Rain Garden**
8. **Shade Tree Grove**
9. **Urban Orchard**
10. **Urban Wetlands**
11. **Cooling Station**
12. **Bike Rack**
13. **Public Plaza**
14. **Sports Field**
15. **Playground**

### Instructions:
- Select the best green or sustainable use of this land.
- Return the response in the following JSON format:
{{
    "chosen_response": "Selected land use option",
    "reasoning": "A concise explanation under 200 words.",
    "suggested_price": "Estimated cost in USD as an int",
    "First important positive impact" : "2-4 words - ranks on a scale of 1 to 5",
    "Second important positive impact" : "2-4 words - ranks on a scale of 1 to 5",
    "Third important positive impact" : "2-4 words - ranks on a scale of 1 to 5",
    "Other possibilities" : "other top possibilities. Limit 3"
    ]
}}

Example response:
\n    "chosen_response": "Urban Wetlands",\n    "reasoning": "Given the area\'s proximity to Jamaica Bay, its large size, and the need for flood mitigation and improved local air quality, transforming the parking lot into urban wetlands is optimal. Culturally, wetlands resonate with the local identity centered around Jamaica Bay. Physically, wetlands naturally manage flood risk and can vastly improve air quality. Engineering-wise, designing for water retention, native plant species, and pathways is feasible. Financially, such projects often receive federal and state funding, minimizing local budget strain, and long-term maintenance costs are lower compared to other options.",\n    "suggested_price": 5000000, \n    "First important positive impact": "Improved flood mitigation systems and protection against climate-change-induced sea-level rise 5",\n    "Second important positive impact": "Enhanced local biodiversity, creating habitats for native species 5",\n    "Third important positive impact": "Improved air and water quality, benefiting community health 4",\n    "Other possibilities":        "Community Garden, Shade Tree Grove, Pocket Park"    \n
"""