"""
Cron jobs for CRM application.
"""

from datetime import datetime
import requests


def log_crm_heartbeat():
    """
    Log a heartbeat message to confirm the CRM application's health.
    Optionally queries the GraphQL hello field to verify the endpoint is responsive.
    """
    # Format: DD/MM/YYYY-HH:MM:SS
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive\n"
    
    # Optionally query GraphQL hello field to verify endpoint is responsive
    try:
        graphql_endpoint = "http://localhost:8000/graphql"
        query = {"query": "{ hello }"}
        response = requests.post(graphql_endpoint, json=query, timeout=5)
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive (GraphQL endpoint responsive)\n"
    except Exception:
        # If GraphQL query fails, still log the heartbeat
        pass
    
    # Append to the log file
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(message)

