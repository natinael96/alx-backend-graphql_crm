# CRM Celery Setup Guide

This guide explains how to set up and run Celery with Celery Beat for generating weekly CRM reports.

## Prerequisites

- Python 3.8+
- Redis server
- Django project dependencies installed

## Installation Steps

### 1. Install Redis

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### On macOS:
```bash
brew install redis
brew services start redis
```

#### On Windows:
Download and install Redis from [https://redis.io/download](https://redis.io/download) or use WSL.

### 2. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Django
- Celery
- django-celery-beat
- Redis client
- GraphQL libraries
- Other dependencies

### 3. Run Migrations

Apply database migrations to set up the necessary tables:

```bash
python manage.py migrate
```

This will create tables for:
- Django models (Customer, Order, Product)
- django-celery-beat periodic task schedules

### 4. Start Redis Server

Ensure Redis is running on `localhost:6379`:

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

If Redis is not running, start it:

```bash
# On Linux/macOS
redis-server

# On Windows (if installed)
redis-server
```

### 5. Start Celery Worker

In a terminal, start the Celery worker:

```bash
celery -A crm worker -l info
```

The worker will:
- Connect to Redis broker
- Process tasks from the queue
- Execute `generate_crm_report` task when scheduled

### 6. Start Celery Beat

In another terminal, start Celery Beat (the scheduler):

```bash
celery -A crm beat -l info
```

Celery Beat will:
- Schedule the `generate_crm_report` task to run every Monday at 6:00 AM
- Send tasks to the Celery worker via Redis

### 7. Verify Logs

Check the report log file to verify the task is running:

```bash
# View the log file
cat /tmp/crm_report_log.txt

# Or on Windows (Git Bash)
cat /tmp/crm_report_log.txt

# Or tail to watch in real-time
tail -f /tmp/crm_report_log.txt
```

The log file should contain entries in the format:
```
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

## Running in Development

For development, you can run both worker and beat in the same process:

```bash
celery -A crm worker --beat -l info
```

## Troubleshooting

### Redis Connection Error
- Ensure Redis is running: `redis-cli ping`
- Check Redis is listening on `localhost:6379`
- Verify firewall settings if using remote Redis

### Task Not Executing
- Check Celery worker is running and connected
- Verify Celery Beat is running
- Check Django settings for `CELERY_BEAT_SCHEDULE`
- Review worker logs for errors

### GraphQL Endpoint Not Available
- Ensure Django development server is running: `python manage.py runserver`
- Verify GraphQL endpoint is accessible at `http://localhost:8000/graphql`
- Check GraphQL schema includes `totalCustomers`, `totalOrders`, and `totalRevenue` queries

### Log File Not Created
- Check write permissions for `/tmp/` directory
- On Windows, ensure the path is accessible or modify the log path in `tasks.py`

## Schedule Configuration

The report is scheduled to run every Monday at 6:00 AM UTC. To modify the schedule, edit `crm/settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

## Production Deployment

For production:
1. Use a process manager (supervisor, systemd) to manage Celery processes
2. Configure Redis persistence
3. Set up monitoring and alerting
4. Use a proper logging system instead of file-based logs
5. Configure proper security settings for Redis

