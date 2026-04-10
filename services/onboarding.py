import sys
import os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.db import (
    get_application_by_name,
    create_application,
    create_asset
)

def parse_excel(file):
    """
    Read uploaded Excel file and return list of asset records.
    """
    try:
        df = pd.read_excel(file, engine='openpyxl')

        # Validate required columns
        required_columns = ['app_name', 'asset_name', 'asset_type', 'environment']
        for col in required_columns:
            if col not in df.columns:
                return None, f"Missing column: '{col}'. Required columns: {required_columns}"

        assets = []
        for _, row in df.iterrows():
            asset = {
                'app_name': str(row['app_name']).strip(),
                'asset_name': str(row['asset_name']).strip(),
                'asset_type': str(row['asset_type']).strip(),
                'environment': str(row['environment']).strip(),
                'ip_address': str(row['ip_address']).strip() if 'ip_address' in df.columns else ''
            }
            assets.append(asset)

        return assets, None

    except Exception as e:
        return None, f"Error reading file: {str(e)}"


def onboard_application(app_name, owner, assets):
    """
    Save application and its assets to the database.
    """
    # Check if already exists
    existing = get_application_by_name(app_name)
    if existing:
        return None, f"Application '{app_name}' is already onboarded."

    # Create application
    app_id = create_application(app_name, owner)

    # Create each asset
    for asset in assets:
        create_asset(
            application_id=app_id,
            asset_name=asset['asset_name'],
            asset_type=asset['asset_type'],
            environment=asset['environment'],
            ip_address=asset.get('ip_address', '')
        )

    return app_id, None