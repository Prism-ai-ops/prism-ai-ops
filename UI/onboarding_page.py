import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.onboarding import parse_excel, onboard_application
import pandas as pd

def show_onboarding_page():
    st.markdown("## 📥 Application Onboarding")
    st.markdown("Upload an Excel file to onboard a new application into Prism.")
    st.divider()

    # Download template
    st.markdown("### 📄 Step 1 — Download Template")
    template_data = {
        'app_name': ['Payment Gateway', 'Payment Gateway'],
        'asset_name': ['PG-ServerA', 'PG-DB01'],
        'asset_type': ['Windows', 'MSSQL'],
        'environment': ['PROD', 'PROD'],
        'ip_address': ['10.0.0.1', '10.0.0.2']
    }
    template_df = pd.DataFrame(template_data)
    st.dataframe(template_df, use_container_width=True)

    # Upload section
    st.markdown("### 📤 Step 2 — Upload Your Excel File")
    col1, col2 = st.columns(2)
    with col1:
        app_name_input = st.text_input("Application Name", placeholder="e.g. Payment Gateway")
    with col2:
        owner_input = st.text_input("Owner Name", placeholder="e.g. Chandu")

    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=['xlsx'])

    if uploaded_file and app_name_input and owner_input:
        assets, error = parse_excel(uploaded_file)

        if error:
            st.error(f"❌ {error}")
        else:
            st.markdown("### 👀 Step 3 — Preview Assets")
            preview_df = pd.DataFrame(assets)
            st.dataframe(preview_df, use_container_width=True)
            st.success(f"✅ {len(assets)} assets found. Ready to onboard.")

            if st.button("✅ Confirm & Onboard", use_container_width=True):
                with st.spinner("Onboarding application..."):
                    app_id, err = onboard_application(app_name_input, owner_input, assets)
                    if err:
                        st.error(f"❌ {err}")
                    else:
                        st.success(f"🎉 '{app_name_input}' onboarded successfully with {len(assets)} assets!")
                        st.balloons()
    elif uploaded_file and (not app_name_input or not owner_input):
        st.warning("Please fill in Application Name and Owner Name before uploading.")