from inspect import getfile
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, IDFilter, RegexpCommandsFilter
from states import Adding_query
from loader import dp
from utils.db_api.test_conn import get_list_oo, get_list_services
from keyboards.keyboard import kb_generator, cb_oo, cb_services
import logging
import pathlib
from random import randint
from datetime import datetime

# Start
@dp.message_handler(CommandStart(), IDFilter(('73053093', '73609237')))
async def bot_start(message: types.Message):
    await message.answer(f"Скажите название ОО (можно первые несколько букв).")
    await Adding_query.select_oo.set()


# Reset everywhere
@dp.message_handler(RegexpCommandsFilter([r'/reset']), state=Adding_query.all_states) #going to use filter Command("something")
async def add_photos(message: types.Message, state: FSMContext):
    await message.answer('Вы сбросили текущую заявку! Начните с начала, если хочется.')
    await state.finish()
    

# Select OO   
@dp.message_handler(state=Adding_query.select_oo)
async def select_oo(message: types.Message, state: FSMContext):
    matching_objects = get_list_oo(message.text)
    if not matching_objects:
        await message.answer(f"Такой ОО еще не открыли (или уже закрыли).")
    else:
        await message.answer(f"Уточните:", reply_markup=kb_generator(matching_objects, cb_oo))
        await Adding_query.select_service_stage1.set()


# Save oo and Select service      
@dp.callback_query_handler(cb_oo.filter(), state=Adding_query.select_service_stage1)
async def return_id_oo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(oo_id=callback_data.get("id"))
    services = get_list_services()
    await call.message.answer(f"Ты выбрал ОО @{callback_data.get('name')}@\nКто будет разгребать?", reply_markup=kb_generator(services, cb_services))
    await Adding_query.select_service_stage2.set()
    


# Save service and Input text
@dp.callback_query_handler(cb_services.filter(), state=Adding_query.select_service_stage2)
async def select_service(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(service_id=callback_data.get('id'))
    await call.message.answer("Введите тест заявки")
    await Adding_query.input_text.set()


# Save text and End-or-photos   
@dp.message_handler(state=Adding_query.input_text)
async def input_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text, user_id=message.from_user.id)
    await message.answer("Теперь добавьте фотографии или завершите создание заявки командой /end")
    await Adding_query.add_photos.set()
    

# End without photos
@dp.message_handler(RegexpCommandsFilter([r'/end']), state=Adding_query.add_photos) #debt: going to use filter Command("something")
async def add_photos(message: types.Message, state: FSMContext):
    await message.answer("Вы создали заявку!")
    # save to DB
    obj_for_DB = await state.get_data()
    logging.info(f"{obj_for_DB}")
    await state.finish()


#Photo 
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Adding_query.add_photos)
async def add_photos(message: types.Message, state: FSMContext):
    await message.answer("Вы создали заявку с фотографиями!")
    path_to_photodir = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("photos")
    path_to_localdir = str(datetime.now()).replace(':', '_').replace(' ', "_") + "_rn_" + str(randint(0, 9999))
    photoname = str(message.photo[0]["file_unique_id"]) + ".jpg"
    await message.photo[-1].download(destination_file=f"{path_to_photodir}\\{path_to_localdir}\\{photoname}") # ADD CORRECT PATH FOR LINUX
    await state.update_data(photopath=path_to_localdir)
    # logging.info(a)
    # save to DB
    obj_for_DB = await state.get_data()
    logging.info(f"{obj_for_DB}")
    await state.finish()
    # print(message.photo[0]["file_id"])
    

    


    