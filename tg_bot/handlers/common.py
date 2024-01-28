from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram import Router, types
import httpx

from tg_bot.keyboards.utils import get_start_kb
from tg_bot.config import FASTAPI_URL

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    async with httpx.AsyncClient() as client:
        request_url = FASTAPI_URL + "/"
        response = await client.get(request_url)
    if response.status_code == 200:
        await message.reply(
            text=response.json()['message'],
            reply_markup=get_start_kb()
        )
    else:
        await message.reply(
            text='Sorry, the service is not available at this moment, please try again later',
        )