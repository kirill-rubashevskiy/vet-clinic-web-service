from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import httpx

from tg_bot.states.states import AddTimestamp
from tg_bot.keyboards.utils import get_start_kb, get_dog_type_kb
from tg_bot.config import FASTAPI_URL


router = Router()

@router.callback_query(F.data == "get_post")
async def create_dog(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.message.reply(
        text="Please, choose timestamp id"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(AddTimestamp.choosing_id)


@router.message(AddTimestamp.choosing_id,
                F.text.regexp(r'^\d+$'))
async def id_chosen(message: Message, state: FSMContext):
    await state.update_data(id=int(message.text))
    await message.reply(
        text="Thank you. Please, choose timestamp")
    await state.set_state(AddTimestamp.choosing_timestamp)


@router.message(AddTimestamp.choosing_timestamp,
                F.text.regexp(r'^\d+$'))
async def timestamp_chosen(message: Message, state: FSMContext):
    await state.update_data(timestamp=int(message.text))
    new_timestamp_data = await state.get_data()
    async with httpx.AsyncClient() as client:
        response = httpx.post(f'{FASTAPI_URL}/post',
                              json=new_timestamp_data)
    if response.status_code == 200:
        response = response.json()
        await message.reply(
            text=f"Timestamp {response['timestamp']} with id {response['id']} has been added"
        )

    await state.clear()
    await message.answer(
        text='Is there anything i can help?',
        reply_markup=get_start_kb()
    )