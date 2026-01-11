#!/usr/bin/env python3
"""
Script to send order reminders for pending orders using GraphQL.
Queries orders with order_date within the last 7 days and logs reminders.
"""

import sys
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Calculate the date 7 days ago (for filtering orders within the last week)
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GraphQL query to get orders with order_date within the last 7 days
query = gql("""
    query GetRecentOrders($startDate: String!) {
        orders(orderDate_Gte: $startDate) {
            id
            customer {
                email
            }
            orderDate
        }
    }
""")

def send_order_reminders():
    """Query GraphQL endpoint and log order reminders."""
    try:
        # Create transport
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
        
        # Create client
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Execute query
        result = client.execute(query, variable_values={"startDate": seven_days_ago})
        
        # Get orders from result
        orders = result.get('orders', [])
        
        # Log each order
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            for order in orders:
                order_id = order.get('id', 'N/A')
                customer_email = order.get('customer', {}).get('email', 'N/A')
                log_message = f"[{timestamp}] Order ID: {order_id}, Customer Email: {customer_email}\n"
                log_file.write(log_message)
        
        print("Order reminders processed!")
        
    except Exception as e:
        # Log error if GraphQL query fails
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"[{timestamp}] Error processing order reminders: {str(e)}\n"
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(error_message)
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    send_order_reminders()

