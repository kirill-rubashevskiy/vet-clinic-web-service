from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import httpx

from tg_bot.config import FASTAPI_URL
from tg_bot.keyboards.utils import get_start_kb, get_dog_type_kb, get_dog_update_kb
from tg_bot.states.states import UpdateDog


router = Router()


@router.callback_query(F.data == "update_dog")
async def create_dog(callback: types.CallbackQuery,
                     state: FSMContext):
    await callback.message.reply(
        text="Please, choose patient pk number"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(UpdateDog.choosing_dog_pk)


@router.message(UpdateDog.choosing_dog_pk,
                F.text.regexp(r'^\d+$'))
async def pk_chosen(message: Message, state: FSMContext):
    async with httpx.AsyncClient() as client:
        request_url = f'{FASTAPI_URL}/dog/{int(message.text)}'
        response = await client.get(request_url)
    if response.status_code == 200:
        await state.update_data(response.json())
        await message.reply(
            text="Thank you. Please, choose fields to update",
            reply_markup=get_dog_update_kb()
        )
        await state.set_state(UpdateDog.updating_fields)
    elif response.status_code == 404:
        await state.clear()
        await message.reply(
            text=f"Dog with pk {message.text} not found"
        )
        await message.answer(
            text='Is there anything i can help?',
            reply_markup=get_start_kb()
        )


@router.callback_query(UpdateDog.updating_fields,
                       F.data == 'update_name')
async def updating_name(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.message.reply(
        text="Please, enter new name",
    )
    await state.set_state(UpdateDog.updating_dog_name)


@router.message(UpdateDog.updating_dog_name)
async def name_updated(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(
        text="Thank you. Please, choose new step",
        reply_markup=get_dog_update_kb()
        )
    await state.set_state(UpdateDog.updating_fields)


@router.callback_query(UpdateDog.updating_fields,
                       F.data == 'update_kind')
async def updating_kind(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.message.reply(
        text="Please, enter select new kind",
        reply_markup=get_dog_type_kb()
    )
    await state.set_state(UpdateDog.updating_dog_kind)


@router.callback_query(UpdateDog.updating_dog_kind, F.data.startswith('dog_type_'))
async def dog_kind_updated(callback: types.CallbackQuery,
                           state: FSMContext):
    await state.update_data(kind=callback.data.removeprefix('dog_type_'))
    await callback.message.reply(
        text="Thank you. Please, choose new step",
        reply_markup=get_dog_update_kb()
    )
    await state.set_state(UpdateDog.updating_fields)


@router.callback_query(UpdateDog.updating_fields,
                       F.data == 'complete_update')
async def complete_update(callback: types.CallbackQuery,
                          state: FSMContext):
    dog_updated_data = await state.get_data()
    response = httpx.patch(f'{FASTAPI_URL}/dog/{str(dog_updated_data["pk"])}',
                           json=dog_updated_data)
    if response.status_code == 200:
        await callback.message.reply(
            text=response.text
        )

    await state.clear()
    await callback.message.answer(
        text='Is there anything i can help?',
        reply_markup=get_start_kb()
    )