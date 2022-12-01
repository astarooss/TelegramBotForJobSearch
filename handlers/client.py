from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date
from aiogram import Dispatcher, types

from handlers.admin import ADMIN_ID
from create_bot import dp, bot
from data_base import ps2_client, ps2_rabota
from keyboards import kb_client_start, kb_client_pass, kb_client_continue, kb_client_menu, kb_gender, kb_fuski_yes, kb_yes_no, kb_client_menu_с, kb_admin_menu_2, kb_client_menu_anketa, kb_client_menu_hesteg, kb_client_start_2
from config import HESHTEG





class FSMAdmin(StatesGroup): 
    full_name = State()
    age = State()
    gender = State()
    flat = State()
    practice = State()
    phone_number = State()






async def cm_start(message: types.Message):
    await FSMAdmin.full_name.set()
    await bot.send_message(message.from_user.id,'Введите ваше имя', reply_markup=kb_client_pass)

async def load_full_name(message: types.Message):
    try:
        if message.text == 'Прoпустить':
            pass
        else:
            await ps2_client.update_full_name(message.from_user.id, message.text)
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,'Введите ваш возраст', reply_markup=kb_client_pass)
    except:
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,'Введите ваш возраст', reply_markup=kb_client_pass)
        

async def load_age(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Прoпустить':
            pass
        else: 
            await ps2_client.update_age(message.from_user.id, message.text)
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Выберете ваш пол', reply_markup=kb_gender) 
    except:
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,'Выберете ваш пол', reply_markup=kb_gender)
        

