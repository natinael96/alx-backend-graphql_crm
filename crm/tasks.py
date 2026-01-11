"""
Celery tasks for CRM application.
"""
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generate_crm_report():
    """
    Generate a weekly CRM report using GraphQL queries.
    Fetches total customers, orders, and revenue, then logs the report.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        graphql_endpoint = "http://localhost:8000/graphql"
        transport = RequestsHTTPTransport(url=graphql_endpoint)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # GraphQL query to fetch report data
        query = gql("""
            query {
                totalCustomers
                totalOrders
                totalRevenue
            }
        """)
        
        result = client.execute(query)
        
        total_customers = result.get('totalCustomers', 0)
        total_orders = result.get('totalOrders', 0)
        total_revenue = result.get('totalRevenue', 0)
        
        # Format revenue to 2 decimal places
        if total_revenue:
            revenue_str = f"{float(total_revenue):.2f}"
        else:
            revenue_str = "0.00"
        
        # Log the report
        report_message = (
            f"{timestamp} - Report: {total_customers} customers, "
            f"{total_orders} orders, {revenue_str} revenue\n"
        )
        
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(report_message)
        
        return {
            'success': True,
            'customers': total_customers,
            'orders': total_orders,
            'revenue': revenue_str
        }
    
    except Exception as e:
        # Log error if GraphQL query fails
        error_message = f"{timestamp} - Error generating report: {str(e)}\n"
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(error_message)
        return {
            'success': False,
            'error': str(e)
        }

