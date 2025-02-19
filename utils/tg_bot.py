from os import getenv
from telegram import Bot
from asyncio import run
from requests import get

<<<<<<< HEAD
token = 'your_token'
=======
>>>>>>> 849772a... вынес пароли в переменные среды, добавил комментарии

# Отправить сообщение автору
async def send_message_to_autor(message: str) -> str:
    bot = Bot(getenv("tg_token"))
    async with bot:
        return await bot.send_message(chat_id=getenv("autor_tg_id"), text=message)

# Запустить асинхронную отправку
def run_send_message_to_autor(message: str) -> str:
    return run(send_message_to_autor(message))

# Отправить сообщение без асинхронности
def send_to_autor_from_fastapi(message: str) -> int:
    return get(f'https://api.telegram.org/bot{getenv("tg_token")}/sendMessage?chat_id={getenv("autor_tg_id")}&text={message}').status_code


if __name__ == '__main__':
    run_send_message_to_autor('Приветик 👋')