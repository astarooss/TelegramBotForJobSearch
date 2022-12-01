import psycopg2 as ps
from create_bot import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from datetime import date
def sql_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print('Data base (user) connected OK!') 


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO anketa (id, user_name, full_name, age, gender, flat, practice, phone_number, fuski, data_reg, data_new, works_number, table_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(data['id'], data['user_name'], data['full_name'], data['age'], data['gender'], data['flat'], data['practice'], data['phone_number'], data['fuski'], data['data_reg'], data['data_new'], data['works_number'], data['table_number']))
        base.commit()

async def check_id(id):
    cur.execute('SELECT id FROM anketa')
    res = cur.fetchall()
    for ids in res:
        if id == ids[0]:
            return True
    return False

async def get_all_id():
    cur.execute('SELECT * FROM anketa')
    res = cur.fetchall()
    lists = []
    for a in res:
        lists.append(a[0])
    return lists

async def get_anketa():
    cur.execute('SELECT * FROM anketa')
    res = cur.fetchall()
    base.commit()
    return res


async def update_full_name(id, full_name):
    cur.execute('UPDATE anketa SET full_name = %s WHERE id = %s', (full_name, id))
    base.commit()

async def update_age(id, age):
    cur.execute('UPDATE anketa SET age = %s WHERE id = %s', (age, id))
    base.commit()

async def update_gender(id, gender):
    cur.execute('UPDATE anketa SET gender = %s WHERE id = %s', (gender, id))
    base.commit()

async def update_flat(id, flat):
    cur.execute('UPDATE anketa SET flat = %s WHERE id = %s', (flat, id))
    base.commit()

async def update_practice(id, practice):
    cur.execute('UPDATE anketa SET practice = %s WHERE id = %s', (practice, id))
    base.commit()

async def update_phone_number(id, phone_number):
    cur.execute('UPDATE anketa SET phone_number = %s WHERE id = %s', (phone_number, id))
    base.commit()

async def update_fuski(id, fuski):
    cur.execute('UPDATE anketa SET fuski = %s WHERE id = %s', (fuski, id))
    base.commit()

async def update_data_new(id):
    datee = str(date.today())
    cur.execute('UPDATE anketa SET data_new = %s WHERE id = %s', (datee, id))
    base.commit()

async def update_works_number(id, works_number):
    cur.execute('UPDATE anketa SET works_number = %s WHERE id = %s', (works_number, id))
    base.commit()



async def get_works_number(id):
    cur.execute('SELECT works_number FROM anketa WHERE id = %s', (id,))
    res = cur.fetchall()
    base.commit()
    return int(res[0][0])

async def get_table_number(id):
    base.commit
    cur.execute('SELECT table_number FROM anketa WHERE id = %s', (id,))
    res = cur.fetchall()
    base.commit()
    return res[0][0]

async def update_table_number(id):
    num = await get_table_number(id)
    num = int(num)
    cur.execute('UPDATE anketa SET table_number = %s WHERE id = %s', (int(num) + 1, id))
    base.commit()


async def get_count():
    cur.execute('SELECT count(*) FROM anketa')
    res = cur.fetchone()
    base.commit
    return res[0]

async def get_new_user():
    datee = date.today()
    cur.execute('SELECT * FROM anketa WHERE data_reg = %s',(str(datee),))
    res = cur.fetchall()
    base.commit
    return len(res)

async def get_active():
    datee = date.today()
    cur.execute('SELECT * FROM anketa WHERE data_new = %s',(str(datee),))
    res = cur.fetchall()
    base.commit
    return len(res)
    

