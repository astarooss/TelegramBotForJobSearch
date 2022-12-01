from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import date
from aiogram import Dispatcher, types

from create_bot import dp, bot
from data_base import ps2_client, ps2_rabota
from keyboards import kb_client_continue, kb_work, kb_work_foto
from handlers import client




class FSMRabota(StatesGroup): 
    id_foto = State()
    hesteg = State()
    description = State()
    price =  State()
    contacts = State()
    
    

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await client.menu_cancel(message)

async def cm_start2(message: types.Message):
    await FSMRabota.id_foto.set()
    await bot.send_message(message.from_user.id,'Отправте по желанию фотографию, или нажмите "Не добавлять фото"', reply_markup=kb_work_foto)

async def load_id_foto(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['id_foto'] = message.photo[-1].file_id
    except IndexError:
        async with state.proxy() as data:
            data['id_foto'] = 'NONE'
    await FSMRabota.next()
    await bot.send_message(message.from_user.id,'Введите тип работы, например "Бармен"', reply_markup=kb_work)

async def load_hesteg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hesteg'] = str(message.text)
    await FSMRabota.next()
    await bot.send_message(message.from_user.id,'Введите описание')



async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = str(message.text)
    await FSMRabota.next()
    await bot.send_message(message.from_user.id,'Введите цену')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = str(message.text)
    await FSMRabota.next()
    await bot.send_message(message.from_user.id,'Введите ваши контакты')


async def load_contacts(message: types.Message, state: FSMContext):      
    nm = await ps2_client.get_table_number(message.from_user.id)
    async with state.proxy() as data:
        data['contacts'] = str(message.text)
        data['id'] = str(message.from_user.id)
        data['id_work'] = str(message.from_user.id) + '_' + str(nm)
        data['date'] = str(date.today())
        data['active'] = '3'
    await ps2_rabota.sql_create_work(state)
    await ps2_client.update_table_number(message.from_user.id)
    await bot.send_message(message.from_user.id,'Анкета отправлена на проверку', reply_markup=kb_client_continue)
    await state.finish()





def register_handlers_work(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(cm_start2, Text(equals='Добавить вакансию', ignore_case=True))

    dp.register_message_handler(load_id_foto, state=FSMRabota.id_foto, content_types=['photo'])
    dp.register_message_handler(load_id_foto, state=FSMRabota.id_foto)
    dp.register_message_handler(load_hesteg, state=FSMRabota.hesteg)
    dp.register_message_handler(load_description, state=FSMRabota.description)
    dp.register_message_handler(load_price, state=FSMRabota.price)
    dp.register_message_handler(load_contacts, state=FSMRabota.contacts)
