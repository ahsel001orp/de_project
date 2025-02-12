from pathlib import Path
from app.api.get_html import *
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.click_house_db import ClickHouseDB as CHDB


router = APIRouter(prefix='', tags=['API'])
templates = Jinja2Templates(directory='app/templates')
cli_db = CHDB()

def get_html_body(name: str) -> str:
    main_html = ''
    with open(Path(f'app/templates/{name}.html').resolve(), 'r', encoding='utf-8') as file:
        main_html = file.read()
    return head_footer['head'] + main_html + head_footer['footer']

@router.get('/')
async def get_main_page(request: Request):
    resp =get_html_body('index')
    return HTMLResponse(content=resp, status_code=200)

@router.get('/vacancies')
async def get_vacancies_page(request: Request):
    key_skils = [
    'Python','SQL','ETL','Linux',
    'Английский — B1 — Средний','Docker','Apache Airflow',
    'DWH','Git','ORACLE','Airflow','API','REST API', 'PostgreSQL'
    ]
    return HTMLResponse(content=get_vacancies_html(cli_db.get_vacancies(key_skils), key_skils), status_code=200)

@router.get('/vacancy_id')
async def get_vacancies_page(request: Request):
    return HTMLResponse(content=get_vacancy_html(cli_db.get_vacancy(request.query_params['id']),request.query_params['id']),status_code=200)

@router.get('/about')
async def get_about_page(request: Request):
    resp = get_html_body('about')
    return HTMLResponse(content=resp, status_code=200)

@router.get('/passport_instructions')
async def get_passport_instructions_page(request: Request):
    resp = get_html_body('old_instructions/Инструкция_по_проверке_паспортов_utf8')
    return HTMLResponse(content=resp, status_code=200)

@router.get('/smp_service')
async def get_smp_service_page(request: Request):
    resp = get_html_body('old_instructions/СМП_для_ЦБ')
    return HTMLResponse(content=resp, status_code=200)

@router.get('/contacts')
async def get_contacts_page(request: Request):
    resp = get_html_body('contacts')
    return HTMLResponse(content=resp, status_code=200)


if __name__ == '__main__':
    pass