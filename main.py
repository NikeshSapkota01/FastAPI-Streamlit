from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import joblib
from typing import List
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from enum import Enum

app = FastAPI()
app.mount("/app", StaticFiles(directory="app", html=True), name="app")

DATA_DIR = "data"

def list_csv_files() -> List[str]:
    # List all CSV files in the data directory
    return [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

# Dynamically create an Enum for the available CSV files
CSV_File_Name = Enum("CSV_File_Name", {file: file for file in list_csv_files()})


# You could also add an endpoint to list available CSV files
@app.get("/list_csv_files_name")
def list_csv_files_name():
    # List all CSV files in the data directory
    return {"files": list_csv_files()}

@app.get("/get_tb_data")
def get_tb_data(
    filename: str = Query(..., description="Name of the CSV file"),
):
    if not filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are supported.")
    
    file_path = os.path.join(DATA_DIR, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Load the CSV data
    tb = pd.read_csv(file_path)

    # Replace inf, -inf, and NaN values
    tb.replace([float('inf'), float('-inf')], None, inplace=True)
    tb.fillna('NaN', inplace=True)

    return tb.to_dict(orient="records")

    

@app.get("/home")
def get_home_info():
    return {
        "title": "Visualisation of Tuberculosis Trends in Nepal",
        "description": (
            "Tuberculosis (TB) remains a significant public health challenge in Nepal, necessitating a comprehensive "
            "understanding of its trends for effective disease control. This application serves as an interactive "
            "platform for exploring TB data provided by the World Health Organization (WHO), specifically focusing "
            "on the epidemiological trends in Nepal."
        ),
        "purpose": (
            "The primary goal of this application is to provide healthcare professionals, policymakers, and researchers "
            "with insights into TB incidence, prevalence, and control measures in Nepal. By visualizing this data, users "
            "can identify trends, assess the effectiveness of current interventions, and explore opportunities for enhanced "
            "TB control."
        ),
        "features": [
            "Data Exploration: Access and interact with the latest TB data from WHO.",
            "Trend Analysis: Visualize trends in TB incidence over time.",
            "Interactive Maps: Explore geographic distribution and high-burden areas in Nepal.",
            "Customizable Views: Filter data by year, region, and demographic characteristics.",
        ],
        "acknowledgements": "This application utilizes data from WHO to support global efforts in TB eradication.",
    }

@app.get("/download_tb_data")
def download_tb_data(
    filename: CSV_File_Name = Query(..., description="Select a file"),
):
    # The filename is now an enum, which will be rendered as a dropdown in Swagger
    file_path = os.path.join(DATA_DIR, filename.value)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file for download
    return FileResponse(
        file_path, media_type="application/octet-stream", filename=filename.value
    )
