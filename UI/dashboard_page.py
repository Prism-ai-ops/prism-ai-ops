import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.health_check import run_health_checks
from database.db import get_assets_by_application, get_health_results_by_asset, get_incidents_by_application

def show_dashboard_page():
    st.markdown("## 📊 Health Dashboard")
    st.divider()

    app_name = st.session_state.get('selected_app_name')
    app_id = st.session_state.get('selected_app_id')

    if not app_name:
        st.warning("Please select an application from the sidebar first.")
        return

    st.markdown(f"### Application: **{app_name}**")

    # Run health check button
    if st.button("🔄 Run Health Check Now", use_container_width=True):
        with st.spinner("Running health checks..."):
            results = run_health_checks(app_id)
            st.session_state['last_results'] = results

    # Show results
    results = st.session_state.get('last_results', [])

    if results:
        # Summary metrics
        pass_count = sum(1 for r in results if r['status'] == 'PASS')
        warn_count = sum(1 for r in results if r['status'] == 'WARN')
        fail_count = sum(1 for r in results if r['status'] == 'FAIL')

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Checks", len(results))
        col2.metric("✅ PASS", pass_count)
        col3.metric("⚠️ WARN", warn_count)
        col4.metric("❌ FAIL", fail_count)

        st.divider()
        st.markdown("### Check Results")

        # Group by asset
        assets = {}
        for r in results:
            if r['asset_name'] not in assets:
                assets[r['asset_name']] = []
            assets[r['asset_name']].append(r)

        for asset_name, checks in assets.items():
            with st.expander(f"🖥️ {asset_name}", expanded=True):
                for c in checks:
                    status = c['status']
                    icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
                    css = "metric-pass" if status == "PASS" else "metric-warn" if status == "WARN" else "metric-fail"
                    st.markdown(
                        f'<div class="{css}">{icon} <b>{c["check_type"].upper()}</b> — {c["value"]} ({status})</div>',
                        unsafe_allow_html=True
                    )
    else:
        st.info("Click 'Run Health Check Now' to see results.")

    st.divider()

    # Incidents section
    st.markdown("### 🚨 Recent Incidents")
    incidents = get_incidents_by_application(app_id)
    if incidents:
        for inc in incidents:
            with st.expander(f"🚨 {inc[1]} — {inc[3]}"):
                st.write(f"**Root Cause:** {inc[2]}")
                st.write(f"**Priority:** {inc[3]}")
                st.write(f"**Status:** {inc[4]}")
                st.write(f"**Created:** {inc[5]}")
    else:
        st.success("No incidents recorded for this application.")