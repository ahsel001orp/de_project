#!/bin/bash -i
source ~/.bashrc
for env in ch_db_password ch_db_default_pass tg_token autor_tg_id de_project_dir
do
if [ -v "${env}" ]; then
 echo "переменная $env уже существует:"
 printenv | grep $env
 echo "что бы её поменять отредактируйте ~/.bashrc"
else 
 echo "введите значение для $env:"
 read env_val
 echo "export $env=$env_val" >> ~/.bashrc
fi
done
echo ""
source ~/.bashrc
echo "Переменные для de_project:"
printenv | grep ch_db_password
printenv | grep ch_db_default_pass
printenv | grep tg_token
printenv | grep autor_tg_id
printenv | grep de_project_dir
echo "не забудте выполнить команду 'source ~/.bashrc'"
echo "что бы обновить bash оболочку!"