async def load_gender(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Прoпустить':
            pass
        else:
            await ps2_client.update_gender(message.from_user.id, message.text)
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Вам нужно предоставить квартиру?', reply_markup=kb_yes_no)
    except:
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Вам нужно предоставить квартиру?', reply_markup=kb_yes_no)

async def load_flat(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Прoпустить':
            pass
        else:
            await ps2_client.update_flat(message.from_user.id, message.text)
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Oпишите какую работу вы ищете, опыт работы, т.д.', reply_markup=kb_client_pass) 
    except:
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Oпишите какую работу вы ищете, опыт работы, т.д.', reply_markup=kb_client_pass)

async def load_practice(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Прoпустить':
            pass
        else:
            await ps2_client.update_practice(message.from_user.id, message.text)
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Введите ваш номер телефона (Мы свяжемся с вами в Viber/WatsAp), когда подберем вам работу', reply_markup=kb_client_pass) 
    except:
        await FSMAdmin.next() 
        await bot.send_message(message.from_user.id,'Введите ваш номер телефона (Мы свяжемся с вами в Viber/WatsAp), когда подберем вам работу', reply_markup=kb_client_pass) 

async def load_phone_number(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Прoпустить':
            pass
        else:
            await ps2_client.update_phone_number(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id,'Анкета создана', reply_markup=kb_client_continue)
        await state.finish()
    except:
        await bot.send_message(message.from_user.id,'Анкета создана', reply_markup=kb_client_continue)
        await state.finish()





async def start(message : types.Message, state: FSMContext):
    if await ps2_client.check_id(message.from_user.id):
        await menu(message)
    else:
        async with state.proxy() as data:
            data['id'] = message.from_user.id
            data['user_name'] = message.from_user.username
            data['full_name'] = "NULL"
            data['age'] = -1
            data['gender'] = "NULL"
            data['flat'] = "NULL"
            data['practice'] = "NULL"
            data['phone_number'] = "NULL"
            data['fuski'] = 0
            data['data_reg'] = str(date.today())
            data['data_new'] = str(date.today())
            data['works_number'] = 0
            data['table_number'] = 0
        await ps2_client.sql_add_command(state)
        await state.finish()
        await bot.send_message(message.from_user.id, 'Вы работодатель или вы ищете работу?', reply_markup=kb_client_start_2)
        
    


async def send_contact(message: types.Message):
    await bot.send_message(message.from_user.id, 'Наши контакты:\nViber/WatsApp: +420775695185\nTelegram: @Ts_denya\nКанал: https://t.me/work_in_prague', reply_markup=kb_client_continue, disable_web_page_preview=True)

async def rabota(message: types.Message):
    n, nn = await ps2_rabota.get_my_work_list_number(message.from_user.id)
    nst = ' '
    if int(n) > 0:
        await bot.send_message(message.from_user.id, f'Количество ваших вакансий: {n}\nВакансий на рассмотрении: {nn}\n\n *Правила:* https://telegra.ph/Pravila-razmeshcheniya-vakansij-09-11', reply_markup=kb_client_menu_с, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await bot.send_message(message.from_user.id, f'*Пожалуйста посмотрите на пример и правила перед публикацией вакансии:* https://telegra.ph/Pravila-razmeshcheniya-vakansij-09-11', reply_markup=kb_client_menu_с, parse_mode='Markdown', disable_web_page_preview=True)
    


async def job_menu(message: types.Message):
    works_number = await ps2_rabota.get_works('0')
    await bot.send_message(message.from_user.id, f'Доступных вакансий: {len(works_number)}', reply_markup=kb_client_menu_hesteg)

async def hesteg_menu(message: types.Message, hestegs=HESHTEG):
    reply = []
    for hesteg in hestegs.split(','):
        hg = await ps2_rabota.get_hesteg_number(hesteg)
        if hg:  
            reply.append(InlineKeyboardButton(hesteg + ': ' + str(hg), callback_data='hg' + hesteg))
            
    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(*reply)
    works_number = await ps2_rabota.get_works('0')
    await bot.send_message(message.from_user.id, f'Доступных вакансий: {len(works_number)}', reply_markup=reply_markup)



@dp.callback_query_handler(lambda x: x.data and x.data.startswith('hg'))
async def calback__handler(callback: types.CallbackQuery):
    await ps2_rabota.get_hesteg_list(callback.from_user.id, callback.data[2:])
    await callback.answer()



async def send_job(message: types.Message):
    await ps2_rabota.get_work_list(message.from_user.id)

async def my_works(message: types.Message):
    await ps2_rabota.get_my_work_list(message.from_user.id)


async def menu(message: types.Message):
    
    try:
        await ps2_client.update_data_new(message.from_user.id)
    except Exception as _ex:
        print(_ex)
    try:
        await ps2_client.update_works_number(message.from_user.id, 0)
    except Exception as _ex:
        print(_ex)
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(message.from_user.id, 'Описание работы бота:\n\n -"Меню Вакансий" Показ актуальных вакансий\n\n -"Для работодателей" В этом разделе можно добавить свою вакансию в бота и каннал\n\n -"Помощь в поиске работы" В этом разделе можно связатся с нами или заполнить/изменить свою анкету\n\nКанал в котором публикуются все вакансии: https://t.me/work_in_prague \n\nТак же у нас есть чат в котором можно публиковать свои товары, услуги, или просто общатся: https://t.me/praha_rabota_chat', reply_markup=kb_admin_menu_2,  disable_web_page_preview=True)
    else:
        await bot.send_message(message.from_user.id, 'Описание работы бота:\n\n -"Вакансии" Показ актуальных вакансий\n\n -"Для работодателей" В этом разделе можно добавить свою вакансию в бота и каннал\n\n -"Помощь в поиске работы" В этом разделе можно связатся с нами или заполнить/изменить свою анкету\n\nКанал в котором публикуются все вакансии: https://t.me/work_in_prague \n\nТак же у нас есть чат в котором можно публиковать свои товары, услуги, или просто общатся: https://t.me/praha_rabota_chat', reply_markup=kb_client_menu,  disable_web_page_preview=True)

async def menu_vakanse(message: types.Message):
    await bot.send_message(message.from_user.id, f'*Наша компания специализируется на помощи в поиске работы*\n\nТак же мы помогаем *переехать в Чехию*, *предоставляем жилье и помогаем с изучением чешского*\n\n*Напишите/позвоните нам* или заполните анкету если в начале пропустили её', reply_markup=kb_client_menu_anketa, parse_mode="Markdown")
    
    

async def menu_cancel(message: types.Message):
    await menu(message)




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_message_handler(cm_start, Text(equals=('Изменить анкету', 'Заполнить анкету'), ignore_case=True), state="*")
    dp.register_message_handler(load_full_name, state=FSMAdmin.full_name)
    dp.register_message_handler(load_age, state=FSMAdmin.age) 
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_flat, state=FSMAdmin.flat)
    dp.register_message_handler(load_practice, state=FSMAdmin.practice)
    dp.register_message_handler(load_phone_number, state=FSMAdmin.phone_number)

    dp.register_message_handler(job_menu, Text(equals=('Меню вакансий','Я ищу работу'), ignore_case=True))
    dp.register_message_handler(hesteg_menu, Text(equals='Выбрать тип работы', ignore_case=True))
    dp.register_message_handler(rabota, Text(equals=('Для работодателей', 'Я работодатель'), ignore_case=True))
    dp.register_message_handler(my_works, Text(equals='Мои вакансии', ignore_case=True))
    dp.register_message_handler(send_job, Text(equals=('Показать новые', 'Дальше'), ignore_case=True))
    dp.register_message_handler(send_contact, Text(equals=('Связатся с нами', 'Наши контакты'), ignore_case=True))
    dp.register_message_handler(menu, Text(equals=('Пропустить', 'Продолжить', 'меню', '/menu', 'Отмена', 'Меню'), ignore_case=True))
    dp.register_message_handler(menu_vakanse, Text(equals='Помощь в поиске работы', ignore_case=True))

    
