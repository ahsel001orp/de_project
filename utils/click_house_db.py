from clickhouse_connect import get_client, driver

# Класс для работы с ClickHouse
class ClickHouseDB:

    def __init__(self):
        try:
            self.client = get_client(host='localhost', username='data_engineer', port=8123, password='your_password')
        except driver.exceptions.DatabaseError as e:
            self.init_db()

    def init_db(self):
        client = get_client(host='localhost', username='default', port=8123, password='your_def_password', )
        client.command("CREATE USER data_engineer IDENTIFIED BY 'duarF101'")
        client.command('CREATE DATABASE IF NOT EXISTS de_project')
        client.command('GRANT ALL ON de_project.* TO data_engineer WITH GRANT OPTION')
        client.close_connections()
        self.client = get_client(host='localhost', username='data_engineer', port=8123, password='your_password')
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

    def insert_vacancies(self, vacancies: list):
        self.client.insert('de_project.vacancies', vacancies,
                            column_names=['id', 'name', 'req_time', 'publicationDate', 'company_name',
                            'company_visible_name', 'company_site_url', 'area_name', 'description',
                            'key_skills', 'compensation', 'translation'])

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

    # Для тестирования
    def get_query(self, ex_str: str) -> list:
        return self.client.query(ex_str).result_rows

    # Переинициализировать таблицы
    def rebuild_table(self):
        self.client.command('ALTER TABLE de_project.vacancies DELETE WHERE 1=1')
        self.client.command('ALTER TABLE de_project.ids_from_req_profession DELETE WHERE 1=1')
        self.client.command('DROP TABLE IF EXISTS de_project.vacancies')
        self.client.command('DROP TABLE IF EXISTS de_project.ids_from_req_profession')
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

    # Частота встречаемости ключевых навыков        
    def get_count_skills(self) -> list:
        return self.get_query('''
                        SELECT
                            element,
                            COUNT(*) AS count
                        FROM
                        (
                            SELECT arrayJoin(key_skills) AS element
                            FROM de_project.vacancies
                        )
                        GROUP BY element
                        ORDER BY count DESC
                        ''')
    
    def close_connection(self):
        self.client.close_connections()
  

if __name__ == '__main__':
    CH = ClickHouseDB()
    print(CH.get_count_skills())
    #CH.get_old_prof_ids('data engineer')
    # for skill in CH.get_count_skills():
    #     print(skill)

    # CH.rebuild_table()
    # print(CH.get_query('SELECT * FROM de_project.vacancies'))
    # print(CH.get_query('SELECT * FROM de_project.ids_from_req_profession'))
    CH.close_connection()
