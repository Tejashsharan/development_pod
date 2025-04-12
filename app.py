import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from ui.main import main_ui
from ui.sidebar import sidebar_history

sidebar_history()
main_ui()
