import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DevMind AI OS",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    """
    # 🤖 DevMind AI Operating System

    ### Multi-Agent AI Workflow Platform

    Research • Planning • Summarization
    """
)

# =========================
# Sidebar
# =========================

st.sidebar.title(
    "🤖 DevMind AI OS"
)

st.sidebar.markdown(
    """
    ---
    ### Navigation

    Manage tasks and monitor agents

    ---
    """
)

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "History"
    ]
)

# =========================
# Dashboard
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

            result = response.json()

            task_id = result["task_id"]

            st.success(
                "Task Submitted Successfully!"
            )

            st.write(
                f"Task ID: {task_id}"
            )

            status_placeholder = st.empty()

            while True:

                task_response = requests.get(
                    f"{API_URL}/tasks/{task_id}"
                ).json()

                current_status = task_response["status"]

                status_placeholder.info(
                    f"Current Status: {current_status}"
                )

                if current_status in [
                    "COMPLETED",
                    "FAILED"
                ]:
                    break

                time.sleep(1)

            if current_status == "COMPLETED":

                st.success(
                    "✅ Task Completed!"
                )

                st.write(
                    task_response["result"]
                )

            else:

                st.error(
                    task_response["result"]
                )

    st.divider()

    # =========================
    # Analytics
    # =========================

    st.subheader(
        "📊 Analytics"
    )

    analytics = requests.get(
        f"{API_URL}/analytics"
    ).json()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📋 Total Tasks",
            analytics["total_tasks"]
        )

    with col2:

        st.metric(
            "✅ Completed",
            analytics["completed_tasks"]
        )

    with col3:

        st.metric(
            "❌ Failed",
            analytics["failed_tasks"]
        )

    st.divider()

    # =========================
    # Agent Metrics
    # =========================

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

    if not df.empty:

        df.columns = [
            "ID",
            "Task",
            "Status",
            "Result",
            "Created At"
        ]

    st.dataframe(
        df,
        width="stretch"
    )