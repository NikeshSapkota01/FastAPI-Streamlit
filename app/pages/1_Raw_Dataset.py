"""
Show the raw dataset
"""
import streamlit as st
import pandas as pd
import os
import io
from loadCss import load_css

# Constants
DATA_DIR = "data"  # Directory containing the CSV files

# Call the function to apply the CSS
load_css()

# List CSV files in the data directory
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]

# Sidebar for selecting a file
selected_file = st.sidebar.selectbox("Select a CSV file", csv_files)

# Check if a file is selected
if selected_file:
    file_path = os.path.join(DATA_DIR, selected_file)
    df = pd.read_csv(file_path)

    # Display options
    display_options = st.sidebar.selectbox("Display Options", ["Head", "Tail"])

    if display_options == "Head":
        # Display the head of the DataFrame
        st.title(f"{selected_file} Head")
        st.write(df.head())
    else:
        # Display the tail of the DataFrame
        st.title(f"{selected_file} Tail")
        st.write(df.tail())

    # Show the entire dataset
    if st.sidebar.checkbox("Show entire dataset"):
        st.title(f"{selected_file} Dataset")
        st.write(df)

    # Show summary statistics and info
    if st.sidebar.checkbox("Show summary statistics and info"):
        # Summary statistics
        st.title(f"{selected_file} Summary Statistics")
        st.write(df.describe())

        # DataFrame info
        st.title(f"{selected_file} Info")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
