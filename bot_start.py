from aiogram.utils import executor  
from create_bot import dp, bot
from data_base import ps2_client, ps2_msg, ps2_rabota
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import hashlib, os
import config
import psycopg2 as ps
import asyncio
import aioschedule
import datetime
import requests
from bs4 import BeautifulSoup as bs
from aiogram.utils.markdown import hlink
from telegraph import Telegraph

WORK_LIST_REPLACE = [('Разнорабочие','Разноробочий'), ('Строительство','Стройка'),('Заводы','Завод'),('Водители','Водитель'),('Рестораны','Ресторан'),('Удаленная работа','Удаленная-работа'),('Менеджеры','Менеджер'),('Домашний персонал','Домашний-персонал'),('Без опыта','Без-опыта'),('Магазин','Магазин'),('Сфера услуг','Сфера-услуг'),('Учителя','Учитель'),('Сельское хозяйство','Сельское-хозяйство')]

base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
cur = base.cursor()

async def on_startup(dp):
    ps2_client.sql_start() #подключение к базе данных
    ps2_rabota.sql_start_work()
    ps2_msg.sql_start_msg()
    asyncio.create_task(scheduler_chat())
    await bot.set_webhook(config.URL_APP)



async def auto_rabota():
    URL_TEMPLATE = 'https://layboard.com/vakansii/chehiya/rabota-v-prage'

    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    urll = soup.find('div', class_='job-filters__item jfilter-item js-filter-by-date').find('input', class_='jfilter-item__check-item-input')
    print(urll['value'])



    r = requests.get('https://layboard.com/vakansii/chehiya/rabota-v-prage?date=' + urll['value'])
    soup = bs(r.text, "html.parser")
    vacancies_names = soup.find_all('div', class_='vacancy-card')
    res_list = []
    n = 0
    bre = True
    while bre:
        res = vacancies_names[n].find('p', class_='vacancy-date')
        
        if res.text.find('минут') != -1 or res.text.find('секунд') != -1:
            res_list.append(vacancies_names[n])
            break
        n += 1
        if n == len(vacancies_names):
            break
    print(len(res_list))


    for name in res_list:
        url = name.a['href']
        r = requests.get('https://layboard.com' + url)
        soup = bs(r.text, "html.parser")
        name = soup.find('span', class_='jarticle__categories-item')
        price = soup.find('div', class_='jarticle__stat-value')
        number = soup.find('div', class_='jarticle__company-info-row')
        describe = soup.find('div', class_='jarticle__descrip')
        number = number.a['data-phone']
        name = name.text

        describe = describe.text[:describe.text.find('Связаться с работодателем')]
        while True:
            if describe[-1] == '\n':
                describe = describe[:-1]
            else:
                break

        while True:
            if describe[0] == ' ':
                describe = describe[1:]
            else:
                break

        if describe[0:11] == 'Требования:':
            describe = describe[11:]

        while True:
            if describe[0] == '\n':
                describe = describe[1:]
            else:
                break
        
        
        describe =  describe.replace('\n\n\n\n\n', '\n\n')
        describe =  describe.replace('\n\n\n\n', '\n\n')
        describe =  describe.replace('\n\n\n', '\n\n')

        for work_nam in WORK_LIST_REPLACE:
            name = name.replace(work_nam[0], work_nam[1])
        name = name.replace('\n','')

        if len(describe) > 750:
            deskr = f'💵Цена: {price.text}\n\n📋Описание: {describe}\n\n 📩Контакты: {number}'
            deskr = deskr.replace('\n','<br>')

            

            conf = {'short_name': 'altruist',
                    'author_name': 'Работа в Праге, Чехии',
                    'author_url': 'https://t.me/work_in_prague',
                    'access_token': 'e27cca42f77f9745940df9f3cda5e61e499472387b6098ac433cf96e770b',
                    'auth_url': 'https://edit.telegra.ph/auth/VeQL6ZlrfaDqJTASRgWMNCkK31RvPtnIHctLbMaqUO'}

            telegraph = Telegraph(conf["access_token"]) 
            response = telegraph.create_page(
                name, 
                html_content=deskr,
                author_name=conf['author_name'], 
                author_url=conf['author_url']
            )
            url_page = 'https://telegra.ph/{}'.format(response['path'])

            link_page = hlink('...читать дальше', url_page)

            
            describe = describe[:500] + link_page
        
        link = hlink('Работа в Праге, Чехии', 'https://t.me/work_in_prague')
        msg = await bot.send_message(chat_id=-1001509271122, text= f'💼 #{name}\n\n💵Зарплата: {price.text}\n\n📋Описание: {describe}\n\n📩Контакты: {number}\n\n{link}', parse_mode='HTML', disable_web_page_preview=True)
        await bot.forward_message(from_chat_id=-1001509271122, chat_id=-1001869904593, message_id=msg.message_id)

async def auto_chat():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Перейти в бота', url='https://t.me/rabota_praha_bot')
    button2 = InlineKeyboardButton('Перейти в канал', url='https://t.me/work_in_prague')
    keyboard.add(button).add(button2)
    await bot.send_message(chat_id=-1001869904593, text= f'Ищете работу или предлагаете вакансии?\n\nВоспользуйтесь нашим беспалатным ботом в котором можно публиковать свои вакансии\n\nТак же все вакансии автоматически публикуются в наш канал', reply_markup=keyboard)

