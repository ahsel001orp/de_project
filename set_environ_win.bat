@echo off
chcp 65001
set /p ch_db_password=введите пароль для ch_db_password:
setx ch_db_password %ch_db_password%
set /p ch_db_default_pass=введите пароль для ch_db_default_pass:
setx ch_db_default_pass %ch_db_default_pass%
set /p tg_token=введите ваш token для телеграмм бота:
setx tg_token %tg_token%
set /p autor_tg_id=введите ваш ID (цифры) в телеграме, для получения пообщений от бота:
setx autor_tg_id %autor_tg_id%
set /p de_project_dir=домашнюю директорию проекта:
setx autor_tg_id %de_project_dir%