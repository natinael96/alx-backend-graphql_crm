#!/bin/bash

# Script to clean up inactive customers with no orders since a year ago
# This script uses Django's manage.py shell to execute the cleanup

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the project root (assuming manage.py is in the parent of crm directory)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to project root directory
cd "$PROJECT_ROOT" || exit 1

# Execute the cleanup using Django shell
python manage.py shell << 'EOF'
import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Ensure Django is set up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from crm.models import Customer, Order

# Calculate the date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
# This includes customers with no orders at all, or whose last order was more than a year ago
customers_to_delete = Customer.objects.exclude(
    orders__created_at__gte=one_year_ago
).distinct()

# Count before deletion
count = customers_to_delete.count()

# Delete the customers
customers_to_delete.delete()

# Log the result
log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deleted {count} inactive customer(s) with no orders since {one_year_ago.strftime('%Y-%m-%d')}\n"

with open('/tmp/customer_cleanup_log.txt', 'a') as log_file:
    log_file.write(log_message)

print(f"Cleanup completed: {count} customer(s) deleted")
EOF

exit 0

