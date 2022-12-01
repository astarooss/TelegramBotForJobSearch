from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2 as ps
import os
import asyncio

from keyboards import kb_fuski_yes
from create_bot import bot
from data_base import ps2_client
from aiogram.utils.markdown import hlink

def sql_start_work():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print('Data base (works) connected OK!') 


async def sql_create_work(state):
    try:
        async with state.proxy() as data:
            cur.execute("INSERT INTO works (hesteg, description, price, contacts, id, id_work, date, active, id_foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(data['hesteg'], data['description'], data['price'], data['contacts'], data['id'], data['id_work'], data['date'], data['active'], data['id_foto']))
            base.commit()
            await bot.send_message(632567149,'+1 в предложке')
    except Exception as _ex:
        base.commit()
        await bot.send_message(632567149, str(_ex) + 'sql_create_work')

async def get_active(id_work):
    cur.execute('SELECT active FROM works WHERE id_work = %s', (id_work,))
    res = cur.fetchone()
    base.commit()
    return str(res[0])

async def update_active(id_work, active):
    cur.execute('UPDATE works SET active = %s WHERE id_work = %s', (int(active), id_work))
    base.commit()

async def get_works(number='2'):
    cur.execute('Select * From works WHERE active = %s', (number,))
    res = cur.fetchall()
    base.commit()
    return res
    
async def get_all_works():
    cur.execute('Select * From works')
    res = cur.fetchall()
    base.commit()
    return res

async def update_hesteg(id_work, hesteg):
    cur.execute('UPDATE works SET hesteg = %s WHERE id_work = %s', (hesteg, id_work))
    base.commit()

async def update_description(id_work, description):
    cur.execute('UPDATE works SET description = %s WHERE id_work = %s', (description, id_work))
    base.commit()


        
async def get_work_list(id):
    cur.execute('SELECT * FROM works WHERE active = %s', ('0',))
    works = cur.fetchall()
    base.commit()
    cur.execute('SELECT * FROM works WHERE active = %s', ('1',))
    works_top = cur.fetchall()
    base.commit()
    works.reverse()
    works_top.reverse()
    n = 1
    for wrt in works_top:
        works.insert(n,wrt)
        n += 2
    try:
        n = await ps2_client.get_works_number(id)
        for a in range(9):
            if works[n][8] == 'NONE':
                await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_fuski_yes)
            else:
                await bot.send_photo(id,photo=works[n][8],caption = f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}')
            n += 1
            if a == 8:
                
                if works[n][8] == 'NONE':
                    await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_fuski_yes)
                else:
                    await bot.send_photo(id,photo=works[n][8],caption = f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_fuski_yes)
                await ps2_client.update_works_number(id, works_number=n)
                test = works[n+1]
            await asyncio.sleep(0.3)
    except Exception as _ex:
        print(str(_ex) + '-- get_work_list')
        await ps2_client.update_works_number(id, works_number=0)

async def get_my_work_list_number(id):
    cur.execute('SELECT * FROM works WHERE id = %s', (str(id),))
    works = cur.fetchall()
    n = 0
    nn = 0
    for work in works:
        if work[7] == '0':
            n += 1
        elif work[7] == '3':
            nn += 1
    base.commit()
    return n, nn


async def post_in_channel(id_work):
    cur.execute('SELECT * FROM works WHERE id_work = %s',(id_work,))
    works = cur.fetchone()
    
    link = hlink('Работа в Праге, Чехии', 'https://t.me/work_in_prague')
    if works[8] == 'NONE':
        msg = await bot.send_message(chat_id=-1001509271122, text= f'💼Тип работы : #{works[0]}\n\n💵Цена: {works[2]}\n\n📋Описание: {works[1]}\n\n📩Контакты: {works[3]}\n\n{link}', parse_mode='HTML', disable_web_page_preview=True)
    else:
        msg = await bot.send_photo(chat_id=-1001509271122, photo=works[8], caption = f'💼Тип работы: #{works[0]}\n\n💵Цена: {works[2]}\n\n📋Описание: {works[1]}\n\n📩Контакты: {works[3]}\n\n{link}', parse_mode='HTML')
    await bot.forward_message(from_chat_id=-1001509271122, chat_id=-1001869904593, message_id=msg.message_id)



async def get_my_work_list(id):
    cur.execute('SELECT * FROM works WHERE id = %s', (str(id),))
    works = cur.fetchall()
    base.commit()
    works.reverse()
    try:
        if len(works) < 1:
            await bot.send_message(id, 'у вас нет вакансий, чтобы добавить нажмите "Добавить вакансию"')
            return
        n = await ps2_client.get_works_number(id)
        for a in range(9):
            if works[n][7] == '0':
                k22 = InlineKeyboardButton('Удалить', callback_data='dl1' + str(works[n][5]))
                kb_admin_work_2 = InlineKeyboardMarkup()
                kb_admin_work_2.add(k22)
                if works[n][8] == 'NONE':
                    await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_admin_work_2)
                else:
                    await bot.send_photo(id,photo=works[n][8],caption = f'Т💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_admin_work_2)

                if a == 8:
                    n += 1
                    test = works[n+1]
                    if works[n][8] == 'NONE':
                        await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_admin_work_2)
                    else:
                        await bot.send_photo(id,photo=works[n][8],caption = f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}', reply_markup=kb_admin_work_2)
                    await ps2_client.update_works_number(id, works_number=n)
                    await bot.send_message(id, f'Страница: {n}', reply_markup=kb_fuski_yes)
            await asyncio.sleep(0.3)
            n += 1
    except Exception as _ex:
        print(str(_ex) + '-- get_my_work_list')
        await ps2_client.update_works_number(id, works_number=0)

async def get_hesteg_list(id, hestegg):
    cur.execute('SELECT * FROM works WHERE hesteg = %s AND active = %s', (hestegg,'0'))
    works = cur.fetchall()
    base.commit()
    works.reverse()
    try:
        n = await ps2_client.get_works_number(id)
        for a in range(9):
            if works[n][7] == '0':
                if works[n][8] == 'NONE':
                    await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}')
                else:
                    await bot.send_photo(id,photo=works[n][8],caption = f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}')

                if a == 8:
                    n += 1
                    test = works[n+1]
                    if works[n][8] == 'NONE':
                        await bot.send_message(id, f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}')
                    else:
                        await bot.send_photo(id,photo=works[n][8],caption = f'💼Тип работы : {works[n][0]}\n\n💵Цена: {works[n][2]}\n\n📋Описание: {works[n][1]}\n\n📩Контакты: {works[n][3]}\n\nДата публикации: {works[n][6]}')
                    await ps2_client.update_works_number(id, works_number=n)
            await asyncio.sleep(0.3)
            n += 1
    except Exception as _ex:
        print(str(_ex) + '-- get_hesteg_list')
        await ps2_client.update_works_number(id, works_number=0)


async def get_hesteg_number(hestegg):
    cur.execute('SELECT * FROM works WHERE hesteg = %s', (hestegg,))
    res = cur.fetchall()
    hesteg = False
    try:
        if res[0][7] == '1' or res[0][7] == '0':
            hesteg = len(res)
        base.commit()
        if hesteg:
            return hesteg
        return False
    except:
        return False


async def delete_column_active(id_work):
    cur.execute('DELETE FROM works WHERE id_work = %s',(id_work,))
    base.commit()
async def delete_column_active_id():
    cur.execute('DELETE FROM works WHERE id_work = %s',('632567149_29'))
    base.commit()
        
