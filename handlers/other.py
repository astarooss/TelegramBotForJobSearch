from aiogram.utils.markdown import hlink
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram import Dispatcher, types
import asyncio
from aiogram.dispatcher import FSMContext
from config import CHANNEL, CHAT
from data_base import ps2_client
from create_bot import dp, bot



VAKANSE = ['Вакансия','вакансия','вакансія','Нова вакансія','БЕСПЛАТНАЯ ВАКАНСИЯ','Работа для мужчин','РАБОТА на','работа на','РАБОТА ДЛЯ МУЖЧИН','предлагаю работу', 'Предлагаю работу']
ISK_SLOVA = ('ELFBAR', 'нужны счета', 'Нужны счета',' Нужны банковские карты','продаю три вида табака','weed','Чёрный список','@BLPraha','兄弟来抖音引流上粉免费合作','VAPES','банковские аккаунты',' cocaine','Alien Kush','Columbian','Fishscale',' нужен счет','залив','SPEED',' KETAMINE','MDMA','COCAINE','THC','sativa',' indica')

async def time_msg_delete(msg, n, state):
    try:
        await asyncio.sleep(n)
    except asyncio.CancelledError:
        raise
    finally:
        try:
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            await state.finish()
        except: 
            pass

async def delete_invite(message: types.Message):
    try:
        await message.delete()
    except:
        pass
    
        

async def check_message(message: types.Message, state: FSMContext):
    print(message)
        
    if message.from_user.username == 'rabota_praha_bot':
        return
    user_status = await bot.get_chat_member(chat_id=-1001509271122, user_id=message.from_user.id)
    if user_status["status"] != 'left':
        print(user_status)
        bot_url = hlink('ботом', 'https://t.me/rabota_praha_bot')
        channel_url = hlink('канале', 'https://t.me/work_in_prague')
        for isk in ISK_SLOVA:
            try:
                if isk.lower() in message.text.lower().replace(' ',''):
                    await message.delete()
                    return
            except:
                pass
        try:
            for vakans in VAKANSE:
                if vakans.lower() in message.text.lower():
                    all_id = await ps2_client.get_all_id()
                    if message.from_user.id in all_id:
                        if await ps2_client.get_table_number(message.from_user.id) == 0:
                                keyboard = InlineKeyboardMarkup()
                                button = InlineKeyboardButton('Перейти в бота', url='https://t.me/rabota_praha_bot')
                                keyboard.add(button)
                                msg = await message.reply(f'Вы так же можете воспользоваться нашим {bot_url} для публикации своих вакансий в {channel_url}, это <b>бесплатно</b>', reply_markup=keyboard, disable_web_page_preview=True, parse_mode='HTML')
                                asyncio.create_task(time_msg_delete(msg, 30, state))
                                return
                    else:
                        keyboard = InlineKeyboardMarkup()
                        button = InlineKeyboardButton('Перейти в бота', url='https://t.me/rabota_praha_bot')
                        keyboard.add(button)
                        msg = await message.reply(f'Вы так же можете воспользоваться нашим {bot_url} для публикации своих вакансий в {channel_url}, это <b>бесплатно</b>', reply_markup=keyboard, disable_web_page_preview=True, parse_mode='HTML')
                        asyncio.create_task(time_msg_delete(msg, 30, state))
                        return

        except Exception as _ex:
            print(_ex)
    else:
        print(user_status, '2')
        try:
            await message.delete()
        except Exception as _ex:
            print(_ex)
        try:
            async with state.proxy() as data:
                msg = data['msg_time']
                await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
                print('aaaaa')
                await state.finish()
        except:
            pass
            
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Пререйти в канал', url='https://t.me/work_in_prague')
        keyboard.add(button)
        msg = await bot.send_message(chat_id=message.chat.id, text=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>, Чтобы писать в чате нужно подписаться на канал', reply_markup=keyboard, parse_mode='HTML')
        asyncio.create_task(time_msg_delete(msg, 180, state))
        async with state.proxy() as data:
            data['msg_time'] = msg
        
        



    

    
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(delete_invite, content_types=['new_chat_members'])
    dp.register_message_handler(check_message, content_types=['text','audio','document','photo','sticker', 'video','video_note','voice'])

    