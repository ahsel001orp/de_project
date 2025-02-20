#!/bin/bash
cd $de_project_dir
source venv/bin/activate
export AIRFLOW_HOME=$de_project_dir/airflow
airflow webserver --port 8080
