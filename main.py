"""
Streamlit entry point. Streamlit auto-discovers files in pages/ and adds
them to the sidebar — this file itself renders as the Home page.

Interactive elements: live summary metrics from the DB, a quick player
search, and navigation shortcut buttons.
"""

import streamlit as st
from services.home_service import get_summary_counts, search_players

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")

st.title("🏏 Cricbuzz LiveStats")
st.markdown("Live Cricbuzz data combined with a SQL database for analytics and CRUD.")

counts = get_summary_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Teams", counts["teams"])
col2.metric("Players", counts["players"])
col3.metric("Matches", counts["matches"])
col4.metric("Series", counts["series"])

st.divider()

st.subheader("🔍 Quick Player Search")
search_term = st.text_input("Search by player name", placeholder="e.g. Kohli")

if search_term:
    results = search_players(search_term)
    if results:
        for r in results:
            st.write(f"**{r['full_name']}** — {r['playing_role']}, {r['country']} ({r['team_name'] or 'No team'})")
    else:
        st.info(f"No players found matching '{search_term}'.")

st.divider()

st.subheader("Jump to a section")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    if st.button("🔴 Live Matches", use_container_width=True):
        st.switch_page("pages/2_Live_Matches.py")

with nav_col2:
    if st.button("🏏 Top Player Stats", use_container_width=True):
        st.switch_page("pages/3_Top_Player_Stats.py")

with nav_col3:
    if st.button("📊 SQL Analytics", use_container_width=True):
        st.info("Coming soon — not built yet.")

with nav_col4:
    if st.button("✏️ CRUD Operations", use_container_width=True):
        st.switch_page("pages/5_CRUD_Operations.py")