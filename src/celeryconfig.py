# src/celeryconfig.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
result_expires = 3600  # Keep task results for 1 hour
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'  # Or your desired timezone

# More advanced settings (optional):
# worker_prefetch_multiplier = 4  # Adjust based on task complexity
# worker_max_tasks_per_child = 100  # Prevent memory leaks
