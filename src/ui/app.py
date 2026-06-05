import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DevMind AI OS",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 DevMind AI Operating System")

# =========================
# Sidebar
# =========================

st.sidebar.title(
    "🤖 DevMind AI OS"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "History"
    ]
)

# =========================
# Dashboard Page
# =========================

if page == "Dashboard":

    st.subheader(
        "🚀 Run Task"
    )

    task = st.text_input(
        "Enter a task"
    )

    if st.button(
        "Run Task"
    ):

        if task:

            response = requests.post(
                f"{API_URL}/task",
                json={
                    "task": task
                }
            )

            st.subheader(
                "📄 Result"
            )

            st.write(
                response.json()
            )

    st.divider()

    st.subheader(
        "📊 Analytics"
    )

    analytics = requests.get(
        f"{API_URL}/analytics"
    ).json()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Tasks",
            analytics["total_tasks"]
        )

    with col2:

        st.metric(
            "Completed",
            analytics["completed_tasks"]
        )

    with col3:

        st.metric(
            "Failed",
            analytics["failed_tasks"]
        )

    st.divider()

    st.subheader(
        "📈 Agent Metrics"
    )

    metrics = requests.get(
        f"{API_URL}/metrics"
    ).json()

    metrics_df = pd.DataFrame(
        list(metrics.items()),
        columns=[
            "Agent",
            "Executions"
        ]
    )

    st.bar_chart(
        metrics_df.set_index(
            "Agent"
        )
    )

# =========================
# History Page
# =========================

if page == "History":

    st.subheader(
        "📜 Task History"
    )

    history = requests.get(
        f"{API_URL}/history"
    ).json()

    df = pd.DataFrame(
        history["tasks"]
    )

    st.dataframe(
        df,
        width="stretch"
    )