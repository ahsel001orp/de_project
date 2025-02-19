from app.api.get_html import *
#from get_html import *
from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

# from sys import path
# path.append('D:/projects/de_project/utils')
from utils.click_house_db import ClickHouseDB as CHDB
from utils.tg_bot import send_to_autor_from_fastapi


router = APIRouter(prefix='', tags=['API'])
cli_db = CHDB()

@router.get('/')
async def get_main_page(request: Request):    
    return HTMLResponse(content=get_html_skill_frequency(cli_db.get_skill_frequency()), status_code=200)

@router.get('/vacancies')
async def get_vacancies_page(request: Request):
    return HTMLResponse(content=get_vacancies_html(cli_db.get_vacancies(k_s), k_s), status_code=200)

@router.get('/vacancy_id')
async def get_vacancies_page(request: Request):
    return HTMLResponse(content=get_vacancy_html(cli_db.get_vacancy(request.query_params['id']),request.query_params['id']),status_code=200)

@router.get('/about')
async def get_about_page(request: Request):
    return HTMLResponse(content=get_html_body('about'), status_code=200)

@router.get('/passport_instructions')
async def get_passport_instructions_page(request: Request):    
    return HTMLResponse(content=get_html_body('old_instructions/Инструкция_по_проверке_паспортов_utf8'), status_code=200)

@router.get('/smp_service')
async def get_smp_service_page(request: Request):
    return HTMLResponse(content=get_html_body('old_instructions/СМП_для_ЦБ'), status_code=200)

@router.get('/contacts')
async def get_contacts_page(request: Request):
    return HTMLResponse(content=get_html_body('contacts'), status_code=200)

@router.post('/send_message')
async def send_message( req: Request,
                       name: str = Body(embed=True),
                       tg: str = Body(embed=True),
                       message: str = Body(embed=True)
                       ):
    cli_db.insert_messages([[req.client.host,name,tg,message]])
    if send_to_autor_from_fastapi(message)==200: return JSONResponse(content=jsonable_encoder({"ID": "OK"}))
    else: return JSONResponse(content=jsonable_encoder({"ID": "ERROR"}))


if __name__ == '__main__':
    get_html_skill_frequency(cli_db.get_skill_frequency())