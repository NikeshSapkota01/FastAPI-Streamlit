import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from loadCss import load_css
import numpy as np

# Call the function to apply the CSS
load_css()

# Load the dataset
file_path = 'data/TB_burden_countries_2024-08-13.csv'
tb_data = pd.read_csv(file_path)

# Convert 'year' to a categorical type for selection
tb_data['year'] = tb_data['year'].astype(str)

# Set the title of the app
st.title("Epidemiological Analysis of TB: Comparision Between")

# Create a sidebar for selecting the country and year range
st.sidebar.header("Filter Options")

# List of available countries
country_list = tb_data['country'].unique()

# Select the first country
selected_country = st.sidebar.selectbox("Select Country", country_list)

# Safely determine the index for "Nepal"
if "Nepal" in country_list:
    default_index = list(country_list).index("Nepal")
else:
    default_index = 0  # Default to the first country if Nepal is not found

# Select the comparison country, defaulting to Nepal if available
selected_comparison_country = st.sidebar.selectbox(
    "Compare with", country_list, index=default_index)

# Define default year range
default_start_year = 2008
default_end_year = int(tb_data['year'].max())

# Create the year range slider with default values
selected_years = st.sidebar.slider(
    "Select Year Range",
    int(tb_data['year'].min()),  # Minimum year available in the dataset
    default_end_year,            # Maximum year available in the dataset
    (default_start_year, default_end_year)  # Default range
)

# selected_years = st.sidebar.slider(
#     "Select Year Range", int(tb_data['year'].min()), int(tb_data['year'].max()), (2000, 2020))

# Filter the data for the selected country
filtered_data = tb_data[(tb_data['country'] == selected_country) & 
                        (tb_data['year'].astype(int).between(*selected_years))]

# Filter the data for the comparison country (Nepal by default)
comparison_data = tb_data[(tb_data['country'] == selected_comparison_country) & 
                          (tb_data['year'].astype(int).between(*selected_years))]


# st.write("## Key Metrics")
header_html = f"""
    <h2 class="h2-class"> Key Metrics </h2>
"""


st.markdown(header_html, unsafe_allow_html=True)

# Create the HTML for the table
table_html = f"""
<div class="table-container">
    <table>
        <tr>
            <th>Metric</th>
            <th>{selected_country}</th>
            <th>{selected_comparison_country}</th>
        </tr>
        <tr>
            <td>Total Estimated Population</td>
            <td>{filtered_data['e_pop_num'].sum():,}</td>
            <td>{comparison_data['e_pop_num'].sum():,}</td>
        </tr>
        <tr>
            <td>Average TB Incidence per 100k</td>
            <td>{filtered_data['e_inc_100k'].mean():.2f}</td>
            <td>{comparison_data['e_inc_100k'].mean():.2f}</td>
        </tr>
        <tr>
            <td>Average Case Fatality Rate (CFR)</td>
            <td>{filtered_data['cfr'].mean():.2f}</td>
            <td>{comparison_data['cfr'].mean():.2f}</td>
        </tr>
    </table>
</div>
"""

# Display the table
st.markdown(table_html, unsafe_allow_html=True)
st.write("")
st.write("")

# Plotting TB incidence for both countries
st.write(f"### TB Incidence Over Time: {selected_country} and {selected_comparison_country} ({selected_years[0]} - {selected_years[1]})")
plt.figure(figsize=(10, 5))
plt.plot(filtered_data['year'], filtered_data['e_inc_100k'], marker='o', label=selected_country)
plt.plot(comparison_data['year'], comparison_data['e_inc_100k'], marker='o', label=selected_comparison_country, linestyle='--')
plt.title(f"TB Incidence Comparison ({selected_country} vs {selected_comparison_country})")
plt.xlabel("Year")
plt.ylabel("Incidence per 100,000")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.write("")
st.write("")


# Plotting Case Fatality Rate (CFR) for both countries
st.write(f"### Case Fatality Rate (CFR) Over Time: {selected_country} and {selected_comparison_country} ({selected_years[0]} - {selected_years[1]})")
plt.figure(figsize=(10, 5))
plt.bar(filtered_data['year'], filtered_data['cfr'], color='blue', alpha=0.5, label=selected_country)
plt.bar(comparison_data['year'], comparison_data['cfr'], color='orange', alpha=0.5, label=selected_comparison_country)
plt.title(f"Case Fatality Rate (CFR) Comparison ({selected_country} vs {selected_comparison_country})")
plt.xlabel("Year")
plt.ylabel("CFR")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.write("")
st.write("")

