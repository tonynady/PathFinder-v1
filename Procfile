web: daphne PathFinder_V1.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=PathFinder_V1.settings -v2