from aiogram.fsm.state import StatesGroup, State

class CreateDog(StatesGroup):
    choosing_dog_pk = State()
    choosing_dog_name = State()
    choosing_dog_type = State()


class SearchDog(StatesGroup):
    choosing_dog_pk = State()


class UpdateDog(StatesGroup):
    choosing_dog_pk = State()
    updating_fields = State()
    updating_dog_kind = State()
    updating_dog_name = State()


class AddTimestamp(StatesGroup):
    choosing_id = State()
    choosing_timestamp = State()