import streamlit as st
from utils.db import get_all_chats

def sidebar_history():
    with st.sidebar:
        st.markdown("## 💬 Chat History")
        history = get_all_chats()
        for i, (meta, doc) in enumerate(history):
            with st.expander(f"Query {i+1}"):
                st.write(f"**User:** {meta['user_input']}")
                st.write(f"**Bot:** {doc}")
