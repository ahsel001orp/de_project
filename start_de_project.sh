#!/bin/bash
export AIRFLOW_HOME=$de_project_dir/airflow
gnome-terminal -e ./start_scheduler.sh
gnome-terminal -e ./start_webserver.sh
gnome-terminal -e "ssh -N -R $remote_ip:5069:$local_ip:5069 de_tunnel@$remote_ip -i $de_project_dir/ssh_keys/de_tunnel_key"
source venv/bin/activate
uvicorn app.main:app --reload --host $local_ip --port 5069
