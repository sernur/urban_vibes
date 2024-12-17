# app.py
import streamlit as st
import pandas as pd

import sector_list
import concern
import twitter_fetcher
import gov_ceo

st.set_page_config(page_title="urban_vibes", layout="wide")
st.markdown(
    """
    <style>
    .card {
        background-color: #333333;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        border: 1px solid #444444;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card h4 {
        color: #ffffff;
        margin: 0;
        font-size: 24px;
    }
    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
    }
    .degree-level-1 {
        background-color: #28a745; /* Green */
    }
    .degree-level-2 {
        background-color: #ffc107; /* Amber */
        color: #333333;
    }
    .degree-level-3 {
        background-color: #dc3545; /* Red */
    }
    .card p {
        color: #dddddd;
        font-size: 18px;
        margin: 10px 0;
    }
    .card strong {
        color: #ffffff;
    }
    .btn {
        background-color: #0066cc;
        color: #ffffff;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin-top: 15px;
    }
    .btn:hover {
        background-color: #005bb5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_us_cities():
    # Ensure cities.csv is one city per line.
    df = pd.read_csv('assets/cities.csv', encoding='utf-8', header=None)
    cities = df[0].tolist()
    return cities

us_cities = load_us_cities()

st.write("An AI assistant to monitor and analyze social media concerns in your city.")

city = st.selectbox("Select a US city:", [""] + us_cities)
if city == "":
    st.warning("Please select a city.")

st.write("### Select Sectors of Interest:")
sector_dict = {s.sector: s for s in sector_list.SECTOR_LIST}
sector_names = [s.sector for s in sector_list.SECTOR_LIST]
selected_sector_names = st.multiselect("", sector_names)

selected_sectors = [sector_dict[name] for name in selected_sector_names if name in sector_dict]

department_list = []
for s in selected_sectors:
    department_list += s.departments

if 'concerns' not in st.session_state:
    st.session_state.concerns = None

if 'solutions' not in st.session_state:
    st.session_state.solutions = {}

if st.button("Get Concerns"):
    if city == "":
        st.warning("Please select a city.")
    elif not selected_sectors:
        st.warning("Please select at least one sector.")
    else:
        with st.spinner("Analyzing concerns from Twitter..."):
            try:
                concerns = twitter_fetcher.get_concerns(selected_sectors, department_list, city)
                concerns.sort(key=lambda x: x.degree_level, reverse=True)
                st.session_state.concerns = concerns
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state.concerns:
    for idx, c in enumerate(st.session_state.concerns):
        st.markdown(
            f"""
            <div class='card'>
                <div class='card-header'>
                    <h4>Sector: {c.sector}</h4>
                    <span class='badge degree-level-{c.degree_level}'>{c.degree}</span>
                </div>
                <p><strong>Department:</strong> {c.department}</p>
                <p><strong>Concern:</strong> {c.concern}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        concern_key = f"concern_{c.sector}_{idx}"
        if concern_key not in st.session_state.solutions:
            if st.button("View Suggested Solution", key=f"btn_{concern_key}"):
                with st.spinner("Generating solution..."):
                    solution = gov_ceo.generate_solution(c.sector, c.department, c.concern)
                    st.session_state.solutions[concern_key] = solution

        if concern_key in st.session_state.solutions:
            st.markdown("### Suggested Solution:")
            st.write(st.session_state.solutions[concern_key])
