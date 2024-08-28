# """
# Tuberculosis dataset with land area and year filter
# """

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from loadCss import load_css

# Call the function to apply the CSS
load_css()

# Define the base URL and filenames
BASE_URL = "http://127.0.0.1:8000"
tb_filename = 'TB_burden_countries_2024-08-13.csv'
land_filename = 'data/land.csv'
land_data = pd.read_csv(land_filename)

# Fetch TB data from FastAPI endpoint
try:
    url = f"{BASE_URL}/get_tb_data"
    params = {"filename": tb_filename}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        tb_data = response.json()
        tb_df = pd.DataFrame(tb_data)

        # Filter by year
        available_years = tb_df['year'].unique()
        selected_year = st.selectbox('Select Year', sorted(available_years))

        tb_df = tb_df[tb_df['year'] == selected_year]

        # Aggregate TB data
        tb_agg = tb_df.groupby(['country', 'iso3', 'e_pop_num'])[['year']].mean().reset_index()

        # Rename 'e_pop_num' to 'total infected population'
        tb_agg.rename(columns={'e_pop_num': 'total infected population'}, inplace=True)

        # Merge with land area data
        tb_agg = tb_agg.merge(land_data, left_on='country', right_on='Country Name', how='left')

        # Calculate TB incidence per square km
        tb_agg['incidence_per_sq_km'] = tb_agg['total infected population'] / tb_agg['sq km']

        # Define the custom color scale (normalized)
        custom_colorscale = [
            [0.0, 'green'],  # 0% -> green
            [0.5, 'orange'],  # 50% -> orange
            [1.0, 'red']  # 100% -> red
        ]

        # Create the map
        fig = px.choropleth(tb_agg,
                            locations='iso3',
                            color='incidence_per_sq_km',
                            color_continuous_scale=custom_colorscale,
                            range_color=[0, 100],  # Adjust range as needed
                            hover_name='country',
                            hover_data={
                                'country': False,  # Don't show 'country' as it's already the hover name
                                'iso3': False,  # ISO code
                                'total infected population': True,  # Population
                                'year': True,  # Year
                                'sq km': True,  # Land Area in sq km
                                'incidence_per_sq_km': ':.2f'  # Format TB Incidence per sq km
                            },
                            labels={'incidence_per_sq_km': 'TB Incidence per sq km'},
                            title=f'TB Incidence per Square Kilometer by Country in {selected_year}')

        fig.update_geos(showcoastlines=True, coastlinecolor='Black',
                        showland=True, landcolor='LightGray',
                        showocean=True, oceancolor='LightBlue',
                        showlakes=True, lakecolor='LightBlue')

        fig.update_layout(hovermode='closest')
        # Streamlit app
        st.title('Global Distribution of TB Incidence: Cases per km²')
        st.plotly_chart(fig)
        
        # Top 5 highest and lowest TB incidence rates per sq km
        top_5_highest = tb_agg.nlargest(5, 'incidence_per_sq_km')
        top_5_lowest = tb_agg.nsmallest(5, 'incidence_per_sq_km')
        
        st.write("### Top 5 Countries with TB Incidence Rates per Square Kilometer")
        
          # Display the results side by side
        col1, col2 = st.columns(2)
        

        with col1:
            st.write("### Highest")
            st.write(top_5_highest[['country', 'incidence_per_sq_km']])

        with col2:
            st.write("### Lowest")
            st.write(top_5_lowest[['country', 'incidence_per_sq_km']])
    else:
        st.error(f"An error occurred: {response.status_code} - {response.text}")
except Exception as e:
    st.error(f"An error occurred: {e}")
