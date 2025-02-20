#!/bin/bash
export AIRFLOW_HOME=$de_project_dir/airflow
gnome-terminal -e ./start_scheduler.sh
gnome-terminal -e ./start_webserver.sh
source venv/bin/activate
uvicorn app.main:app --reload --host 192.168.0.12 --port 5069
