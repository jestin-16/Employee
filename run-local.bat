@echo off
echo Starting EMS Container Virtualization Dashboard locally...
python manage.py migrate
python seed_data.py
python manage.py runserver 0.0.0.0:8000

