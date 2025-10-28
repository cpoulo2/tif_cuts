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
        df2=pd.read_csv(r"alder_list.csv")
        df2=df2[['ward','alder_first_last']]
        print(df.head())
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].replace({r'[\$,]': ''}, regex=True)
        df['tif_surplus_552_m'] = df['tif_surplus_552_m'].apply(pd.to_numeric, errors='coerce')
        df['tif_surplus_387_m'] = df['tif_surplus_387_m'].apply(pd.to_numeric, errors='coerce')
        df = df.merge(df2,on="ward",how='left')
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

    st.set_page_config(page_title="TIF Surplus Tool", layout="centered")

    st.header("Declaring a TIF Surplus")
    st.subheader("What a 'No' Vote Costs Our Schools")

    st.markdown("""
    Use the TIF Surplus Tool to see the real cost of withholding TIF surplus revenue. Our tool shows how much funding schools will lose — and how many mid-year positions could be cut — at both the school and ward level.      
    """, unsafe_allow_html=True)

# Add a sidebar with methodology

    school_tab,ward_tab = st.tabs(["School level 🏫","Ward 🏛️"])

    with school_tab:

        st.subheader("School level view 🏫")

        schools = df[['unit_name','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','ward','alder_first_last','student_count','non_white_per']]

        selected_schools = st.multiselect("**Select A School or Schools**", options=schools['unit_name'].unique().tolist(),help="Use the drop-down menu or begin typing a school name to select. Left-click on column names to sort.")

        if selected_schools == []:

            schools_filtered = schools
        
        else:

            schools_filtered = schools[schools['unit_name'].isin(selected_schools)]

        schools_filtered.columns = ['School Name',"TIF Surplus ($552m)", "TIF Surplus ($387m)","Mid Year Cuts",'Ward',"Alder","Number of Students","Percent Non-White"]

        st.dataframe(
            schools_filtered.style.format({
        "TIF Surplus ($552m)": "${:,.0f}",
        "TIF Surplus ($387m)": "${:,.0f}",
        "Percent Non-White": "{:.0%}"}),
        hide_index=True)

        if selected_schools != []:
            n = len(schools_filtered['School Name'])
            if n == 1:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 2:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[1]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[1]} positions** affecting **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 3:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[1]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[1]} positions** affecting **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[2]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[2]} positions** affecting **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 4:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)            
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[1]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[1]} positions** affecting **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[2]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[2]} positions** affecting **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[3]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[3]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[3]} positions** affecting **{schools_filtered['Number of Students'].iloc[3]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[3]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 5:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)            
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[1]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[1]} positions** affecting **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[2]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[2]} positions** affecting **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[3]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[3]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[3]} positions** affecting **{schools_filtered['Number of Students'].iloc[3]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[3]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[4]}** will stand to lose *at least* **${schools_filtered['TIF Surplus ($387m)'].iloc[4]:,.0f}** and **{schools_filtered['Mid Year Cuts'].iloc[4]} positions** affecting **{schools_filtered['Number of Students'].iloc[4]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[4]:.0%}** are non-white.
""",unsafe_allow_html=True)

    with ward_tab:

        st.subheader("Ward 🏛️")

        ward = df[['unit_name','ward','alder_first_last','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','White #','non_white_per']]

        # Sort ward options ascending
        ward = ward.sort_values(by='ward')

        select_ward = st.selectbox("**Select A Ward**", options=ward['ward'].unique().tolist(),index=32,help="Left click on a column name to sort.")

        ward_filtered = ward[ward['ward'] == select_ward]

        alder = ward_filtered['alder_first_last'].iloc[0]
        ward = ward_filtered['ward'].iloc[0]

        ward_filtered = ward_filtered[['unit_name','ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','White #','non_white_per']]

        # Create totals column

        totals = ward_filtered.copy()
        totals['non_white'] = totals['student_count'] - totals['White #']
        totals = totals[['ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white']]
        totals = totals.groupby('ward').sum().reset_index()
        totals['non_white_per'] = totals['non_white'] / totals['student_count']

        totals = totals[['tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]

        totals['unit_name'] = f'Ward {ward} Total'

        # Concatenate totals to ward_filtered

        ward_filtered = pd.concat([ward_filtered, totals], ignore_index=True)

        ward_filtered = ward_filtered[['unit_name','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]

        ward_filtered.columns = ['Name',"TIF Surplus ($552m)", "TIF Surplus ($387m)","Mid Year Cuts","Number of Students","Percent Non-White"]

        # Sort by TIF surplus descending

        ward_filtered = ward_filtered.sort_values(by="TIF Surplus ($552m)", ascending=False)

        st.markdown(f"""<b>{alder}'s Ward</b> ({ward}) will stand to lose *at least* **${ward_filtered['TIF Surplus ($387m)'].iloc[0]:,.0f}** and **{ward_filtered['Mid Year Cuts'].iloc[0]} positions** affecting **{ward_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{ward_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""", unsafe_allow_html=True)

        # Highlight Ward Total row

        def highlight_row(s):
            return ['background-color: yellow'] * len(s)
        
        ward_total_name = f'Ward {ward} Total'
        
        st.dataframe(
            ward_filtered.style.apply(lambda x: highlight_row(x) if ward_filtered.loc[x.name, 'Name'] == ward_total_name else ['']*len(x), axis=1).format({
        "TIF Surplus ($552m)": "${:,.0f}",
        "TIF Surplus ($387m)": "${:,.0f}",
        "Percent Non-White": "{:.0%}"}),
        hide_index=True)

    st.markdown("""
    **Methodology**
                
    School-level TIF surplus revenue is calculated by multiplying the share of the City of Chicago’s total declared TIF surplus allocated to CPS by each school’s FY26 budget share (that school’s FY26 budget as a percentage of the total CPS school budgets). We provide two estimates: one based on Mayor Brandon Johnson’s historic proposed surplus—$552 million directed to CPS—and another based on the Chicago Board of Education’s budgeted surplus.
                
    Estimated mid-year position loss is school-level TIF surplus revenue divided by 100,000 (the average per position dollar amount) and multiplied by 2. We multiply by 2 because it takes twice as many position cuts to get the savings of one. The mid-year position loss uses the CBOE's budgeted TIF surplus.

    **Data sources**

    Fiscal year 2026 Budget data was FOIA'd from Chicago Public Schools (CPS). Student counts and demongraphics are from CPS's Racial/Ethnic Report for school year 2025.     
                
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()