import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, create_dog, get_dog, get_dog_by_pk, update_dog, get_post
from config import BOT_TOKEN

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(
    common.router,
    create_dog.router,
    get_dog.router,
    get_dog_by_pk.router,
    update_dog.router,
    get_post.router
)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())