from telegram import Bot
from asyncio import run, wait_for
from requests import get

token = 'your_token'

async def send_message_to_autor(message: str) -> str:
    bot = Bot(token)
    async with bot:
        return await bot.send_message(chat_id=700068700, text=message)

def run_send_message_to_autor(message: str) -> str:
    return run(send_message_to_autor(message))

def send_to_autor_from_fastapi(message: str) -> int:
    return get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id=700068700&text={message}').status_code


if __name__ == '__main__':
    run_send_message_to_autor('Приветик 👋')