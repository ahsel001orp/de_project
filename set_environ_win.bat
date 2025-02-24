echo off
setlocal enableextensions enabledelayedexpansion
chcp 65001
for %%i in (ch_db_password ch_db_default_pass tg_token autor_tg_id de_project_dir local_ip remote_ip) do (
     if defined %%i ( echo Переменная %%i уже существует, для редактирования используете: 'setx %%i') else (
    echo введите значение %%i:& set /p my_var=
    setx %%i !my_var!
    echo "%%i = !my_var!" )
     )
echo Не забудте обновить оболочку для корректного чтения переменных