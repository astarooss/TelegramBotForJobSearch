from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2 as ps
import asyncio
import os

from create_bot import bot
from data_base import ps2_client
from handlers import work

def sql_start_msg():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print('Data base (msg) connected OK!') 


async def sql_add_command(id, state):
    async with state.proxy() as data:
        table_number = await ps2_client.get_table_number(id)
        await ps2_client.update_table_number()
        cur.execute("INSERT INTO msg (id_msg,             foto,         msg,         date_time,         link1,         link2,         textlink1,         textlink2,         where_post,         the_end) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                     (table_number, data['foto'], data['msg'], data['date_time'], data['link1'], data['link2'], data['textlink1'], data['textlink2'], data['where_post'], data['the_end']))
        base.commit()
