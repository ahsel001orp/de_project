from requests import session
from bs4 import BeautifulSoup as BS
from json import loads
from datetime import datetime
from click_house_db import ClickHouseDB as CHDB


url = 'https://hh.ru/vacancy'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
    
# Контроллер загрузки
class VacDownloader:
        
    def __init__(self, profession: str):
        self.profession = profession
        self.vacancies = []
        self.hh_session = session()
        self.vacancies_id = []
        self.page_num = 0
        self.cli_db = CHDB()
        self.err = ''
        self.count_vac = 0
        self.cont_new_vac = 0
        self.count_same_vac = 0
        self.new_prof_ids = []
        self.retry_ids = []

    # Собираем ID вакансий со страниц    
    def get_IDs(self):
        url_all_vac = f'{url}?text={self.profession}&schedule=remote&items_on_page=100&page={self.page_num}'        
        #print(url_all_vac)
        data = self.hh_session.get(url_all_vac,headers=headers)
        if data.status_code == 200:            
            json_vacancies = loads(BS(data.text, 'lxml').find('noindex').findChild('template').text)
            self.append_vacancies_id(dict(json_vacancies['userLabelsForVacancies']))        
            if self.page_num == 0:
                count_vac = int(json_vacancies['searchCounts']['value'])
                print(f'{self.profession} - {count_vac}')
                count_page = 0
                if (count_vac % 100 == 0) and (count_vac > 100): count_page = count_vac // 100 + 1
                elif count_vac > 100: count_page = count_vac // 100 + 2
                self.count_vac = count_vac
                self.page_num = count_page if count_page<=20 else 20
        else:
            self.close()
            self.err +=f'\nПри сборе вакансий со страницы {url_all_vac} код ответа не 200 - {data.status_code}'
            self.page_num = None

    # Получаем информацию о вакансии
    def get_vacancy(self, id: str):
        url_one_vac = f'{url}/{id}'
        #print(url_one_vac)
        vac = self.hh_session.get(url_one_vac,headers=headers)
        if vac.status_code == 200:
            check = BS(vac.text, 'lxml').find('noindex').findChild('template')
            if check is None: self.retry_ids.append(id)
            else: self.parse_vacancy(loads(check.text),id)
        else:
            if len(self.vacancies) > 0:
                self.insert_vacancies()
            self.close()
            self.err +=f'\nПри получении вакнсии {id} код ответа не 200 - {vac.status_code}'                                     
            self.page_num = None

    def parse_vacancy(self, json_vacancy: dict, id: str):
        compensation = []
        for k,v in json_vacancy['vacancyView']['compensation'].items():
            compensation.append(f'{k} : {v}')            
        translations = []
        for k,v in json_vacancy['vacancyView']['translations'].items():
            translations.append(f'{k} : {v}')
        if json_vacancy['vacancyView'].get('keySkills') is None:
            keySkill = []
        else: keySkill = json_vacancy['vacancyView']['keySkills']['keySkill']
        if json_vacancy['vacancyView']['company'].get('name') is None:
            company_name = ''
        else: company_name = json_vacancy['vacancyView']['company']['name']
        if json_vacancy['vacancyView']['company'].get('visibleName') is None:
            company_visibleName = ''
        else: company_visibleName = json_vacancy['vacancyView']['company']['visibleName']
        if json_vacancy['vacancyView']['company'].get('companySiteUrl') is None:
            company_companySiteUrl = ''
        else: company_companySiteUrl = json_vacancy['vacancyView']['company']['companySiteUrl']
        vacancy = [id, json_vacancy['vacancyView']['name'], datetime.now(),
                    datetime.strptime(json_vacancy['vacancyView']['publicationDate'],'%Y-%m-%dT%H:%M:%S.%f%z'),
                    company_name, company_visibleName, company_companySiteUrl,
                    json_vacancy['vacancyView']['area']['name'], json_vacancy['vacancyView']['description'],
                    keySkill, compensation, translations]
        self.vacancies.append(vacancy)
        self.new_prof_ids.append(id)

    # Перебераем все страницы
    def get_all_pages_id(self):
        if self.page_num != 0:
            all_pages = self.page_num
            for page in range(1,all_pages):
                self.page_num = page
                self.get_IDs()
        
    def append_vacancies_id(self, vacancies_dict : dict):
        for id in vacancies_dict: self.vacancies_id.append(id)

    # Собираем все вакансии
    def get_all_vacancies(self):
        old_prof_ids = self.cli_db.get_old_prof_ids(self.profession)
        old_ids = self.cli_db.get_old_ids()
        new_id = list(set(self.vacancies_id) - set(old_ids))
        self.cont_new_vac = len(new_id)
        same_id_prof = list((set(self.vacancies_id) & set(old_prof_ids[0]))-set(old_prof_ids[1]))
        self.count_same_vac = len(same_id_prof)
        self.cli_db.insert_prof(same_id_prof,self.profession)
        self.get_all_vacancies_loop(new_id)
        self.get_all_vacancies_loop(self.retry_ids)

    def get_all_vacancies_loop(self, ids: list):
        for_strict_loop = ids
        for id in for_strict_loop:
            try:
                self.get_vacancy(id)
            except Exception as e:
                self.insert_vacancies()
                self.err +=f' / Ошибка при получении вакансии - {str(e)}\n'\
                                     f'id - {id}'
                self.close()
                break

    # Записываем полученные вакансии в ClickHouse
    def insert_vacancies(self):
        self.cli_db.insert_vacancies(self.vacancies)
        self.cli_db.insert_prof(self.new_prof_ids,self.profession)
        
    def close(self):
        self.hh_session.close
        self.cli_db.close_connection()


if __name__ == '__main__':
    pass
    # vacancies = 'data engineer'
    # VD = VacDownloader(vacancies)    
    # VD.get_IDs()
    # VD.get_all_pages_id()
    # VD.get_all_vacancies()
    # VD.insert_vacancies()    
    # VD.close()
    # print(VD.err)
    # print(f'Всего нашлось - {VD.count_vac}')
    # print(f'Добавлено новых - {VD.cont_new_vac}')
    # print(f'Количество ID к которым добавлена 2 профессия - {VD.count_same_vac}')
    # VD.get_vacancy('116068295')
    # VD.close()
    # print(VD.err)