#  TB Mortality Rate Over Time:
st.write(f"### TB Mortality Rate Over Time: {selected_country} and {selected_comparison_country} ({selected_years[0]} - {selected_years[1]})")
plt.figure(figsize=(10, 5))
plt.plot(filtered_data['year'], filtered_data['e_mort_exc_tbhiv_100k'], marker='o', label=selected_country)
plt.plot(comparison_data['year'], comparison_data['e_mort_exc_tbhiv_100k'], marker='o', label=selected_comparison_country, linestyle='--')
plt.title(f"TB Mortality Rate Comparison ({selected_country} vs {selected_comparison_country})")
plt.xlabel("Year")
plt.ylabel("Mortality Rate per 100,000")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.write("")
st.write("")

# Load the second dataset that contains 'sex' and 'age_group' information
# Replace 'second_dataset.csv' with the actual file name
sex_age_group = 'data/TB_burden_age_sex_2024-08-13.csv'
sex_age_data = pd.read_csv(sex_age_group)

# Ensure the 'year' column in both datasets is of the same type (string in this case)
tb_data['year'] = tb_data['year'].astype(str)
sex_age_data['year'] = sex_age_data['year'].astype(str)

# Merge the datasets on common columns like 'country' and 'year'
merged_data = pd.merge(tb_data, sex_age_data, on=['country', 'year'], how='inner')
columns_to_keep = [
    'country', 'year', 'e_inc_100k', 'e_pop_num', 'age_group', 'sex', 'risk_factor', 'best', 'hi'
]
filtered_data = merged_data[columns_to_keep]
# Filter the data for the comparison country
comparison_data = filtered_data[(filtered_data['country'] == selected_comparison_country)]


# Add a gender filter before filtering the data
gender_mapping = {"All": "a", "Male": "m", "Female": "f"}
selected_gender = st.selectbox("Select Gender", options=list(gender_mapping.keys()), index=0)

# Filter data for the year 2022 and the selected gender
if selected_gender == "All":
    filtered_data_2022 = filtered_data
    comparison_data_2022 = comparison_data
else:
    filtered_data_2022 = filtered_data[(filtered_data['sex'] == gender_mapping[selected_gender])]
    comparison_data_2022 = comparison_data[(comparison_data['sex'] == gender_mapping[selected_gender])]

# # Group data by age group and calculate the mean incidence
age_group_data = filtered_data_2022.groupby('age_group')['e_inc_100k'].mean().reset_index()
comparison_age_group_data = comparison_data_2022.groupby('age_group')['e_inc_100k'].mean().reset_index()

st.write(f"### TB Incidence by Age Group (2022): {selected_country} and {selected_comparison_country}")
plt.figure(figsize=(10, 5))
plt.bar(age_group_data['age_group'], age_group_data['e_inc_100k'], color='blue', alpha=0.5, label=selected_country)
plt.bar(comparison_age_group_data['age_group'], comparison_age_group_data['e_inc_100k'], color='orange', alpha=0.5, label=selected_comparison_country)
plt.title(f"TB Incidence by Age Group ({selected_country} vs {selected_comparison_country}) - 2022")
plt.xlabel("Age Group")
plt.ylabel("Incidence per 100,000")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.write("")
st.write("")

st.write(f"### TB Incidence by Age Group (2022): {selected_country} and {selected_comparison_country}")

# Preparing the data for the donut charts
labels = age_group_data['age_group']
sizes = age_group_data['e_inc_100k']
comparison_sizes = comparison_age_group_data['e_inc_100k']

# Create a figure with two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Donut chart for the selected country
axes[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}, colors=plt.cm.Blues(np.linspace(0.3, 0.7, len(labels))))
axes[0].add_artist(plt.Circle((0, 0), 0.70, color='white'))
axes[0].set_title(f"TB Incidence by Age Group - {selected_country} (2022)")

# Donut chart for the comparison country
axes[1].pie(comparison_sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}, colors=plt.cm.Oranges(np.linspace(0.3, 0.7, len(labels))))
axes[1].add_artist(plt.Circle((0, 0), 0.70, color='white'))
axes[1].set_title(f"TB Incidence by Age Group - {selected_comparison_country} (2022)")

# Display the side-by-side donut charts
st.pyplot(fig)


# Define the CSS for the table
st.markdown("""
<style>
.table-container {
    display: flex;
    justify-content: center;
}
table {
    width: 100%;
    margin: 0px;
    border-collapse: collapse;
    font-size: 1.1em;
}
table, th, td {
    border: 1px solid #ddd;
}
th, td {
    padding: 8px;
    text-align: left;
}
th {
    background-color: #393737;
}
.h2-class {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(250, 250, 250);
    letter-spacing: -0.005em;
    padding: 1rem 0px 0.5rem 0px;
    margin: 0px;
    line-height: 1.2;
}
</style>
""", unsafe_allow_html=True)