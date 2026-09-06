"""
Top Player Stats page — two data sources:
  - Live Rankings tab: current ICC-style rankings from the Cricbuzz API
  - Database Leaderboards tab: top performers from our own stored match data

Interactive elements: country filter, click-to-expand player drill-down,
and bar charts visualizing the leaderboards.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from services.player_stats_service import (
    get_live_batting_rankings, get_live_bowling_rankings,
    get_top_run_scorers, get_top_wicket_takers, get_all_countries,
    get_player_batting_history, get_player_bowling_history,
)

st.set_page_config(page_title="Top Player Stats", page_icon="🏏", layout="wide")

if st.button("🏠 Home"):
    st.switch_page("main.py")

st.title("🏏 Top Player Stats")

tab_live, tab_db = st.tabs(["Live Rankings", "Database Leaderboards"])

with tab_live:
    format_type = st.selectbox("Format", ["test", "odi", "t20"], key="rankings_format")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Batsmen")
        with st.spinner("Fetching rankings..."):
            batting_rankings = get_live_batting_rankings(format_type)
        if batting_rankings:
            st.dataframe(pd.DataFrame(batting_rankings), hide_index=True, use_container_width=True)
        else:
            st.info("Rankings unavailable right now — this endpoint may differ on your API plan.")

    with col2:
        st.subheader("Top Bowlers")
        with st.spinner("Fetching rankings..."):
            bowling_rankings = get_live_bowling_rankings(format_type)
        if bowling_rankings:
            st.dataframe(pd.DataFrame(bowling_rankings), hide_index=True, use_container_width=True)
        else:
            st.info("Rankings unavailable right now — this endpoint may differ on your API plan.")

with tab_db:
    countries = ["All"] + get_all_countries()
    country_filter = st.selectbox("Filter by country", countries)
    result_limit = 10

    country_param = None if country_filter == "All" else country_filter

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Run Scorers")
        run_scorers = get_top_run_scorers(limit=result_limit, country=country_param)
        if run_scorers:
            df_runs = pd.DataFrame(run_scorers)

            fig_runs = px.bar(
                df_runs, x="full_name", y="total_runs",
                title="Total Runs by Player",
                labels={"full_name": "Player", "total_runs": "Total Runs"},
                color="total_runs", color_continuous_scale="Blues",
            )
            st.plotly_chart(fig_runs, use_container_width=True)

            st.dataframe(df_runs.drop(columns=["player_id"]), hide_index=True, use_container_width=True)

            selected_batter = st.selectbox(
                "View match history for:",
                ["Select a player..."] + [r["full_name"] for r in run_scorers],
                key="batter_drilldown",
            )
            if selected_batter != "Select a player...":
                player_id = next(r["player_id"] for r in run_scorers if r["full_name"] == selected_batter)
                history = get_player_batting_history(player_id)
                st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)
        else:
            st.info("No batting data matches this filter.")

    with col2:
        st.subheader("Top Wicket Takers")
        wicket_takers = get_top_wicket_takers(limit=result_limit, country=country_param)
        if wicket_takers:
            df_wickets = pd.DataFrame(wicket_takers)

            fig_wickets = px.bar(
                df_wickets, x="full_name", y="total_wickets",
                title="Total Wickets by Player",
                labels={"full_name": "Player", "total_wickets": "Total Wickets"},
                color="total_wickets", color_continuous_scale="Reds",
            )
            st.plotly_chart(fig_wickets, use_container_width=True)

            st.dataframe(df_wickets.drop(columns=["player_id"]), hide_index=True, use_container_width=True)

            selected_bowler = st.selectbox(
                "View match history for:",
                ["Select a player..."] + [w["full_name"] for w in wicket_takers],
                key="bowler_drilldown",
            )
            if selected_bowler != "Select a player...":
                player_id = next(w["player_id"] for w in wicket_takers if w["full_name"] == selected_bowler)
                history = get_player_bowling_history(player_id)
                st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)
        else:
            st.info("No bowling data matches this filter.")