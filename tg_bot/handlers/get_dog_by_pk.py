from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import httpx

from tg_bot.keyboards.utils import get_start_kb
from tg_bot.config import FASTAPI_URL
from tg_bot.states.states import SearchDog


router = Router()

@router.callback_query(F.data == "get_dog_by_pk")
async def get_dog_by_pk(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.message.reply(
        text="Choose patient pk number"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(SearchDog.choosing_dog_pk)


@router.message(SearchDog.choosing_dog_pk,
                F.text.regexp(r'^\d+$'))
async def pk_chosen(message: Message, state: FSMContext):
    async with httpx.AsyncClient() as client:
        request_url = f'{FASTAPI_URL}/dog/{message.text}'
        response = await client.get(request_url)
    if response.status_code == 200:
        response = response.json()
        await message.reply(
            text=f"{response['kind']} {response['name']}"
        )
    elif response.status_code == 404:
        await message.reply(
            text=response.json()['detail']
        )

    await state.clear()
    await message.answer(
        text='Is there anything i can help?',
        reply_markup=get_start_kb()
    )