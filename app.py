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

    st.set_page_config(
        page_title="Protecting Chicago Schools Calculator", 
        layout="centered",
        page_icon="🏫",
        initial_sidebar_state="collapsed"
    )

    # hide Streamlit share profile/avatar elements (matches obfuscated class names)
    st.markdown("""
    <style>
    /* match obfuscated profile container / preview and creator avatar */
    div[class*="profileContainer"],
    div[class*="profilePreview"],
    img[data-testid="appCreatorAvatar"],
    a[href*="share.streamlit.io/user/"],
    a[href*="share.streamlit.io"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("Protecting Chicago Schools Calculator")
    st.subheader("What a 'No' Vote Costs Our Schools")

    st.markdown("""
    Mayor Brandon Johnson's **Protecting Chicago** budget delivers an historic half a billion dollar TIF surplus to Chicago's public schools. A “no” vote will withhold these resources from our classrooms. Use the <i>Protecting Chicago Schools Calculator</i> to see how much TIF surplus revenue each school would lose with a "no" vote and how many positions could be cut mid-year. Look it up by school or ward, and then [tell your Alder](https://www.ctulocal1.org/posts/alder-letters-budget-2025): "vote <b>yes</b> for our students!"      
    """, unsafe_allow_html=True)

# Add a sidebar with methodology

    school_tab,ward_tab = st.tabs(["School level 🏫","Ward 🏛️"])

    with school_tab:

        st.subheader("School level view 🏫")

#        schools = df[['unit_name','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','ward','alder_first_last','student_count','non_white_per']]
        schools = df[['unit_name','tif_surplus_552_m','mid_year_cuts','ward','alder_first_last','student_count','non_white_per']]

        selected_schools = st.multiselect("**Select A School or Schools**", options=schools['unit_name'].unique().tolist(),help="Select a school or schools using the drop-down menu or by typing a school name.")

        if selected_schools == []:

            schools_filtered = schools
        
        else:

            schools_filtered = schools[schools['unit_name'].isin(selected_schools)]



#        schools_filtered.columns = ['School Name',"TIF Surplus ($552m)", "TIF Surplus ($387m)","Mid Year Cuts",'Ward',"Alder","Number of Students","Percent Non-White"]
        schools_filtered.columns = ['School Name',"Dollars Lost","Positions Cut",'Ward',"Alder","Number of Students","Percent Non-White"]

        if selected_schools != []:
            n = len(schools_filtered['School Name'])
            if n == 1:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 2:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[1]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[1]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 3:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[1]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[1]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[2]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[2]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 4:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)            
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[1]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[1]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[2]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[2]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[3]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[3]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[3]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[3]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[3]:.0%}** are non-white.
""",unsafe_allow_html=True)
            elif n == 5:
                st.markdown(f"""**{schools_filtered['School Name'].iloc[0]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
""",unsafe_allow_html=True)            
                st.markdown(f"""**{schools_filtered['School Name'].iloc[1]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[1]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[1]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[1]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[1]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[2]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[2]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[2]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[2]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[2]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[3]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[3]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[3]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[3]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[3]:.0%}** are non-white.
""",unsafe_allow_html=True)
                st.markdown(f"""**{schools_filtered['School Name'].iloc[4]}** will stand to lose **${schools_filtered['Dollars Lost'].iloc[4]:,.0f}** and **{schools_filtered['Positions Cut'].iloc[4]} positions**. This will affect **{schools_filtered['Number of Students'].iloc[4]:,.0f}** students of which **{schools_filtered['Percent Non-White'].iloc[4]:.0%}** are non-white.
""",unsafe_allow_html=True)
                
        st.markdown(f"""<center>✊ <b>Take action!</b> 📢 <a href="https://www.ctulocal1.org/posts/alder-letters-budget-2025">Tell your Alder to vote YES for TIF surplus</a>!</center>""", unsafe_allow_html=True)
        st.markdown(" ")

        if selected_schools == []:
            st.markdown(f"""<center> <b> What a NO vote costs these schools</b></center>""", unsafe_allow_html=True)
        if selected_schools != []:
            n = len(schools_filtered['School Name'])
            if n == 1:
                st.markdown(f"""<center> <b> What a NO vote costs this school</b></center>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<center> <b> What a NO vote costs these schools</b></center>""", unsafe_allow_html=True)
        st.dataframe(
            schools_filtered.style.format({
#        "TIF Surplus ($552m)": "${:,.0f}",
        "Dollars Lost": "${:,.0f}",
        "Number of Students" : "{:,.0f}",
        "Percent Non-White": "{:.0%}"}),
        hide_index=True)


    with ward_tab:

        st.subheader("Ward 🏛️")

        ward = df[['unit_name','ward','alder_first_last','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','White #','non_white_per']]

        # Sort ward options ascending
        ward = ward.sort_values(by='ward')

        wards = ward['ward'].unique().tolist()
        wards.append(42)

        wards = sorted(wards)

        select_ward = st.selectbox("**Select A Ward**", options=wards,index=32,help="Left click on a column name to sort.")

        ward_filtered = ward[ward['ward'] == select_ward]

        if select_ward == 42:

            st.markdown(f""" Alder <b>Brendan Reilly's</b> Ward (42) has no public schools in it.""",unsafe_allow_html=True)

        else:

            alder = ward_filtered['alder_first_last'].iloc[0]
            ward = ward_filtered['ward'].iloc[0]

    #        ward_filtered = ward_filtered[['unit_name','ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','White #','non_white_per']]
            ward_filtered = ward_filtered[['unit_name','ward','tif_surplus_552_m','mid_year_cuts','student_count','White #','non_white_per']]

            # Create totals column

            totals = ward_filtered.copy()
            totals['non_white'] = totals['student_count'] - totals['White #']
    #        totals = totals[['ward','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white']]
            totals = totals[['ward','tif_surplus_552_m','mid_year_cuts','student_count','non_white']]
            totals = totals.groupby('ward').sum().reset_index()
            totals['non_white_per'] = totals['non_white'] / totals['student_count']

    #        totals = totals[['tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]
            totals = totals[['tif_surplus_552_m','mid_year_cuts','student_count','non_white_per']]

            totals['unit_name'] = f'Ward {ward} Total'

            # Concatenate totals to ward_filtered

            ward_filtered = pd.concat([ward_filtered, totals], ignore_index=True)

    #        ward_filtered = ward_filtered[['unit_name','tif_surplus_552_m','tif_surplus_387_m','mid_year_cuts','student_count','non_white_per']]
            ward_filtered = ward_filtered[['unit_name','tif_surplus_552_m','mid_year_cuts','student_count','non_white_per']]
            ward_filtered.columns = ['Name',"Dollars Lost","Positions Cut","Number of Students","Percent Non-White"]

            # Sort by TIF surplus descending

            ward_filtered = ward_filtered.sort_values(by="Dollars Lost", ascending=False)

            st.markdown(f""" Schools in Alder <b>{alder}'s</b> Ward ({ward}) will stand to lose **${ward_filtered['Dollars Lost'].iloc[0]:,.0f}** and **{ward_filtered['Positions Cut'].iloc[0]} positions**. This will affect **{ward_filtered['Number of Students'].iloc[0]:,.0f}** students of which **{ward_filtered['Percent Non-White'].iloc[0]:.0%}** are non-white.
    """, unsafe_allow_html=True)

            # Highlight Ward Total row

            def highlight_row(s):
                return ['background-color: yellow'] * len(s)
            
            ward_total_name = f'Ward {ward} Total'
            st.markdown(f"""<center>✊ <b>Take action!</b> 📢 <a href="https://www.ctulocal1.org/posts/alder-letters-budget-2025">Tell your Alder to vote YES for TIF surplus</a>!</center>""", unsafe_allow_html=True)
            st.markdown(" ")
            st.markdown(f"""<center> <b> What a NO vote costs these schools</b></center>""", unsafe_allow_html=True)
            st.dataframe(
                ward_filtered.style.apply(lambda x: highlight_row(x) if ward_filtered.loc[x.name, 'Name'] == ward_total_name else ['']*len(x), axis=1).format({
    #        "TIF Surplus ($552m)": "${:,.0f}",
            "Dollars Lost": "${:,.0f}",
            "Number of Students" : "{:,.0f}",
            "Percent Non-White": "{:.0%}"}),
            hide_index=True)

    st.markdown("""
    <style>
    .small-text {
        font-size: 0.8em; /* You can adjust this to 0.7em or 0.9em as needed */
        line-height: 1.4;
    }
    </style>

    <div class="small-text">
    <b>Methodology</b><br><br>
    <i>“Dollars Lost”</i> refers to the potential TIF surplus revenue that a “no” vote would withhold from schools. It is calculated by multiplying Mayor Brandon Johnson’s historic TIF surplus—of which $552 million is allocated to CPS—by each school’s budget share (that school’s budget as a percentage of the total CPS budget for schools).<br><br>
    <i>“Positions Cut”</i> refers to the potential mid-year cuts that a “no” vote would make necessary to balance CPS’s budget. It is calculated by dividing school-level TIF surplus revenue by 100,000 (the average per-position dollar amount) and multiplying by 2. We multiply by 2 because it takes twice as many position cuts to achieve the savings of one. These calculations use the Chicago Board of Education’s budgeted $387 million in TIF surplus revenue as the basis for the cuts.<br><br>
    <b>Data sources</b><br><br>
    Fiscal year 2026 budget data was FOIA'd from Chicago Public Schools (CPS). Student counts and demographics are from CPS's Racial/Ethnic Report for school year 2025.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()