# ALX Backend GraphQL CRM

A Django-based Customer Relationship Management (CRM) system with GraphQL API, automated cron jobs, and Celery task scheduling.

## Features

- **GraphQL API**: Full GraphQL schema with queries and mutations
- **Customer Management**: Track customers, orders, and products
- **Automated Tasks**: 
  - Customer cleanup (inactive customers)
  - Order reminders
  - Product stock alerts
  - Weekly CRM reports
- **Scheduled Jobs**: Using django-crontab and Celery Beat
- **Health Monitoring**: Heartbeat logging system

## Project Structure

```
alx-backend-graphql_crm/
├── crm/                    # Main Django app
│   ├── models.py           # Customer, Order, Product models
│   ├── schema.py           # GraphQL schema and mutations
│   ├── cron.py             # Django-crontab jobs
│   ├── tasks.py            # Celery tasks
│   ├── celery.py           # Celery configuration
│   ├── cron_jobs/          # Shell scripts and crontab entries
│   │   ├── clean_inactive_customers.sh
│   │   ├── send_order_reminders.py
│   │   └── *.txt           # Crontab configuration files
│   └── README.md           # Celery setup guide
├── manage.py
├── requirements.txt
└── README.md               # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The GraphQL endpoint will be available at: `http://localhost:8000/graphql`

## GraphQL API

### Queries

- `hello`: Simple health check query
- `products`: List all products
- `customers`: List all customers
- `orders`: List all orders
- `totalCustomers`: Get total customer count
- `totalOrders`: Get total order count
- `totalRevenue`: Get total revenue from all orders

### Mutations

- `updateLowStockProducts`: Updates products with stock < 10 by incrementing stock by 10

### Example Query

```graphql
query {
  totalCustomers
  totalOrders
  totalRevenue
}
```

### Example Mutation

```graphql
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
```

## Scheduled Tasks

### Django-Crontab Jobs

1. **Heartbeat Logger** (`crm.cron.log_crm_heartbeat`)
   - Runs every 5 minutes
   - Logs to `/tmp/crm_heartbeat_log.txt`

2. **Low Stock Updates** (`crm.cron.update_low_stock`)
   - Runs every 12 hours
   - Updates products with stock < 10
   - Logs to `/tmp/low_stock_updates_log.txt`

### Shell Scripts

1. **Customer Cleanup** (`crm/cron_jobs/clean_inactive_customers.sh`)
   - Runs every Sunday at 2:00 AM
   - Deletes customers with no orders since a year ago
   - Logs to `/tmp/customer_cleanup_log.txt`

2. **Order Reminders** (`crm/cron_jobs/send_order_reminders.py`)
   - Runs daily at 8:00 AM
   - Sends reminders for orders from the last 7 days
   - Logs to `/tmp/order_reminders_log.txt`

### Celery Tasks

1. **Weekly CRM Report** (`crm.tasks.generate_crm_report`)
   - Runs every Monday at 6:00 AM
   - Generates report with total customers, orders, and revenue
   - Logs to `/tmp/crm_report_log.txt`

For detailed Celery setup instructions, see [crm/README.md](crm/README.md).

## Setting Up Scheduled Tasks

### Django-Crontab

1. Add cron jobs to crontab:
```bash
python manage.py crontab add
```

2. Show current cron jobs:
```bash
python manage.py crontab show
```

3. Remove cron jobs:
```bash
python manage.py crontab remove
```

### Celery

1. Install and start Redis (see [crm/README.md](crm/README.md))

2. Start Celery worker:
```bash
celery -A crm worker -l info
```

3. Start Celery Beat:
```bash
celery -A crm beat -l info
```

For complete Celery setup instructions, see [crm/README.md](crm/README.md).

## Models

### Customer
- `name`: Customer name
- `email`: Unique email address
- `created_at`, `updated_at`: Timestamps

### Order
- `customer`: Foreign key to Customer
- `total_amount`: Decimal field for order total
- `created_at`, `updated_at`: Timestamps

### Product
- `name`: Product name
- `stock`: Integer field for inventory
- `price`: Decimal field for price
- `created_at`, `updated_at`: Timestamps

## Log Files

All scheduled tasks log to `/tmp/` directory:

- `/tmp/crm_heartbeat_log.txt` - Heartbeat logs
- `/tmp/customer_cleanup_log.txt` - Customer cleanup logs
- `/tmp/order_reminders_log.txt` - Order reminder logs
- `/tmp/low_stock_updates_log.txt` - Stock update logs
- `/tmp/crm_report_log.txt` - Weekly report logs

## Requirements

- Python 3.8+
- Django 4.2+
- Redis (for Celery)
- PostgreSQL/SQLite (SQLite by default)

## Dependencies

See `requirements.txt` for complete list. Key dependencies:

- Django
- graphene-django
- celery
- django-celery-beat
- django-crontab
- gql
- redis

## Development

### Running Tests

```bash
python manage.py test
```

### Accessing Admin Panel

1. Create superuser: `python manage.py createsuperuser`
2. Start server: `python manage.py runserver`
3. Visit: `http://localhost:8000/admin`

## License

This project is part of the ALX Backend curriculum.
