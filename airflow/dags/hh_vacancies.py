from sys import path
path.append('/home/prostoleha/de_project/utils')
from vac_downloader import VacDownloader as VacDown
from click_house_db import ClickHouseDB as ClickHouse
from datetime import datetime, timedelta
from pendulum import timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


args = {
    'owner': 'de_engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 3, tzinfo=timezone('Europe/Moscow')),
    'catchup': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'max_active_runs': 1
}

def get_vacancies():
    # vacancies = 'data engineer'
    vacancies = 'python data backend'
    VD = VacDown(vacancies)
    VD.get_IDs()
    VD.get_all_pages_id()
    VD.get_all_vacancies()
    VD.close()
    with open ('/home/prostoleha/de_project/dw_result.txt', 'w') as dw_res:
        dw_res.write(VD.err)
        dw_res.write(f'\nВсего нашлось - {VD.count_vac}')
        dw_res.write(f'\nДобавлено новых - {VD.cont_new_vac}')
        dw_res.write(f'\nКоличество ID к которым добавлена 2 профессия - {VD.count_same_vac}')

def write_clickhouse():
    CH = ClickHouse()
    skills = CH.get_count_skills()
    with open ('/home/prostoleha/de_project/dw_result.txt', 'a') as dw_res:
        for skill in skills:
            dw_res.write(f'\n{skill[0]} - {skill[1]}')

with DAG(
        dag_id='hh_vacancies',
        schedule_interval='10 8 * * *',
        default_args=args,
        tags=['hh_vacancies', 'de_engineer'],
        description='',
        concurrency=1
) as dag:

    get_vacancies = PythonOperator(
        task_id='get_vacancies',
        python_callable=get_vacancies
    )

    write_clickhouse = PythonOperator(
        task_id='write_clickhouse',
        python_callable=write_clickhouse,
    )

    end = EmptyOperator(
        task_id='end',
    )

    get_vacancies >> write_clickhouse >> end