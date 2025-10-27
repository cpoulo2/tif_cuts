# %%
import streamlit as st
import pandas as pd
import numpy as np
import requests
import geopandas as gpd
from shapely.geometry import shape

# Load data
@st.cache_data
def load_data():
    """Load the EBF data"""
    try:
        df = pd.read_csv(r"data.csv")
        print(df.head())
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].apply(pd.to_numeric, errors='coerce')
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].apply(pd.to_numeric, errors='coerce')
        return df
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}. Please ensure the CSV files are in the correct location.")
        return None
#%%
def main():    
    # Load data
    df=load_data()

    if df is None:
        return

    # Main app

    st.set_page_config(page_title="TIF and cuts", layout="centered")

    st.header("Declaring TIF Surplus")
    st.subheader("What a 'No' Vote Costs Our Schools")

    st.markdown("""
    This tool allows you to look up the impact of withholding TIF surplus revenue on our schools--both financially and the numbers of positions that will have to be terminated.
    """, unsafe_allow_html=True)

# Add a sidebar with methodology

    school_tab,ward_tab = st.tabs(["School level 🏫","Ward 🏛️"])

    with school_tab:

        st.subheader("School level view 🏫")

        schools = df[['unit_name','ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]

        selected_schools = st.multiselect("**Select A School or Schools**", options=schools['unit_name'].unique().tolist(),help="Left-click on column names to sort.")

        if selected_schools == []:

            schools_filtered = schools
        
        else:

            schools_filtered = schools[schools['unit_name'].isin(selected_schools)]

        schools_filtered.columns = ['School Name','Ward',"TIF Surplus ($552m)", "TIF Surplus ($387m)","Mid Year Cuts","Number of Students","Percent Non-White"]

        st.dataframe(
            schools_filtered.style.format({
        "TIF Surplus ($552m)": "${:,.0f}",
        "TIF Surplus ($387m)": "${:,.0f}",
        "Percent Non-White": "{:.0%}"}),
        hide_index=True)

        if selected_schools != []:
            st.write("**STATE BASIC FACTS**")
            n = len(schools_filtered['School Name'])
            if n == 1:
                st.write(schools_filtered['School Name'].iloc[0])
            elif n == 2:
                st.write(schools_filtered['School Name'].iloc[0])
                st.write(schools_filtered['School Name'].iloc[1])
            elif n == 3:
                st.write(schools_filtered['School Name'].iloc[0])
                st.write(schools_filtered['School Name'].iloc[1])
                st.write(schools_filtered['School Name'].iloc[2])
            elif n == 4:
                st.write(schools_filtered['School Name'].iloc[0])
                st.write(schools_filtered['School Name'].iloc[1])
                st.write(schools_filtered['School Name'].iloc[2])
                st.write(schools_filtered['School Name'].iloc[3])
            elif n == 5:
                st.write(schools_filtered['School Name'].iloc[0])
                st.write(schools_filtered['School Name'].iloc[1])
                st.write(schools_filtered['School Name'].iloc[2])
                st.write(schools_filtered['School Name'].iloc[3])
                st.write(schools_filtered['School Name'].iloc[4])

    with ward_tab:

        st.subheader("Ward 🏛️")

        ward = df[['unit_name','ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]

        select_ward = st.selectbox("**Select A Ward**", options=ward['ward'].unique().tolist(),index=16,help="Left click on a column name to sort.")

        st.image(f"ward_{select_ward}.png")

        st.write(f"**Name of the Ward {select_ward} Alder.**")

        ward_filtered = ward[ward['ward'] == select_ward]

        ward_filtered = ward_filtered[['unit_name','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]

        ward_filtered.columns = ['School Name',"TIF Surplus ($552m)", "TIF Surplus ($387m)","Mid Year Cuts","Number of Students","Percent Non-White"]

        st.dataframe(
            ward_filtered.style.format({
        "TIF Surplus ($552m)": "${:,.0f}",
        "TIF Surplus ($387m)": "${:,.0f}",
        "Percent Non-White": "{:.0%}"}),
        hide_index=True)

if __name__ == "__main__":
    main()