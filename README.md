### DE_project
Это приложение для мониторинга сайта [HeadHunter](https://hh.ru) с поиском новых вакансий по заданным профессиям. 
С помощью [airflow](https://airflow.apache.org/) происходит скачивание новых вакансий по списку профессий перечисленных в файле [professions.txt](https://github.com/ahsel001orp/de_project/blob/master/professions.txt), с их последующем сохранением в [clickhouse](https://clickhouse.com/), и уведомление пользователя в телеграм о ходе выполнения.
У системы есть web представление реализованное на [fastapi](https://fastapi.tiangolo.com/), его можно посмотреть по [ссылке](http://193.149.129.51:5069/)
#### Установка и запуск
1) Установите [clickhouse](https://clickhouse.com/docs/install). Во время установки не меняйте порт по умолчанию и сохраните пароль от пользователя default - он понадобится для инициализации новой схемы в БД.
2) Для корректной работы airflow рекомендую установить [postgresql](https://www.postgresql.org/). После установки необходимо подготовить базу для работы с airflow выполнив команды
```
sudo -iu postgres psql -c "CREATE DATABASE airflow;"
sudo -iu postgres psql -c "CREATE USER airflow WITH PASSWORD 'your password';"
sudo -iu postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;"
```
3) Клонируйте данный репозиторий:
```
git clone https://github.com/ahsel001orp/de_project
``` 
4) Запустите [скрипт](https://github.com/ahsel001orp/de_project/blob/master/set_environ_lin.sh), чтобы добавить в систему необходимые переменные среды
```
./set_environ_lin.sh
ch_db_password - пароль от схемы проекта в clickhouse (любой)
ch_db_default_pass - проль от пользователя default заданный при установке clickhouse 
tg_token - токен от телеграм бота
autor_tg_id - id пользоввателя телеграмм, который будет получать сообщения
de_project_dir - путь до директории в которую вы клонировали репозиторий
local_ip - ip машины на которой развернуто приложение
remote_ip - ip VPS сервера принимающего запросы к web интерфейсу (при наличии)
``` 
5) Создайте виртуальное окружение и установите зависимости
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
6) Установите airflow
```
# Устанавливаем в папку проекта
export AIRFLOW_HOME=$de_project_dir/airflow
# Берем из https://pypi.org/project/apache-airflow/
AIRFLOW_VERSION=2.10.4
# Версия python
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" 
# Команда pip
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install apache-airflow[postgres]
```
7) Перед запуском airflow поменяйте используемую БД на postgresql из пункта 2, для этого замените в файле конфигурации ($de_project_dir/airflow/airflow.cfg) строку:
```
sql_alchemy_conn = postgresql+psycopg2://airflow:your_password@localhost/airflow
```
8) Поменяйте executor для одного хоста и инициализируйте БД
```
executor = LocalExecutor 
airflow db init
```
9) Создайте пользователя web интерфейса:
```
airflow users create \
--username admin \
--password your_password \
--firstname your_firstname \
--lastname your_lastname \
--role Admin \
--email your_email
```
10) В новом окне терминала запускаем [скрипт](https://github.com/ahsel001orp/de_project/blob/master/start_de_project.sh) (для локального запуска закомментируйте строку с ssh туннелем)
```
./start_de_project.sh
```
