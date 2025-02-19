from fastapi import FastAPI
from app.api.router import router
from fastapi.staticfiles import StaticFiles

# Запускаем FastAPI
app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), 'static')
app.include_router(router)