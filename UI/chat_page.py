import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.troubleshoot import troubleshoot, raise_incident
from services.change_analyzer import get_todays_changes, summarise_changes
from services.health_check import run_health_checks
from database.db import get_assets_by_application

def format_health_results(results):
    output = ""
    for r in results:
        status = r['status']
        icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
        css_class = "metric-pass" if status == "PASS" else "metric-warn" if status == "WARN" else "metric-fail"
        output += f'<div class="{css_class}">{icon} <b>{r["asset_name"]}</b> | {r["check_type"].upper()} | {r["value"]}</div>'
    return output

def show_chat_page():
    st.markdown("## 💬 Prism AI Assistant")
    st.markdown("Ask me to run health checks, troubleshoot, or analyze changes.")
    st.divider()

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'pending_action' not in st.session_state:
        st.session_state.pending_action = None

    app_name = st.session_state.get('selected_app_name')
    app_id = st.session_state.get('selected_app_id')

    if not app_name:
        st.warning("Please select an application from the sidebar first.")
        return

    # Display chat history
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🔷 <b>Prism</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    st.divider()

    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏥 Health Check", use_container_width=True):
            st.session_state.user_input = f"Run health check for {app_name}"
    with col2:
        if st.button("🔍 Troubleshoot", use_container_width=True):
            st.session_state.user_input = f"Troubleshoot {app_name}"
    with col3:
        if st.button("🎫 Change Analysis", use_container_width=True):
            st.session_state.user_input = f"Any changes affecting {app_name} today?"

    # Chat input
    user_input = st.chat_input(f"Ask Prism about {app_name}...")

    if 'user_input' in st.session_state and st.session_state.user_input:
        user_input = st.session_state.user_input
        st.session_state.user_input = None

    if user_input:
        # Add user message
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        msg_lower = user_input.lower()

        with st.spinner("Prism is thinking..."):

            # Health check
            if 'health check' in msg_lower or 'run check' in msg_lower:
                results = run_health_checks(app_id)
                response = f"<b>Health Check Results for {app_name}:</b><br>"
                response += format_health_results(results)
                pass_count = sum(1 for r in results if r['status'] == 'PASS')
                warn_count = sum(1 for r in results if r['status'] == 'WARN')
                fail_count = sum(1 for r in results if r['status'] == 'FAIL')
                response += f"<br><b>Summary:</b> ✅ {pass_count} PASS | ⚠️ {warn_count} WARN | ❌ {fail_count} FAIL"

            # Troubleshoot
            elif 'troubleshoot' in msg_lower:
                result = troubleshoot(app_id)
                if result['all_clear']:
                    response = f"✅ <b>All Clear!</b> All health checks passed for <b>{app_name}</b>.<br><br>Would you like me to check today's change tickets as well? (Reply <b>Yes</b> or <b>No</b>)"
                    st.session_state.pending_action = 'check_changes'
                else:
                    response = format_health_results(result['results'])
                    response += f"<br><br>🔷 <b>AI Diagnosis:</b><br>{result['ai_diagnosis'].replace(chr(10), '<br>')}"
                    response += "<br><br>Would you like me to <b>raise an incident ticket</b> for this? (Reply <b>Yes</b> or <b>No</b>)"
                    st.session_state.pending_action = 'raise_incident'
                    st.session_state.last_diagnosis = result.get('ai_diagnosis', '')

            # Change analysis
            elif 'change' in msg_lower:
                assets = get_assets_by_application(app_id)
                asset_names = [a[1] for a in assets]
                tickets = get_todays_changes(asset_names)
                summary = summarise_changes(tickets)
                if tickets:
                    response = f"<b>🎫 Change Tickets for {app_name} Today:</b><br><br>"
                    for t in tickets:
                        response += f'<div class="ticket-card">📋 <b>{t[0]}</b> — {t[1]}<br>CI: {t[3]} | Type: {t[4]} | Status: {t[6]}</div>'
                    response += f"<br><b>AI Summary:</b><br>{summary}"
                else:
                    response = f"✅ No change tickets found for <b>{app_name}</b> today."

            # Yes/No handling
            elif msg_lower in ['yes', 'yeah', 'yes please', 'please']:
                if st.session_state.pending_action == 'check_changes':
                    assets = get_assets_by_application(app_id)
                    asset_names = [a[1] for a in assets]
                    tickets = get_todays_changes(asset_names)
                    summary = summarise_changes(tickets)
                    response = f"<b>🎫 Change Tickets for {app_name} Today:</b><br>{summary}"
                    st.session_state.pending_action = None
                elif st.session_state.pending_action == 'raise_incident':
                    diagnosis = st.session_state.get('last_diagnosis', 'Issue detected during health check')
                    raise_incident(app_id, f"Issues found in {app_name}", diagnosis, "Medium")
                    response = f"✅ <b>Incident raised successfully</b> for <b>{app_name}</b>.<br>Priority: Medium | Status: Open"
                    st.session_state.pending_action = None
                else:
                    response = "I'm not sure what you're confirming. Please ask me to run a health check or troubleshoot first."

            elif msg_lower in ['no', 'nope', 'no thanks']:
                st.session_state.pending_action = None
                response = "No problem! Let me know if you need anything else."

            else:
                response = """I can help you with:<br>
                • <b>Health Check</b> — 'Run health check for {app}'<br>
                • <b>Troubleshoot</b> — 'Troubleshoot {app}'<br>
                • <b>Change Analysis</b> — 'Any changes affecting {app} today?'""".format(app=app_name)

        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()