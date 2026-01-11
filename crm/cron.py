"""
Cron jobs for CRM application.
"""

from datetime import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


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
        transport = RequestsHTTPTransport(url=graphql_endpoint)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        if result.get('hello'):
            message = f"{timestamp} CRM is alive (GraphQL endpoint responsive)\n"
    except Exception:
        # If GraphQL query fails, still log the heartbeat
        pass
    
    # Append to the log file
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(message)


def update_low_stock():
    """
    Execute the UpdateLowStockProducts mutation via GraphQL endpoint.
    Logs updated product names and new stock levels.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        graphql_endpoint = "http://localhost:8000/graphql"
        
        # GraphQL mutation to update low stock products
        mutation = """
            mutation {
                updateLowStockProducts {
                    success
                    message
                    updatedProducts {
                        id
                        name
                        stock
                    }
                }
            }
        """
        
        response = requests.post(
            graphql_endpoint,
            json={"query": mutation},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            mutation_result = result.get('data', {}).get('updateLowStockProducts', {})
            
            if mutation_result.get('success'):
                updated_products = mutation_result.get('updatedProducts', [])
                
                # Log updated products
                with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
                    log_file.write(f"[{timestamp}] {mutation_result.get('message')}\n")
                    for product in updated_products:
                        product_name = product.get('name', 'N/A')
                        new_stock = product.get('stock', 'N/A')
                        log_file.write(
                            f"[{timestamp}] Updated product: {product_name}, New stock: {new_stock}\n"
                        )
            else:
                # Log if mutation was not successful
                error_msg = mutation_result.get('message', 'Unknown error')
                with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
                    log_file.write(f"[{timestamp}] Error: {error_msg}\n")
        else:
            # Log HTTP error
            with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
                log_file.write(
                    f"[{timestamp}] HTTP Error {response.status_code}: {response.text}\n"
                )
    
    except Exception as e:
        # Log exception
        with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
            log_file.write(f"[{timestamp}] Exception: {str(e)}\n")

