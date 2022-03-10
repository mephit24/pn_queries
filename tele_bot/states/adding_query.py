from aiogram.dispatcher.filters.state import StatesGroup, State


class Adding_query(StatesGroup):
    button_start = State()
    select_oo = State()
    # select_oo_stage2 = State()
    select_service_stage1 = State()
    select_service_stage2 = State()
    input_text = State()
    add_photos = State()
    
    # test = State()
    
