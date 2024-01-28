from aiogram import F, Router, types
import httpx

from tg_bot.keyboards.utils import get_start_kb
from tg_bot.config import FASTAPI_URL


router = Router()

@router.callback_query(F.data == "get_dog")
async def get_dog(callback: types.CallbackQuery):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{FASTAPI_URL}/dog')
    if response.status_code == 200:
        await callback.message.answer(
            text=response.text
        )
    await callback.message.answer(
        text='Is there anything i can help?',
        reply_markup=get_start_kb()
    )