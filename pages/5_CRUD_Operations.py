"""
CRUD Operations page — manage Players and Teams through forms.

Interactive elements: search/filter on the players list, delete
confirmation checkboxes, and friendly messages for common database errors
(like duplicate names) instead of raw tracebacks.
"""

import streamlit as st
from services.crud_service import (
    create_player, list_players, update_player, delete_player,
    create_team, list_teams, update_team, delete_team,
)
from utils.validators import ValidationError, VALID_PLAYING_ROLES

st.set_page_config(page_title="CRUD Operations", page_icon="✏️", layout="wide")

if st.button("🏠 Home"):
    st.switch_page("main.py")

st.title("✏️ CRUD Operations")

tab_players, tab_teams = st.tabs(["Players", "Teams"])

# ---------------------------------------------------------------------------
# PLAYERS TAB
# ---------------------------------------------------------------------------
with tab_players:
    st.subheader("Add a new player")

    teams = list_teams()
    team_options = {t["team_name"]: t["team_id"] for t in teams}

    with st.form("add_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full name")
            country = st.text_input("Country")
            playing_role = st.selectbox("Playing role", sorted(VALID_PLAYING_ROLES))
        with col2:
            batting_style = st.text_input("Batting style (optional)")
            bowling_style = st.text_input("Bowling style (optional)")
            team_name = st.selectbox("Team", ["(none)"] + list(team_options.keys()))

        submitted = st.form_submit_button("Add player")
        if submitted:
            try:
                team_id = team_options.get(team_name) if team_name != "(none)" else None
                new_player = create_player(
                    full_name=full_name,
                    country=country,
                    playing_role=playing_role,
                    batting_style=batting_style or None,
                    bowling_style=bowling_style or None,
                    team_id=team_id,
                )
                st.success(f"Added player: {new_player['full_name']} (id={new_player['player_id']})")
            except ValidationError as e:
                st.error(str(e))
            except Exception as e:
                if "unique constraint" in str(e).lower():
                    st.error(f"A player named '{full_name}' already exists in this match context.")
                else:
                    st.error(f"Something went wrong: {e}")

    st.divider()
    st.subheader("Existing players")

    all_players = list_players()

    search_col, country_col, role_col = st.columns(3)
    with search_col:
        search_term = st.text_input("Search by name", placeholder="e.g. Kohli")
    with country_col:
        player_countries = ["All"] + sorted({p["country"] for p in all_players})
        country_filter = st.selectbox("Filter by country", player_countries, key="player_country_filter")
    with role_col:
        role_filter = st.selectbox("Filter by role", ["All"] + sorted(VALID_PLAYING_ROLES), key="player_role_filter")

    filtered_players = all_players
    if search_term:
        filtered_players = [p for p in filtered_players if search_term.lower() in p["full_name"].lower()]
    if country_filter != "All":
        filtered_players = [p for p in filtered_players if p["country"] == country_filter]
    if role_filter != "All":
        filtered_players = [p for p in filtered_players if p["playing_role"] == role_filter]

    st.caption(f"Showing {len(filtered_players)} of {len(all_players)} players")

    if not filtered_players:
        st.info("No players match your filters.")
    else:
        for p in filtered_players:
            with st.expander(f"{p['full_name']} ({p['country']}) — {p['playing_role']}"):
                with st.form(f"edit_player_{p['player_id']}"):
                    e_name = st.text_input("Full name", value=p["full_name"], key=f"name_{p['player_id']}")
                    e_country = st.text_input("Country", value=p["country"], key=f"country_{p['player_id']}")
                    e_role = st.selectbox(
                        "Playing role", sorted(VALID_PLAYING_ROLES),
                        index=sorted(VALID_PLAYING_ROLES).index(p["playing_role"]),
                        key=f"role_{p['player_id']}",
                    )
                    e_batting = st.text_input("Batting style", value=p["batting_style"] or "", key=f"bat_{p['player_id']}")
                    e_bowling = st.text_input("Bowling style", value=p["bowling_style"] or "", key=f"bowl_{p['player_id']}")
                    confirm_delete = st.checkbox("I confirm I want to delete this player", key=f"confirm_{p['player_id']}")

                    col_save, col_delete = st.columns(2)
                    save = col_save.form_submit_button("Save changes")
                    delete = col_delete.form_submit_button("Delete player", type="secondary")

                    if save:
                        try:
                            update_player(
                                p["player_id"], e_name, e_country, e_role,
                                batting_style=e_batting or None,
                                bowling_style=e_bowling or None,
                                team_id=p["team_id"],
                            )
                            st.success("Updated — refresh to see changes.")
                            st.rerun()
                        except ValidationError as ve:
                            st.error(str(ve))
                        except Exception as e:
                            st.error(f"Could not update player: {e}")

                    if delete:
                        if not confirm_delete:
                            st.warning("Please check the confirmation box before deleting.")
                        else:
                            try:
                                delete_player(p["player_id"])
                                st.success("Deleted — refresh to see changes.")
                                st.rerun()
                            except Exception as de:
                                st.error(
                                    f"Could not delete — this player likely has match performance "
                                    f"records tied to them. ({de})"
                                )

