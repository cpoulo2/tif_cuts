# %%
import streamlit as st
import pandas as pd
import numpy as np
import requests
import geopandas as gpd
from shapely.geometry import shape
import jinja2
import pdfkit
import base64
import streamlit.components.v1 as components

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

    st.markdown(
        """<h1 style="text-align:center;margin-top:0">
             <a href="https://protectingchicagoschools.com"
                target="_blank" 
                style="color:#0d6efd; text-decoration:underline; font-weight:600;">
               🚧 We've updated the site! 🚧 Click here for the new Protecting Chicago Schools Calculator.
             </a>
           </h1>""",
        unsafe_allow_html=True
    )

    st.image('logo.png',width='stretch')


    st.markdown("""
    Mayor Brandon Johnson's **Protecting Chicago** budget delivers an historic half a billion dollar TIF surplus to Chicago's public schools. A “no” vote will withhold these resources from our classrooms. Use the <i>Protecting Chicago Schools Calculator</i> to see how much TIF surplus revenue each school would lose with a "no" vote and how many positions could be cut mid-year. Look it up by school or ward, and then [tell your Alder](https://www.ctulocal1.org/posts/alder-letters-budget-2025): "vote <b>yes</b> for our students!"      
    """, unsafe_allow_html=True)

# Add a sidebar with methodology

    school_tab,ward_tab, keep_chicago_open_tab = st.tabs(["School level 🏫","Ward 🏛️","Keep Chicago Open 🕒"])

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
        
        def generate_html(ward, school_count, student_count, funding_loss, position_loss):
            """Generate HTML flyer for a ward"""
            try:
                template_path = "."
                
                context = {
                    'ward': ward,
                    'school_count': school_count,
                    'student_count': student_count,
                    'funding_loss': f"{funding_loss:,.0f}",
                    'position_loss': position_loss
                }
                
                template_loader = jinja2.FileSystemLoader(searchpath=template_path)
                template_env = jinja2.Environment(loader=template_loader)
                template = template_env.get_template("protect_chicago_flyer_template.html")
                
                html_content = template.render(context)
                
                return html_content
            except Exception as e:
                st.error(f"Error generating HTML: {e}")
                return None

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

            # Add HTML download button
            school_count = len(ward_filtered) - 1  # Subtract 1 for the total row
            student_count = int(ward_filtered['Number of Students'].iloc[0])
            funding_loss = ward_filtered['Dollars Lost'].iloc[0]
            position_loss = int(ward_filtered['Positions Cut'].iloc[0])
            
            html_content = generate_html(select_ward, school_count, student_count, funding_loss, position_loss)

            html_b64 = base64.b64encode(html_content.encode()).decode()
            data_uri = f"data:text/html;base64,{html_b64}"
            
            if html_content:
                st.download_button(
                    label="📄 Download Ward Fact Sheet (HTML)",
                    data=html_content,
                    file_name=f"protecting_chicago_ward_{select_ward}_fact_sheet.html",
                    mime="text/html",
                    help="Download an HTML fact sheet for this ward"
                )

            ward_pdf_url = f"https://chicagoteachersunion.github.io/ward{ward}.pdf"

            st.link_button("📄 View Ward Fact Sheet", ward_pdf_url)

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

    with keep_chicago_open_tab:
        st.subheader("Keep Chicago Open Clock")
        st.write("And a list of creeps who would rather make your grandma shovel snow than make the richest corporations on planet earth (and in human history) pay half a penny on every payroll dollar to fund services.")

        src = "https://w2.countingdownto.com/6755808"
        st.components.v1.iframe(src, width=800, height=154, scrolling=False)

        # SVG Digital Clock
        svg_clock_html = """
<html>
<head>
<style>
html, body, div {
  height: 100%;
}

body {
  margin: 0;
  background: rgb(159, 191, 135);
}

div {
  display: flex;
}

svg {
  flex: 1;
  opacity: 0.8;
  fill: red;
  background-color: black;
}
</style>
</head>
<body>
  <div>
    <svg id='clock' viewBox='0 36 122 36' xmlns='http://www.w3.org/2000/svg'>
      <g id='seconds'>
        <g>
          <path id='f7' d='M106,69l3-3h6l3,3c0,0-1,1-3,1h-6C107,70,106,69,106,69z'/>
          <path id='f6' d='M119,55l-3,2v8l3,3c0,0,1-1,1-3v-7C120,56,119,55,119,55z'/>
          <path id='f5' d='M105,55l3,2v8l-3,3c0,0-1-1-1-3v-7C104,56,105,55,105,55z'/>
          <polygon id='f4' points='109,52 115,52 118,54 115,56 109,56 106,54'/>
          <path id='f3' d='M119,40l-3,3v8l3,2c0,0,1-1,1-3v-7C120,41,119,40,119,40z'/>
          <path id='f2' d='M105,40l3,3v8l-3,2c0,0-1-1-1-3v-7C104,41,105,40,105,40z'/>
          <path id='f1' d='M106,39l3,3h6l3-3c0,0-1-1-3-1h-6C107,38,106,39,106,39z'/>
        </g>
        <g>
          <path id='e7' d='M88,69l3-3h6l3,3c0,0-1,1-3,1h-6C89,70,88,69,88,69z'/>
          <path id='e6' d='M101,55l-3,2v8l3,3c0,0,1-1,1-3v-7C102,56,101,55,101,55z'/>
          <path id='e5' d='M87,55l3,2v8l-3,3c0,0-1-1-1-3v-7C86,56,87,55,87,55z'/>
          <polygon id='e4' points='91,52 97,52 100,54 97,56 91,56 88,54'/>
          <path id='e3' d='M101,40l-3,3v8l3,2c0,0,1-1,1-3v-7C102,41,101,40,101,40z'/>
          <path id='e2' d='M87,40l3,3v8l-3,2c0,0-1-1-1-3v-7C86,41,87,40,87,40z'/>
          <path id='e1' d='M88,39l3,3h6l3-3c0,0-1-1-3-1h-6C89,38,88,39,88,39z'/>
        </g>
      </g>
      <g id='minutes'>
        <g>
          <path id='d7' d='M64,69l3-3h6l3,3c0,0-1,1-3,1h-6C65,70,64,69,64,69z'/>
          <path id='d6' d='M77,55l-3,2v8l3,3c0,0,1-1,1-3v-7C78,56,77,55,77,55z'/>
          <path id='d5' d='M63,55l3,2v8l-3,3c0,0-1-1-1-3v-7C62,56,63,55,63,55z'/>
          <polygon id='d4' points='67,52 73,52 76,54 73,56 67,56 64,54'/>
          <path id='d3' d='M77,40l-3,3v8l3,2c0,0,1-1,1-3v-7C78,41,77,40,77,40z'/>
          <path id='d2' d='M63,40l3,3v8l-3,2c0,0-1-1-1-3v-7C62,41,63,40,63,40z'/>
          <path id='d1' d='M64,39l3,3h6l3-3c0,0-1-1-3-1h-6C65,38,64,39,64,39z'/>
        </g>
        <g>
          <path id='c7' d='M46,69l3-3h6l3,3c0,0-1,1-3,1h-6C47,70,46,69,46,69z'/>
          <path id='c6' d='M59,55l-3,2v8l3,3c0,0,1-1,1-3v-7C60,56,59,55,59,55z'/>
          <path id='c5' d='M45,55l3,2v8l-3,3c0,0-1-1-1-3v-7C44,56,45,55,45,55z'/>
          <polygon id='c4' points='49,52 55,52 58,54 55,56 49,56 46,54'/>
          <path id='c3' d='M59,40l-3,3v8l3,2c0,0,1-1,1-3v-7C60,41,59,40,59,40z'/>
          <path id='c2' d='M45,40l3,3v8l-3,2c0,0-1-1-1-3v-7C44,41,45,40,45,40z'/>
          <path id='c1' d='M46,39l3,3h6l3-3c0,0-1-1-3-1h-6C47,38,46,39,46,39z'/>
        </g>
      </g>
      <g id='hours'>
        <g>
          <path id='b7' d='M22,69l3-3h6l3,3c0,0-1,1-3,1h-6C23,70,22,69,22,69z'/>
          <path id='b6' d='M35,55l-3,2v8l3,3c0,0,1-1,1-3v-7C36,56,35,55,35,55z'/>
          <path id='b5' d='M21,55l3,2v8l-3,3c0,0-1-1-1-3v-7C20,56,21,55,21,55z'/>
          <polygon id='b4' points='25,52 31,52 34,54 31,56 25,56 22,54'/>
          <path id='b3' d='M35,40l-3,3v8l3,2c0,0,1-1,1-3v-7C36,41,35,40,35,40z'/>
          <path id='b2' d='M21,40l3,3v8l-3,2c0,0-1-1-1-3v-7C20,41,21,40,21,40z'/>
          <path id='b1' d='M22,39l3,3h6l3-3c0,0-1-1-3-1h-6C23,38,22,39,22,39z'/>
        </g>
        <g>
          <path id='a7' d='M4,69l3-3h6l3,3c0,0-1,1-3,1h-6C5,70,4,69,4,69z'/>
          <path id='a6' d='M17,55l-3,2v8l3,3c0,0,1-1,1-3v-7C18,56,17,55,17,55z'/>
          <path id='a5' d='M3,55l3,2v8l-3,3c0,0-1-1-1-3v-7C2,56,3,55,3,55z'/>
          <polygon id='a4' points='7,52 13,52 16,54 13,56 7,56 4,54'/>
          <path id='a3' d='M17,40l-3,3v8l3,2c0,0,1-1,1-3v-7C18,41,17,40,17,40z'/>
          <path id='a2' d='M3,40l3,3v8l-3,2c0,0-1-1-1-3v-7C2,41,3,40,3,40z'/>
          <path id='a1' d='M4,39l3,3h6l3-3c0,0-1-1-3-1h-6C5,38,4,39,4,39z'/>
        </g>
      </g>
      <g id='dots'>
        <g>
          <circle cx='82' cy='50' r='2'/>
          <circle cx='82' cy='58' r='2'/>
        </g>
        <g>
          <circle cx='40' cy='50' r='2'/>
          <circle cx='40' cy='58' r='2'/>
        </g>
      </g>
    </svg>
  </div>
  <script>
  (function() {
    function display(a, n) {
      number = [
        [1, 1, 1, 0, 1, 1, 1], // 0
        [0, 0, 1, 0, 0, 1, 0], // 1
        [1, 0, 1, 1, 1, 0, 1], // 2
        [1, 0, 1, 1, 0, 1, 1], // 3
        [0, 1, 1, 1, 0, 1, 0], // 4
        [1, 1, 0, 1, 0, 1, 1], // 5
        [1, 1, 0, 1, 1, 1, 1], // 6
        [1, 0, 1, 0, 0, 1, 0], // 7
        [1, 1, 1, 1, 1, 1, 1], // 8
        [1, 1, 1, 1, 0, 1, 1]  // 9
      ]

      n = number[n]
      i = 0
      while (i < n.length) {
        crystal = document.getElementById(a + (i + 1))
        if (n[i] === 0) {
          crystal.style.opacity = '0.125'
        }
        else {
          crystal.style.opacity = '1'
        }
        i++
      }
    }

    function format(value) {
      value = value + ''
      if (value.length === 1) {
        return '0' + value
      }
      return value
    }

    (function update() {
      date = new Date()
      hours = format(date.getHours())
      minutes = format(date.getMinutes())
      seconds = format(date.getSeconds())

      display('a', hours[0])
      display('b', hours[1])
      display('c', minutes[0])
      display('d', minutes[1])
      display('e', seconds[0])
      display('f', seconds[1])
      
      setTimeout(update, 1000)
    })()
  })()
  </script>
</body>
</html>
"""

        st.components.v1.html(svg_clock_html, width=800, height=200, scrolling=False)

        html = """<!DOCTYPE HTML>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Audiowide&display=swap" rel="stylesheet">
<style>

p {
  text-align: center;
  font-size: 60px;
  margin-top: 0px;
  font-family: 'Audiowide', sans-serif;
  background-color: black;
  color: red;
}
</style>
</head>
<body>

<p id="demo"></p>

<script>
// Set the date we're counting down to
var countDownDate = new Date("Jan 5, 2030 15:37:25").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("demo").innerHTML = days + " Days " + hours + " Hours "
  + minutes + " Minutes " + seconds + " Seconds ";
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);
</script>

</body>
</html>"""

        st.components.v1.html(html, width=1000, height=154, scrolling=False)


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