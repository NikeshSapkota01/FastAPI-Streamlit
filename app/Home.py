# src/app.py
import streamlit as st
import pandas as pd
import requests
from loadCss import load_css

# Call the function to apply the CSS
load_css()

# welcome message
st.title("Tuberculosis dataset explorer")
st.write(
    "This is a simple multi-page Tuberculosis dataset explorer app. \
     It uses a ```FastAPI``` backend to serve the ```Tuberculosis``` dataset EDA and \
     make predictions using a pre-trained model. \
     The frontend is built using Streamlit.")


def get_home_info():
    response = requests.get("http://127.0.0.1:8000/home")
    response.raise_for_status()
    return response.json()

def home_page():
    home_info = get_home_info()

    st.title(home_info['title'])
    st.markdown(
        f"""
        ## {home_info['description']}

        ### Purpose
        {home_info['purpose']}

        ### Key Features
        - {home_info['features'][0]}
        - {home_info['features'][1]}
        - {home_info['features'][2]}
        - {home_info['features'][3]}

        ### Acknowledgements
        {home_info['acknowledgements']}

        ---
        **Developed by:** Nikesh Sapkota
        """
    )

if __name__ == "__main__":
    home_page()