from clickhouse_connect import get_client, driver
from os import getenv

# Класс для работы с ClickHouse
class ClickHouseDB:

    # Перед запуском убедитесь, что в переменные среды добавлены 
    # ch_db_password - пароль от пользователя data_engineer
    # ch_db_default_pass - пароль от пользователя default, 
    # который вы задали при установке ClickHouse 
    # Пароли можно задать запустив set_environ_win.bat для Windows
    # или set_environ_lin.sh для Linux (устанавливает в переменные пользователя)
    def __init__(self):
        try:
            self.client = get_client(host='localhost', username='data_engineer', port=8123, password=getenv('ch_db_password'))
        except driver.exceptions.DatabaseError as e:
            self.init_db()

    # Инициализация БД
    def init_db(self):
        client = get_client(host='localhost', username='default', port=8123, password=getenv('ch_db_default_pass') )
        client.command(f"CREATE USER data_engineer IDENTIFIED BY '{getenv('ch_db_password')}'")
        client.command('CREATE DATABASE IF NOT EXISTS de_project')
        client.command('GRANT ALL ON de_project.* TO data_engineer WITH GRANT OPTION')
        client.close_connections()
        self.client = get_client(host='localhost', username='data_engineer', port=8123, password=getenv('ch_db_password'))
        self.init_tables()

    def init_tables(self):
        # Основная таблица с вакансиями
        self.client.command('''CREATE TABLE IF NOT EXISTS de_project.vacancies (
                    id UInt32, name String, req_time DateTime('Europe/Moscow'),
                    publicationDate DateTime('Europe/Moscow'), company_name String,
                    company_visible_name String, company_site_url String,
                    area_name String, description String, key_skills Array(String),
                    compensation Array(String), translation Array(String)) 
                    ENGINE = MergeTree() ORDER BY (id, req_time, publicationDate)'''
                    )
        # Таблица для учета одинаковых вакансий, возвращающихся по разным профессиям
        self.client.command('''
                    CREATE TABLE IF NOT EXISTS de_project.ids_from_req_profession (
                    id UInt32, req_profession String) ENGINE = MergeTree() ORDER BY id
                    ''')
        # Таблица для хранения сообщений от гостей
        self.client.command('''
                    CREATE TABLE IF NOT EXISTS de_project.messages_to_autor (
                    ip String, name String, tg String, message String) ENGINE = MergeTree() ORDER BY ip
                    ''')

    def insert_vacancies(self, vacancies: list):
        self.client.insert('de_project.vacancies', vacancies,
                            column_names=['id', 'name', 'req_time', 'publicationDate', 'company_name',
                            'company_visible_name', 'company_site_url', 'area_name', 'description',
                            'key_skills', 'compensation', 'translation'])
        
    def insert_messages(self, messages: list):
        self.client.insert('de_project.messages_to_autor', messages,
                            column_names=['ip', 'name', 'tg', 'message'])

    # Для исключения  повторяющихся вакансий       
    def get_old_ids(self) ->  list:
        old_ids = []
        result_rows = self.get_query('SELECT id FROM de_project.vacancies')
        for row in result_rows:
            old_ids.append(str(row[0]))        
        return old_ids
    
    # Для учета одинаковых вакансий по разным профессиям
    def get_old_prof_ids(self, professin: str) -> tuple[list,list]:
        old_ids = []
        same_ids = []
        result_rows = self.get_query(f"SELECT id FROM de_project.ids_from_req_profession WHERE req_profession != '{professin}'")
        same_result = self.get_query(f"SELECT id FROM de_project.ids_from_req_profession WHERE req_profession = '{professin}'")
        for row in result_rows:
            old_ids.append(str(row[0]))
        for row in same_result:
            same_ids.append(str(row[0]))
        return (old_ids,same_ids)
    
    def insert_prof(self, ids: list, profession: str):
        prepared = []
        for id in ids:
            prepared.append([id,profession])
        self.client.insert('de_project.ids_from_req_profession', prepared,
                            column_names=['id', 'req_profession'])

    # Для получения записей из БД
    def get_query(self, ex_str: str) -> list:
        return self.client.query(ex_str).result_rows

    # Переинициализировать таблицы
    def rebuild_table(self):
        self.client.command('ALTER TABLE de_project.vacancies DELETE WHERE 1=1')
        self.client.command('ALTER TABLE de_project.ids_from_req_profession DELETE WHERE 1=1')
        self.client.command('ALTER TABLE de_project.messages_to_autor DELETE WHERE 1=1')
        self.client.command('DROP TABLE IF EXISTS de_project.vacancies')
        self.client.command('DROP TABLE IF EXISTS de_project.ids_from_req_profession')
        self.client.command('DROP TABLE IF EXISTS de_project.messages_to_autor')
        self.init_tables()

    # Удаление дубликатов на этапе тестирования
    def delete_main_duplicate(self):
        self.client.command('''
                            ALTER TABLE de_project.vacancies DELETE WHERE id in (
                            SELECT id FROM de_project.vacancies
                            GROUP BY id
                            HAVING COUNT(id)>1
                            )
                            ''')

    # Частота встречаемости ключевых навыков по профессиям
    def get_skill_frequency(self) -> list:
        result = []
        for profession in self.get_query('select distinct req_profession from de_project.ids_from_req_profession'):
            result.append({profession[0] : 
                           self.get_query(f'''
                        SELECT element, COUNT(1) AS count FROM
                        ( SELECT arrayJoin(key_skills) AS element
                            FROM de_project.vacancies WHERE id IN
                              (SELECT id FROM de_project.ids_from_req_profession 
                              WHERE req_profession='{profession[0]}'))
                        GROUP BY element ORDER BY count DESC LIMIT 20
                        ''')})
        return result

    # Вакансии для соответствующей html страницы
    def get_vacancies(self, in_key_skills: list) -> list:
        return self.get_query(f'''
                    SELECT 
                    length(arrayIntersect(key_skills, {in_key_skills})) AS intersect_count,
                    id, name, formatDateTime(publicationDate,'%d.%m.%Y'), company_visible_name,
                    company_site_url, area_name, key_skills ,translation FROM de_project.vacancies
                    HAVING intersect_count>2 ORDER BY toDayOfYear(publicationDate) DESC, 
                    intersect_count DESC, translation LIMIT 50
                    ''') 

    # Описание вакансии для соответствующей html страницы
    def get_vacancy(self, id: str) -> list:
        return self.get_query(f'SELECT company_visible_name, description from de_project.vacancies WHERE id={id}')

    # Для отправки в телеграм новых вакансий от финтех компаний  
    def get_new_fin_vacances(self) -> list:
        return self.get_query('''
                    SELECT id, name, company_name, translation FROM de_project.vacancies
                    WHERE toDate(req_time)=toDate(now()) AND
                    multiSearchFirstIndex(lower(description),['fintech','финтех'])>0
                    ORDER BY translation, publicationDate DESC
                    ''')
    
    def close_connection(self):
        self.client.close_connections()
  

if __name__ == '__main__':
    pass
    # CH = ClickHouseDB()
    # print(CH.get_query('SELECT * FROM de_project.messages_to_autor '))
    # CH.close_connection()
