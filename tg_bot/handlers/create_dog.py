from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import httpx

from tg_bot.states.states import CreateDog
from tg_bot.keyboards.utils import get_start_kb, get_dog_type_kb
from tg_bot.config import FASTAPI_URL


router = Router()

@router.callback_query(F.data == "create_dog")
async def create_dog(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.message.reply(
        text="Please, choose new patient pk number"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreateDog.choosing_dog_pk)


@router.message(CreateDog.choosing_dog_pk,
                F.text.regexp(r'^\d+$'))
async def pk_chosen(message: Message, state: FSMContext):
    async with httpx.AsyncClient() as client:
        request_url = f'{FASTAPI_URL}/dog/{int(message.text)}'
        response = await client.get(request_url)
    if response.status_code == 200:
        await state.clear()
        await message.reply(
            text=f"Dog with pk {message.text} already exists. Please, choose another pk."
        )
        await message.answer(
            text='Is there anything i can help?',
            reply_markup=get_start_kb()
        )
    elif response.status_code == 404:
        await state.update_data(pk=int(message.text))
        await message.reply(
            text="Thank you. Please, choose new patient name")
        await state.set_state(CreateDog.choosing_dog_name)


@router.message(CreateDog.choosing_dog_name)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(
        text="Thank you. Please, choose new patient type",
        reply_markup=get_dog_type_kb()
        )
    await state.set_state(CreateDog.choosing_dog_type)


@router.callback_query(CreateDog.choosing_dog_type, F.data.startswith('dog_type_'))
async def dog_type_chosen(callback: types.CallbackQuery,
                        state: FSMContext):
    await state.update_data(kind=callback.data.removeprefix('dog_type_'))
    new_dog_data = await state.get_data()
    async with httpx.AsyncClient() as client:
        response = httpx.post(f'{FASTAPI_URL}/dog',
                              json=new_dog_data)
    if response.status_code == 200:
        response = response.json()
        await callback.message.reply(
            text=f"New patient {response['kind']} {response['name']} has been added"
        )

    await state.clear()
    await callback.message.answer(
        text='Is there anything i can help?',
        reply_markup=get_start_kb()
    )

