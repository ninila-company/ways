from telethon import TelegramClient
import os

# Получаем api_id и api_hash из переменных окружения (лучше для безопасности)
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = 'my_session'  # Файл сессии будет создан рядом с этим скриптом

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def send_telegram_message(user, message):
    """
    Отправляет сообщение в Telegram пользователю (по username или user_id).
    """
    await client.start()  # Убедимся, что клиент запущен
    await client.send_message(user, message)