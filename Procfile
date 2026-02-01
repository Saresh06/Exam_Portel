release: python manage.py migrate
web: gunicorn Exam_portel.wsgi:application --bind 0.0.0.0:$PORT