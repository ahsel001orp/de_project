from sys import path
from os import getenv
path.append(f'{getenv("de_project_dir")}/utils/')
from vac_downloader import VacDownloader as VacDown
from click_house_db import ClickHouseDB as ClickHouse
from tg_bot import run_send_message_to_autor
from datetime import datetime, timedelta
from pendulum import timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


args = {
    'owner': 'de_engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 12, tzinfo=timezone('Europe/Moscow')),
    'catchup': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'max_active_runs': 1
}

# Скачиваем новые вакансии по запросам профессий из списка и сохраняем их в БД
def get_vacancies():
    with open(f'{getenv("de_project_dir")}/professions.txt', encoding='utf-8' ) as professions:
        for profession in professions.readlines():
            VD = VacDown(profession.replace('\n',''))
            VD.get_IDs()
            VD.get_all_pages_id()
            VD.get_all_vacancies()
            VD.insert_vacancies()
            VD.close()
            print(VD.err)
            tg_str = f'{profession}\nВсего нашлось - {VD.count_vac}\nДобавлено новых - {VD.cont_new_vac}\n'\
                f'Количество ID к которым добавлена 2 профессия - {VD.count_same_vac}\n{VD.err}'
            if len(tg_str)>4000:
                run_send_message_to_autor(f'''
                {profession}\nВсего нашлось - {VD.count_vac}\nДобавлено новых - {VD.cont_new_vac}
                Количество ID к которым добавлена 2 профессия - {VD.count_same_vac}\n!!!БЫЛО МНОГО ОШИБОК - СМОТРИ ЛОГ!!!
                ''')
            else: run_send_message_to_autor(tg_str)
        

# Отправляем новые вакансии из финтеха автору
def send_new_vacancies():
    CH = ClickHouse()
    new_vacances = CH.get_new_fin_vacances()
    for vacancy in new_vacances:
        run_send_message_to_autor(f'{vacancy[1]} - {vacancy[2]} - {vacancy[3][0].split(":")[1]}\nhttps://hh.ru/vacancy/{vacancy[0]}')
    CH.close_connection()

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

    send_new_vacancies = PythonOperator(
        task_id='send_new_vacancies',
        python_callable=send_new_vacancies,
    )

    end = EmptyOperator(
        task_id='end',
    )

    get_vacancies >> send_new_vacancies >> end

# if __name__ == '__main__':
#     get_vacancies()
    #send_new_vacancies()
