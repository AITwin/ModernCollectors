# Modern Collectors

## Run celery

celery -A ModernCollectors worker -l info -S django
celery -A ModernCollectors beat -l info -S django
