import pyodbc
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

def get_connection():
    """Get a connection to PRISM_DB."""
    return pyodbc.connect(config.CONNECTION_STRING)

# -------------------------------------------------
# APPLICATIONS
# -------------------------------------------------
def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT application_id, application_name, owner FROM Applications")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_application_by_name(app_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT application_id, application_name, owner FROM Applications WHERE application_name = ?", app_name)
    row = cursor.fetchone()
    conn.close()
    return row

def create_application(app_name, owner):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Applications (application_name, owner) VALUES (?, ?)", app_name, owner)
    conn.commit()
    cursor.execute("SELECT application_id FROM Applications WHERE application_name = ?", app_name)
    row = cursor.fetchone()
    conn.close()
    return row[0]

# -------------------------------------------------
# ASSETS
# -------------------------------------------------
def get_assets_by_application(application_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT asset_id, asset_name, asset_type, environment, ip_address FROM Assets WHERE application_id = ?", application_id)
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_asset(application_id, asset_name, asset_type, environment, ip_address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Assets (application_id, asset_name, asset_type, environment, ip_address)
        VALUES (?, ?, ?, ?, ?)
    """, application_id, asset_name, asset_type, environment, ip_address)
    conn.commit()
    conn.close()

# -------------------------------------------------
# HEALTH RESULTS
# -------------------------------------------------
def save_health_result(asset_id, check_type, status, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Health_Results (asset_id, check_type, status, value)
        VALUES (?, ?, ?, ?)
    """, asset_id, check_type, status, value)
    conn.commit()
    conn.close()

def get_health_results_by_asset(asset_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT check_type, status, value, checked_at
        FROM Health_Results
        WHERE asset_id = ?
        ORDER BY checked_at DESC
    """, asset_id)
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------------------------
# CHANGE TICKETS
# -------------------------------------------------
def get_todays_change_tickets(asset_names):
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join(["?" for _ in asset_names])
    query = f"""
        SELECT ticket_id, title, description, ci_name, change_type, change_time, status
        FROM Change_Tickets
        WHERE CAST(change_time AS DATE) = CAST(GETDATE() AS DATE)
        AND LOWER(ci_name) IN ({placeholders})
    """
    lower_names = [name.lower() for name in asset_names]
    cursor.execute(query, lower_names)
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------------------------
# INCIDENTS
# -------------------------------------------------
def create_incident(application_id, issue_summary, root_cause, priority):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Incidents (application_id, issue_summary, root_cause, priority, status)
        VALUES (?, ?, ?, ?, 'Open')
    """, application_id, issue_summary, root_cause, priority)
    conn.commit()
    conn.close()

def get_incidents_by_application(application_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT incident_id, issue_summary, root_cause, priority, status, created_at
        FROM Incidents
        WHERE application_id = ?
        ORDER BY created_at DESC
    """, application_id)
    rows = cursor.fetchall()
    conn.close()
    return rows