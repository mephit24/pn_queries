from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, IDFilter, RegexpCommandsFilter
from states import Adding_query
from loader import dp, DB_CREDIENTALS, tgusers
from utils.db_api.test_conn import get_list_oo, get_list_services, add_query_to_DB
from keyboards.keyboard import kb_generator, cb_oo, cb_services
import logging
import pathlib
from random import randint
from datetime import datetime
import asyncio
import nest_asyncio
nest_asyncio.apply()


# Start
@dp.message_handler(CommandStart(), IDFilter(tgusers))
async def bot_start(message: types.Message):
    await message.answer(f"Скажите название ОО (можно первые несколько букв).")
    await Adding_query.select_oo.set()


# Ignore /start in any state   
@dp.message_handler(CommandStart(), state = Adding_query.all_states)
async def bot_start_everywhere(message: types.Message):
    pass


# Reset everywhere
@dp.message_handler(RegexpCommandsFilter([r'/reset']), state = Adding_query.all_states) #debt: going to use filter Command("something") instead of RegexphotocounterommandsFilter
async def reset(message: types.Message, state: FSMContext):
    await message.answer('Вы сбросили текущую заявку! Начните с начала, если хочется.')
    await state.finish()


# Select OO   
@dp.message_handler(state = Adding_query.select_oo)
async def select_oo(message: types.Message, state: FSMContext):
    matching_objects = get_list_oo(message.text, DB_CREDIENTALS)
    if not matching_objects:
        await message.answer(f"Такой ОО еще не открыли (или уже закрыли).")
    else:
        await message.answer(f"Уточните:", reply_markup = kb_generator(matching_objects, cb_oo))
        await Adding_query.select_service_stage1.set()


# Save oo and Select service      
@dp.callback_query_handler(cb_oo.filter(), state = Adding_query.select_service_stage1)
async def return_id_oo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(oo_id = callback_data.get("id"))
    services = get_list_services(DB_CREDIENTALS)
    await call.message.answer(f"Ты выбрал ОО @{callback_data.get('name')}@\nКто будет разгребать?", reply_markup=kb_generator(services, cb_services))
    await Adding_query.select_service_stage2.set()


# Save service and Input text
@dp.callback_query_handler(cb_services.filter(), state = Adding_query.select_service_stage2)
async def select_service(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(service_id = callback_data.get('id'))
    await call.message.answer("Введите тест заявки")
    await Adding_query.input_text.set()


# Save text and End-or-photos   
@dp.message_handler(state = Adding_query.input_text)
async def input_text(message: types.Message, state: FSMContext):
    await state.update_data(text = message.text, user_id = message.from_user.id)
    await message.answer("Теперь добавьте фотографии или завершите создание заявки командой /end")
    await state.update_data(photocounter = 0)
    path_to_localdir = str(datetime.now()).replace(':', '_').replace(' ', "_") + "_rn_" + f"{randint(0, 9999):04d}"
    await state.update_data(path_to_localdir = path_to_localdir)
    await Adding_query.add_photos.set()


# End without photos
@dp.message_handler(RegexpCommandsFilter([r'/end']), state=Adding_query.add_photos) #debt: wanna use filter Command("something") instead of RegexphotocounterommandsFilter
async def or_photos(message: types.Message, state: FSMContext):
    obj_for_DB  =  await state.get_data()
    asyncio.get_event_loop().run_until_complete(add_query_to_DB(obj_for_DB, DB_CREDIENTALS))
    logging.info(f"{obj_for_DB}")
    await state.finish()
    await message.answer("Вы создали заявку!")


# Photos
@dp.message_handler(content_types = types.ContentType.PHOTO, state = Adding_query.add_photos)
async def add_photos(message: types.Message, state: FSMContext):
    # Download photos to dir
    path_to_photodir = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("photos") # get path to dir photo
    photoname = str(message.photo[0]["file_unique_id"]) + ".jpg"
    statedata = await state.get_data()
    photocounter = int(statedata["photocounter"])
    path_to_localdir = statedata["path_to_localdir"]
    if photocounter < 2:
        await message.photo[-1].download(destination_file = f"{path_to_photodir}\\{path_to_localdir}\\{photoname}") # debt: ADD CORRECT PATH FOR LINUX
        await state.update_data(photocounter = photocounter + 1)
        await message.answer("Фотография добавлена")
    else:
        await message.photo[-1].download(destination_file = f"{path_to_photodir}\\{path_to_localdir}\\{photoname}")
        obj_for_DB = await state.get_data()
        asyncio.get_event_loop().run_until_complete(add_query_to_DB(obj_for_DB, DB_CREDIENTALS))
        logging.info(f"{obj_for_DB}")
        await state.finish()
        await message.answer("Вы создали заявку с фотографиями!")
