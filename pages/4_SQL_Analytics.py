"""
SQL Analytics page — pick any of the confirmed analytics questions and
run it live against the database, with the query text shown alongside.

Includes an optional bar chart when the result has a clear numeric
column suited to visual comparison (e.g. runs, wickets, margins).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from services.analytics_service import QUERIES, run_query

st.set_page_config(page_title="SQL Analytics", page_icon="📊", layout="wide")

if st.button("🏠 Home"):
    st.switch_page("main.py")

st.title("📊 SQL Analytics")
st.caption("25 analytics questions from the project brief — currently Q1–Q14 are available.")

question_labels = {num: info["title"] for num, info in QUERIES.items()}
selected_num = st.selectbox(
    "Choose a question",
    options=list(question_labels.keys()),
    format_func=lambda n: question_labels[n],
)

query_info = QUERIES[selected_num]
st.subheader(query_info["title"])
st.write(query_info["description"])

with st.expander("View SQL query"):
    st.code(query_info["sql"].strip(), language="sql")

if st.button("Run query"):
    with st.spinner("Running query..."):
        try:
            results = run_query(selected_num)
        except Exception as e:
            st.error(f"Query failed: {e}")
            results = None

    if results is not None:
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.caption(f"{len(results)} row(s) returned")

            # Offer a bar chart when there's an obvious label column + one numeric column
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            label_candidates = [c for c in df.columns if df[c].dtype == object]

            if numeric_cols and label_candidates and st.checkbox("Show as bar chart"):
                label_col = label_candidates[0]
                value_col = st.selectbox("Value to chart", numeric_cols)
                fig = px.bar(
                    df, x=label_col, y=value_col,
                    title=f"{value_col} by {label_col}",
                    color=value_col, color_continuous_scale="Blues",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Query ran successfully but returned no rows.")