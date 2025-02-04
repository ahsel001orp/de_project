from os import makedirs
from sys import version

# airflow нужна отдельная директория
AIRFLOW_HOME='airflow'
try: 
    makedirs(AIRFLOW_HOME, 0o766)
except FileExistsError as e:
    print('Папка уже существует')

# Новую версию airflow берем с https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html
AIRFLOW_VERSION='2.10.4'
# python --version | cut -d " " -f 2 | cut -d "." -f 1-2
PYTHON_VERSION=version[:4]
CONSTRAINT_URL=f"https://raw.githubusercontent.com/apache/airflow/constraints-{AIRFLOW_VERSION}/constraints-{PYTHON_VERSION}.txt"
print(CONSTRAINT_URL)
#pip install f"apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"