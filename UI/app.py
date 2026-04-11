import streamlit as st
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_all_applications

st.set_page_config(
    page_title="Prism - IT Operations AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    .prism-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }
    .prism-sub { color: #8b949e; font-size: 1rem; margin-bottom: 20px; }
    .metric-pass {
        background-color: #1a3a1a;
        border-left: 4px solid #2ea043;
        padding: 10px; border-radius: 5px;
        margin: 5px 0; color: #2ea043;
    }
    .metric-warn {
        background-color: #3a2e1a;
        border-left: 4px solid #d29922;
        padding: 10px; border-radius: 5px;
        margin: 5px 0; color: #d29922;
    }
    .metric-fail {
        background-color: #3a1a1a;
        border-left: 4px solid #f85149;
        padding: 10px; border-radius: 5px;
        margin: 5px 0; color: #f85149;
    }
    .chat-user {
        background-color: #1f2937;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        text-align: right;
        color: #e6edf3;
    }
    .chat-ai {
        background-color: #161b22;
        border-left: 3px solid #00d4ff;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #e6edf3;
    }
    .ticket-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px; margin: 8px 0;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="prism-header">🔷 PRISM</div>', unsafe_allow_html=True)
    st.markdown('<div class="prism-sub">AI-Powered IT Operations</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("### 📋 Select Application")
    apps = get_all_applications()
    app_names = [a[1] for a in apps]
    app_dict = {a[1]: a[0] for a in apps}

    if app_names:
        selected_app_name = st.selectbox("Application", app_names, label_visibility="collapsed")
        selected_app_id = app_dict[selected_app_name]
        st.session_state['selected_app_name'] = selected_app_name
        st.session_state['selected_app_id'] = selected_app_id
    else:
        st.warning("No applications found. Please onboard one first.")
        selected_app_name = None
        selected_app_id = None

    st.divider()
    st.markdown("### 🧭 Navigation")
    page = st.radio("Go to", ["💬 Chat", "📊 Dashboard", "📥 Onboarding"], label_visibility="collapsed")

    st.divider()
    st.markdown("### ℹ️ System Info")
    st.markdown("**AI Mode:** Mock 🟡")
    st.markdown("**DB:** PRISM_DB ✅")

if page == "💬 Chat":
    import importlib.util
    spec = importlib.util.spec_from_file_location("chat_page", os.path.join(os.path.dirname(__file__), "chat_page.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.show_chat_page()

elif page == "📊 Dashboard":
    import importlib.util
    spec = importlib.util.spec_from_file_location("dashboard_page", os.path.join(os.path.dirname(__file__), "dashboard_page.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.show_dashboard_page()

elif page == "📥 Onboarding":
    import importlib.util
    spec = importlib.util.spec_from_file_location("onboarding_page", os.path.join(os.path.dirname(__file__), "onboarding_page.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.show_onboarding_page()