async def auto_channel():
    keyboard = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton('Написать', url='https://t.me/alltruiist')
    keyboard.add(button2)
    await bot.send_message(chat_id=-1001509271122, text= f'Развиваете свой бизнес?. Нужны заказы?\n\nНапишите нам, за 500 крон мы выложим вашу рекламу 90 раз в чате и 15 раз в канале, места ограничены', reply_markup=keyboard)

async def auto_chat_cz():
    try:
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Инстаграм', url='https://instagram.com/icepeak.cz?igshid=YmMyMTA2M2Y=')
        button2 = InlineKeyboardButton('ТикТок', url='https://www.tiktok.com/@icepeak.czech?_t=8WYtkzFrNfJ&_r=1')
        keyboard.add(button).add(button2)
        await bot.send_photo(chat_id=-1001869904593, photo='AgACAgQAAxkBAAIBGGNbw9YCAzlzYeYUY2qQCJdfyRdRAAKOvDEb7GrgUtCrBXavMlHZAQADAgADcwADKgQ', caption = f'ICEPEAK - курсы ЖИВОГО чешского\n\nЗаговори уже на первом уроке!\n\n❗️идёт набор в группы А1, А2 и на индивидуальные занятия❗️\n\nОФФЛАЙН  и  ОНЛАЙН группы\n- А1, А2, B1 - 2800 kč/мес (8 занятий/полтора часа)\n\nИНДИВИДУАЛЬНЫЕ ЗАНЯТИЯ:\n- онлайн\n- график гибкий, расписание подстраивается под Вас\n----------------------------------------\n- Вас ждут эффективные занятия по авторской программе. Мы научим Вас ЖИВОМУ чешскому, научим ГОВОРИТЬ.\n\n- Записаться и узнать подробности можно в личных сообщениях: @icepeakcz или по номеру\n+420774091027', reply_markup=keyboard)
    except Exception as _ex:
        await bot.send_message(632567149, str(_ex), 'auto_cahat_cz')

async def auto_reclama():
    try:
        keyboard = InlineKeyboardMarkup()
        button2 = InlineKeyboardButton('Написать', url='https://t.me/alltruiist')
        keyboard.add(button2)
        await bot.send_message(chat_id=-1001869904593, text= f'Развиваете свой бизнес?. Нужны заказы?\n\nНапишите нам, за 500 крон мы выложим вашу рекламу 90 раз в чате и 30 раз в канале, места ограничены', reply_markup=keyboard)

    except Exception as _ex:
        await bot.send_message(632567149, str(_ex), 'auto_cahat_cz')

async def adss():
    try:
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton('Узнать подробнее', url='https://telegra.ph/Uroki-po-Python-10-25')
        button2 = InlineKeyboardButton('Написать в лс', url='https://t.me/alltruiist')
        keyboard.add(button).add(button2)
        await bot.send_photo(chat_id=-1001869904593, photo='AgACAgQAAxkBAAI5DmNZElAqd5qFvJSVb6xQxRozAb1hAAJctzEbkZPBUscvVFC3D-LIAQADAgADcwADKgQ', caption = f'<b>Интересует программирование но не знаешь с чего начать? </b> <tg-spoiler> <i> \n\nЯ создатель этого чата и бота от имени которого отправляется сообщение, помогаю новичкам освоится в сфере IT с нуля. </i> </tg-spoiler> \n\nПроведу от стадии "Хочу войти в IT но у меня лапки", до первых кейсов.\n\nОбучаю написанию всевозможных парсеров, Телеграм ботов, сайтов на Django,\n\nтак же бонусом SQL, HTML. CSS.',parse_mode='HTML', reply_markup=keyboard)
    except Exception as _ex:
        await bot.send_message(632567149, str(_ex),' adss')

async def scheduler_chat():
    time_chat = ['8:00','10:00','14:00','16:00','18:00']
    for time in time_chat:
        aioschedule.every().day.at(time).do(auto_chat)
    
    time_chat_cz = ['8:30','10:30','14:30','16:30','18:30']
    for time in time_chat_cz:
        aioschedule.every().day.at(time).do(auto_chat_cz)
    
    time_adss = ['7:20','8:20','9:20','10:20','11:20','12:20','13:20','14:20','15:20','16:20','17:20','18:20','19:20','20:20']
    for time in time_chat_cz:
        aioschedule.every().day.at(time).do(auto_reclama)
    
    time_adss = ['9:00','11:00','15:00','17:00','19:00']
    for time in time_adss:
        aioschedule.every().day.at(time).do(adss)

    time_adss = ['7:10','8:10','9:10','10:10','11:10','12:10','13:10','14:10','15:10','16:10','17:10','18:10','19:10','20:10']
    for time in time_adss:
        aioschedule.every().day.at(time).do(auto_rabota)


    aioschedule.every().day.at('18:20').do(auto_channel)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
    
    
async def on_shutdown(dp): 
    await bot.delete_webhook()
    cur.close()
    base.close()


from handlers import admin, client, other, work

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
work.register_handlers_work(dp)
other.register_handlers_other(dp)

executor.start_webhook(
    dispatcher = dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)))