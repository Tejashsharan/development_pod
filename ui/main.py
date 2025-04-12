import streamlit as st
from utils.db import store_interaction
from utils.langgraph_flow import orchestrate_agents

def main_ui():
    st.title("🧠 AI Dev Pod with Agents")

    input_text = st.text_area("📝 Enter your requirements or fix requests")

    if st.button("🚀 Run Dev Pod") and input_text:
        st.info("Processing through Dev Pod agents...")

        user_stories, design, code, test = orchestrate_agents(input_text)

        st.subheader("📌 User Stories")
        st.write(user_stories)

        st.subheader("🎨 Design")
        st.write(design)

        st.subheader("💻 Code")
        st.code(code, language="python")

        st.subheader("🧪 Test Result")
        st.write(test)

        store_interaction(input_text, test)
