import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DevMind AI OS",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 DevMind AI Operating System")

task = st.text_input(
    "Enter a task"
)

if st.button("Run Task"):

    if task:

        response = requests.post(

            f"{API_URL}/task",

            json={
                "task": task
            }
        )

        st.subheader(
            "Result"
        )

        st.write(
            response.json()
        )