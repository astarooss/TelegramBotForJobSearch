from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import RetryAfter
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher, types


from create_bot import dp, bot
from data_base import ps2_client, ps2_msg, ps2_rabota
from keyboards import kb_admin_menu, kb_work_foto, kb_admin_where_post, kb_admin_check, kb_admin_rs, kb_admin_pass, kb_admin_cal
from handlers import client
from datetime import date, datetime
from config import HESHTEG, ADMIN_ID, VAKANSE
import asyncio




class FSMRedact(StatesGroup):
    hesteg = State()
    description = State()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await client.menu(message)
        return
    await state.finish()
    await client.menu(message)




async def load_hesteg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_work = data['id_work']
    await ps2_rabota.update_hesteg(id_work, message.text)
    await state.finish()
    await bot.send_message(message.from_user.id,'Успешно изменено')

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_work = data['id_work']
    await ps2_rabota.update_description(id_work, message.text)
    await state.finish()
    await bot.send_message(message.from_user.id,'Успешно изменено')




async def Admin_menu(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        works = await ps2_rabota.get_works('3')
        await bot.send_message(message.from_user.id, f'Заявок на публикацию: {len(works)}', reply_markup=kb_admin_menu)


async def work_p(message: types.Message, state: FSMContext ,wrr='3'):
    try:
        await state.finish()
        if message.from_user.id in ADMIN_ID:
            if message.text == 'Активные вакансии':
                wrr = '0'
            works = await ps2_rabota.get_works(wrr)
            works2 = await ps2_rabota.get_works('1')
            for a in works2:
                works.append(a)
            n = 0
            for work in works:
                if wrr == '3':
                    k1 = InlineKeyboardButton('Добавить', callback_data='wr1' + str(work[5]))
                    k2 = InlineKeyboardButton('Удалить', callback_data='wr2' + str(work[5]))
                    k3 = InlineKeyboardButton('Редактировать тип работы', callback_data='wr3' + str(work[5]))
                    k4 = InlineKeyboardButton('Редактировать описание', callback_data='wr5' + str(work[5]))
                    k5 = InlineKeyboardButton('Добавить в топ', callback_data='wr4' + str(work[5]))
                    kb_admin_work = InlineKeyboardMarkup()
                    kb_admin_work.add(k1).insert(k2).add(k3).add(k4).add(k5)
                    
                    n += 1
                    try:
                        if work[0] in HESHTEG.split(','):
                            if work[8] == 'NONE':
                                msg = await bot.send_message(message.from_user.id, f'💼Тип работы : {work[0]}\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                            else:
                                msg = await bot.send_photo(message.from_user.id ,photo=work[8],caption = f'💼Тип работы : {work[0]}\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                        else:
                            if work[8] == 'NONE':
                                msg = await bot.send_message(message.from_user.id, f'💼Тип работы: ❌{work[0]}❌\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                            else:
                                msg = await bot.send_photo(message.from_user.id ,photo=work[8],caption = f'💼Тип работы: ❌{work[0]}❌\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                    except Exception as _ex:
                        await bot.send_message(632567149, _ex)            
                elif wrr == '0':
                    try:
                        k2 = InlineKeyboardButton('Удалить', callback_data='wr2' + str(work[5]))
                        kb_admin_work = InlineKeyboardMarkup()
                        kb_admin_work.add(k2)
                        
                        n += 1
                        if work[8] == 'NONE':
                            msg = await bot.send_message(message.from_user.id, f'💼Тип работы: {work[0]}\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                        else:
                            msg = await bot.send_photo(message.from_user.id ,photo=work[8],caption = f'💼Тип работы: {work[0]}\n\n💵Цена: {work[2]}\n\n📋Описание: {work[1]}\n\n📩Контакты: {work[3]}\n\nДата публикации: {work[6]}', reply_markup=kb_admin_work)
                    except Exception as _ex:
                        await bot.send_message(632567149, _ex)  

                async with state.proxy() as data:
                    data[str(work[5])] = msg
                if n > 10:
                    break
    except Exception as _ex:
        print(_ex)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('wr'))
async def calback__handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            msg = data[callback.data[3:]]
            await msg.delete()
    except Exception as _ex:
        print(_ex, 'calback__handler')
    if callback.data[2] == '1':
        id_work = callback.data[3:]
        a = id_work.find('_')
        if await ps2_rabota.get_active(id_work) == '3':
            await ps2_rabota.post_in_channel(id_work)
            await bot.send_message(id_work[:a], text='Вакансия одобрена')
        await ps2_rabota.update_active(id_work, '0')
        await callback.answer(':)')

    elif callback.data[2] == '3':
        async with state.proxy() as data:
            data['id_work'] = callback.data[3:]
        await bot.send_message(callback.from_user.id, f'Введите новый тип работы для: ID {callback.data[3:]}')
        await FSMRedact.hesteg.set()
        await callback.answer()
        
    elif callback.data[2] == '2':
        id_work = callback.data[3:]
        await ps2_rabota.delete_column_active(id_work)
        await callback.answer(':(')

    elif callback.data[2] == '5':
        async with state.proxy() as data:
            data['id_work'] = callback.data[3:]
        await bot.send_message(callback.from_user.id, f'Введите новое описание для: ID {callback.data[3:]}')
        await FSMRedact.description.set()
        await callback.answer()
    
    else:
        id_work = callback.data[3:]
        if await ps2_rabota.get_active(id_work) == '3':
            await ps2_rabota.post_in_channel(id_work)
        await ps2_rabota.update_active(id_work, '1')
        await callback.answer(':)')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('dl'))
async def calback__handler(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data[2])
    if callback.data[2] == '1':
        await ps2_rabota.update_active(callback.data[3:], '2')
        await callback.answer('Удалено')
    await callback.answer()


async def statistic(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        count = await ps2_client.get_count()
        new_user = await ps2_client.get_new_user()
        active = await ps2_client.get_active()
        await message.answer(f'Пользователей за все времмя: {count}\nНовых пользователей за сегодня: {new_user}\nПримерный актив за сегодня: {active}')

async def scheduler(message, all_id):
    n = 0
    for ids in all_id:
        try:
            if len(message.text[17:]) > 5:
                await bot.send_message(ids, f'{message.text[17:]}')
                n += 1
        except RetryAfter as e:
            await asyncio.sleep(e.timeout + 1)
        except Exception as _ex1:
            await bot.send_message(message.from_user.id, str(_ex1)) 
        await asyncio.sleep(0.5)
    await bot.send_message(message.from_user.id, f'Отправлено {str(n)} пользователям')


    


async def send_message_all_users(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        all_id = await ps2_client.get_all_id()
        await bot.send_message(message.from_user.id, 'Начинаю рассылку')
        asyncio.create_task(scheduler(message=message, all_id=all_id))
        


        

async def get_anketa(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        try:
            res = await ps2_client.get_anketa()
            
            for a in res:
                if a[5] != 'NULL' or a[6] != 'NULL':
                    await bot.send_message(message.from_user.id, f'id: {a[0]}\nuser_name: @{a[1]}\nfull_name: {a[2]}\nВозраст: {a[3]}\nПол: {a[4]}\nНужна квартира: {a[5]}\nОпыт/Предпочтения: {a[6]}\nphone_number: {a[7]}\ndata_reg: {a[9]}\ndata_new: {a[10]}')
        except Exception as _ex:
            print(_ex)

@dp.message_handler(commands=['ads'])
async def ads(message: types.Message):
    await message.delete()
    try:
        all_id = await ps2_client.get_all_id()
            
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Перейти в бота', url='https://t.me/rabota_praha_bot')
        keyboard.add(button)

        if message.reply_to_message.from_user.id in all_id:
            if await ps2_client.get_table_number(message.reply_to_message.from_user.id) == 0:
                await bot.send_message(chat_id=message.chat.id, text='Вы так же можете воспользоваться нашим ботом для публикации своих вакансий в канале', reply_to_message_id=message.reply_to_message.message_id, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id, text='Вы так же можете воспользоваться нашим ботом для публикации своих вакансий в канале', reply_to_message_id=message.reply_to_message.message_id, reply_markup=keyboard)

    except Exception as _ex:
        print(_ex)


class FSMMsg(StatesGroup):
    id_foto = State()
    msg = State()
    datetime = State()
    link1 = State()
    link2 = State()
    where_post = State()
    the_end = State()
    check = State()
    redact_msg = State()

    

async def menu_rs(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(message.from_user.id,'Меню', reply_markup=kb_admin_rs)

async def cm_start_msg(message: types.Message):
    print(message)
    if message.from_user.id in ADMIN_ID:
        await FSMMsg.id_foto.set()
        await bot.send_message(message.from_user.id,'Отправте по желанию фотографию, или нажмите "Не добавлять фото"', reply_markup=kb_work_foto)

async def load_id_foto(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['id_foto'] = message.photo[-1].file_id
    except IndexError:
        async with state.proxy() as data:
            data['id_foto'] = 'NONE'
            
    await FSMMsg.next()
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Пример HTML разметки', url='https://guruweba.com/html/tegi-formatirovaniya-teksta-v-html/')
    keyboard.add(button)
    await bot.send_message(message.from_user.id,'Введите текст сообщения (разметка HTML)', reply_markup=keyboard)

async def load_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    await FSMMsg.next()
    await bot.send_message(message.from_user.id,'Введите время в виде "18:00, 19:00"', reply_markup=kb_admin_cal)
    
async def load_date_time(message: types.Message, state: FSMContext):
    if message.text.replace(':','').replace(',','').replace('.','').replace(' ','').isdigit():
        async with state.proxy() as data:
            data['date_time'] = message.text
        await FSMMsg.next()
        await bot.send_message(message.from_user.id,'введите сыллку и текст для кнопки, в виде "https://..., текст кнопки", или нажмите пропустить',reply_markup=kb_admin_pass)
    else:
        await FSMMsg.datetime()
        await bot.send_message(message.from_user.id,'Не коректный ввод\n\nВведите время в виде "18:00, 19:00"', reply_markup=kb_admin_cal)

async def load_link1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'пропустить':
            message_text = message.text.split(',')
            data['link1'] = message_text[0]
            data['textlink1'] = message_text[1]
        else:
            data['link1'] = 'NONE'
            data['textlink1'] = 'NONE'
    await FSMMsg.next()
    await bot.send_message(message.from_user.id,'введите вторую сыллку и текст для кнопки, в виде "https://..., текст кнопки", или нажмите пропустить')

async def load_link2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'пропустить':
            message_text = message.text.split(',')
            data['link2'] = message_text[0]
            data['textlink2'] = message_text[1]
        else:
            data['link2'] = 'NONE'
            data['textlink2'] = 'NONE'
    await FSMMsg.next()
    await bot.send_message(message.from_user.id,'Куда постить?', reply_markup=kb_admin_where_post)# 0 = в канал, 1 в канал с репостом в чат, 2 в чат, 10 = черновик

async def load_where_post(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'В канал':
            data['where_post'] = 0

        elif message.text == 'В канал с репостом в чат':
            data['where_post'] = 1

        else:
            data['where_post'] = 2

    await bot.send_message(message.from_user.id,f'Введиту дату окончания в виде "03.01.2023"\nили нажмите кнопку "Пропустить"', reply_markup=kb_admin_pass)
    await FSMMsg.next()




async def load_the_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['the_end'] = "NONE"
        else:
            data['the_end'] = message.text

        if data['id_foto'] != 'NONE':
            if data['link1'] != 'NONE':
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(data['textlink1'], url=data['link1'])
                keyboard.add(button)
                if data['link2'] != 'NONE':
                    button2 = InlineKeyboardButton(data['textlink2'], url=data['link2'])
                    keyboard.add(button2)
                await bot.send_photo(chat_id=message.from_user.id, photo=data['id_foto'], caption=data['msg'],parse_mode='HTML', reply_markup=keyboard)
            else:
                await bot.send_photo(chat_id=message.from_user.id, photo=data['id_foto'], caption=data['msg'],parse_mode='HTML')
        else:
            if data['link1'] != 'NONE':
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(data['textlink1'], url=data['link1'])
                keyboard.add(button)
                if data['link2'] != 'NONE':
                    button2 = InlineKeyboardButton(data['textlink2'], url=data['link2'])
                    keyboard.add(button2)
                await bot.send_message(chat_id=message.from_user.id, text=data['msg'],parse_mode='HTML', reply_markup=keyboard)
            else:
                await bot.send_message(chat_id=message.from_user.id, text=data['msg'],parse_mode='HTML')


            num = data['where_post']
            if num == 0:
                where = 'В канал'
            elif num == 1:
                where = 'В канал с репостом в чат'
            else:
                where = 'В чат'
            end = data['the_end']
            if end == "NONE":
                end = 'Отсутствует'
        await bot.send_message(message.from_user.id,f'Время публикаций: {data["date_time"]}\nКуда: {where}\nВремя окончания: {end}', reply_markup=kb_admin_check)
    await FSMMsg.next()

async def load_check(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        await ps2_msg.sql_add_command(message.from_user.id, state)
        await state.finish()

    elif message.text == 'Сохранить как черновик':
        async with state.proxy() as data:
            data['where_post'] = 10 
            await ps2_msg.sql_add_command(message.from_user.id, state)

    elif message.text == 'Редактировать текст':
        async with state.proxy() as data:
            await FSMMsg.redact_msg.set()
            await bot.send_message(message.from_user.id, f'{data["msg"]}', parse_mode='HTML')
            await bot.send_message(message.from_user.id, 'Отправте отредактированое сообщение')

async def load_redact_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    

    if data['id_foto'] != 'NONE':
        if data['link1'] != 'NONE':
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(data['textlink1'], url=data['link1'])
            keyboard.add(button)
            if data['link2'] != 'NONE':
                button2 = InlineKeyboardButton(data['textlink2'], url=data['link2'])
                keyboard.add(button2)
            bot.send_photo(chat_id=message.from_user.id, photo=data['id_foto'], caption=data['msg'],parse_mode='HTML', reply_markup=keyboard)
        else:
            bot.send_photo(chat_id=message.from_user.id, photo=data['id_foto'], caption=data['msg'],parse_mode='HTML')
    else:
        if data['link1'] != 'NONE':
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(data['textlink1'], url=data['link1'])
            keyboard.add(button)
            if data['link2'] != 'NONE':
                button2 = InlineKeyboardButton(data['textlink2'], url=data['link2'])
                keyboard.add(button2)
            bot.send_message(chat_id=message.from_user.id, text=data['msg'],parse_mode='HTML', reply_markup=keyboard)
        else:
            bot.send_message(chat_id=message.from_user.id, text=data['msg'],parse_mode='HTML')


    num = data['where_post']
    if num == 0:
        where = 'В канал'
    elif num == 1:
        where = 'В канал с репостом в чат'
    else:
        where = 'В чат'
   
    end = data['the_end']
    if end == "NONE":
        end = 'Отсутствует'
    await FSMMsg.check.set()
    await bot.send_message(message.from_user.id,f'Время публикаций: {data["date_time"]}\nКуда: {where}\nВремя окончания: {end}', reply_markup=kb_admin_check)
    
    



async def send_message_to_chat(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Канал с вакансиями', url='https://t.me/work_in_prague')
        keyboard.add(button)
        link_page = hlink('ботом', 'https://t.me/rabota_praha_bot')
        await bot.send_message(chat_id=-1001869904593, text = f'В этом чате публикации <b>бесплатные</b>, так же можно пользоваться ссылками\n\nИщете работу? воспользуйтесь нашим {link_page}, в нём можно искать работу по категориям, все новые вакансии публикуются в канал', reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)
        


    

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(send_message_to_chat, commands=['SqS'])
    dp.register_message_handler(cancel_handler, Text(equals=('отмена', 'Отмена', 'Отменить'), ignore_case=True), state="*")
    


    dp.register_message_handler(cm_start_msg, Text(equals=('Добавить новую рассылку')))
    dp.register_message_handler(load_id_foto, state=FSMMsg.id_foto, content_types=['photo','text'])
    dp.register_message_handler(load_msg, state=FSMMsg.msg)
    dp.register_message_handler(load_date_time, state=FSMMsg.datetime)
    dp.register_message_handler(load_link1, state=FSMMsg.link1)
    dp.register_message_handler(load_link2, state=FSMMsg.link2)
    dp.register_message_handler(load_where_post, state=FSMMsg.where_post)
    dp.register_message_handler(load_the_end, state=FSMMsg.the_end)
    dp.register_message_handler(load_check, state=FSMMsg.check)
    dp.register_message_handler(load_msg, state=FSMMsg.redact_msg)


    dp.register_message_handler(load_hesteg, state=FSMRedact.hesteg)
    dp.register_message_handler(load_description, state=FSMRedact.description)
    dp.register_message_handler(Admin_menu, Text(equals='Админ меню'))
    dp.register_message_handler(send_message_all_users, commands=['send_message_all'])
    dp.register_message_handler(get_anketa, commands=['get_anketa'])
    dp.register_message_handler(statistic, Text(equals='Статистика'))
    dp.register_message_handler(work_p, Text(equals=('Активные вакансии','Предложка')))
    dp.register_message_handler(menu_rs, Text(equals=('Рассылки')))


    