# ---------------------------------------------------------------------------
# TEAMS TAB
# ---------------------------------------------------------------------------
with tab_teams:
    st.subheader("Add a new team")

    with st.form("add_team_form", clear_on_submit=True):
        t_name = st.text_input("Team name")
        t_country = st.text_input("Country")
        t_submitted = st.form_submit_button("Add team")
        if t_submitted:
            try:
                new_team = create_team(t_name, t_country)
                st.success(f"Added team: {new_team['team_name']} (id={new_team['team_id']})")
            except ValidationError as e:
                st.error(str(e))
            except Exception as e:
                if "unique constraint" in str(e).lower():
                    st.error(f"A team named '{t_name}' already exists — please use a different name.")
                else:
                    st.error(f"Could not add team: {e}")

    st.divider()
    st.subheader("Existing teams")

    all_teams = list_teams()
    team_search = st.text_input("Search by team name", placeholder="e.g. India", key="team_search")

    filtered_teams = all_teams
    if team_search:
        filtered_teams = [t for t in filtered_teams if team_search.lower() in t["team_name"].lower()]

    st.caption(f"Showing {len(filtered_teams)} of {len(all_teams)} teams")

    if not filtered_teams:
        st.info("No teams match your search.")
    else:
        for t in filtered_teams:
            with st.expander(f"{t['team_name']} ({t['country']})"):
                with st.form(f"edit_team_{t['team_id']}"):
                    e_team_name = st.text_input("Team name", value=t["team_name"], key=f"tname_{t['team_id']}")
                    e_team_country = st.text_input("Country", value=t["country"], key=f"tcountry_{t['team_id']}")
                    confirm_team_delete = st.checkbox("I confirm I want to delete this team", key=f"tconfirm_{t['team_id']}")

                    col_save, col_delete = st.columns(2)
                    save = col_save.form_submit_button("Save changes")
                    delete = col_delete.form_submit_button("Delete team", type="secondary")

                    if save:
                        try:
                            update_team(t["team_id"], e_team_name, e_team_country)
                            st.success("Updated — refresh to see changes.")
                            st.rerun()
                        except ValidationError as ve:
                            st.error(str(ve))
                        except Exception as e:
                            st.error(f"Could not update team: {e}")

                    if delete:
                        if not confirm_team_delete:
                            st.warning("Please check the confirmation box before deleting.")
                        else:
                            try:
                                delete_team(t["team_id"])
                                st.success("Deleted — refresh to see changes.")
                                st.rerun()
                            except Exception as de:
                                st.error(
                                    f"Could not delete — this team likely has players or matches "
                                    f"tied to it. ({de})"
                                )