import os

AI_PROVIDER = "mock"
ANTHROPIC_API_KEY = "your-api-key-here"
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"


DB_SERVER = "ICS-LT-92QTHT3\\SQLEXPRESS"
DB_NAME = "PRISM_DB"
DB_DRIVER = "ODBC Driver 17 for SQL Server"
DB_USERNAME = "sa"
DB_PASSWORD = "India@123456"

CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};Server=ICS-LT-92QTHT3\\SQLEXPRESS;DATABASE=PRISM_DB;UID=sa;PWD=India@123456;"
    #data file paths

CHANGE_TICKETS_PATH = os.path.join(os.path.dirname(__file__), "data", "mock", "change_tickets.json")

    #Health Check thresholds

CPU_WARN = 80
CPU_FAIL = 95
MEMORY_WARN = 75
MEMORY_FAIL = 90
DISK_WARN = 85
DISK_FAIL = 95
LATENCY_WARN = 100