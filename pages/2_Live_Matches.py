"""
Live Matches page — shows currently live matches and recent results
pulled directly from the Cricbuzz API. No database involved here.

Interactive elements: format filter, refresh button, and expandable
per-match scorecards fetched on demand.
"""

import streamlit as st
import pandas as pd
from services.live_match_service import get_live_matches_flat, get_recent_matches_flat, get_scorecard_flat

st.set_page_config(page_title="Live Matches", page_icon="🔴", layout="wide")
if st.button("🏠 Home"):
   st.switch_page("main.py")
st.title("🔴 Live Matches")

col_refresh, col_filter = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 Refresh"):
        st.rerun()
with col_filter:
    format_filter = st.selectbox("Filter by format", ["All", "TEST", "ODI", "T20"])


def render_match_list(matches: list[dict], key_prefix: str):
    if format_filter != "All":
        matches = [m for m in matches if m["match_format"] == format_filter]

    if not matches:
        st.info("No matches to show for this filter.")
        return

    for match in matches:
        with st.container(border=True):
            st.subheader(f"{match['team1']} vs {match['team2']}")
            st.caption(f"{match['series_name']} — {match['match_desc']} ({match['match_format']})")
            st.write(f"📍 {match['venue']}")
            st.write(f"**Status:** {match['status']}")

            if match["match_id"]:
                with st.expander("View Scorecard"):
                    if st.button("Load scorecard", key=f"{key_prefix}_{match['match_id']}"):
                        with st.spinner("Fetching scorecard..."):
                            scorecard = get_scorecard_flat(match["match_id"])

                        if scorecard["error"]:
                            st.error(f"Could not load scorecard: {scorecard['error']}")
                        elif not scorecard["innings"]:
                            st.info("Scorecard not available yet for this match.")
                        else:
                            for inning in scorecard["innings"]:
                                st.markdown(f"**{inning['inning_label']}**")
                                if inning["batting"]:
                                    st.dataframe(pd.DataFrame(inning["batting"]), hide_index=True, use_container_width=True)
                                if inning["bowling"]:
                                    st.dataframe(pd.DataFrame(inning["bowling"]), hide_index=True, use_container_width=True)


tab_live, tab_recent = st.tabs(["Live Now", "Recent Matches"])

with tab_live:
    with st.spinner("Fetching live matches..."):
        live_matches = get_live_matches_flat()
    render_match_list(live_matches, "live")

with tab_recent:
    with st.spinner("Fetching recent matches..."):
        recent_matches = get_recent_matches_flat()
    render_match_list(recent_matches, "recent")