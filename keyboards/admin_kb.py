from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Предложка')
b2 = KeyboardButton('Активные вакансии')
b3 = KeyboardButton('Статистика')
b4 = KeyboardButton('Рассылки')
b5 = KeyboardButton('Меню')



kb_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_menu.add(b1).add(b2).add(b3).add(b4).add(b5)

b1 = KeyboardButton('Добавить новую рассылку')
b2 = KeyboardButton('Активные рассылки')
b3 = KeyboardButton('Меню')

kb_admin_rs = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_rs.add(b1).add(b2).add(b3)


c1 = KeyboardButton('Меню вакансий')
c2 = KeyboardButton('Для работодателей')
c3 = KeyboardButton('Помощь в поиске работы')
c4 = KeyboardButton('Админ меню')


kb_admin_menu_2 = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_admin_menu_2.add(c1).insert(c2).insert(c3).add(c4)# add добавление кнопок сверху вниз, insert кнопка сбоку, 

c1 = KeyboardButton('В канал')
c2 = KeyboardButton('В канал с репостом в чат')
c3 = KeyboardButton('в чат')
c4 = KeyboardButton('Отменить')



kb_admin_where_post = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_admin_where_post.add(c1).insert(c2).insert(c3).add(c4)# add добавление кнопок сверху вниз, insert кнопка сбоку, 

c1 = KeyboardButton('Подтвердить')
c2 = KeyboardButton('Отменить')
с3 = KeyboardButton('Сохранить как черновик')
с4 = KeyboardButton('Редактировать текст')

kb_admin_check = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_admin_check.add(c1).insert(c2).insert(c3)# add добавление кнопок сверху вниз, insert кнопка сбоку, 


cc1 = KeyboardButton('Пропустить')
cc2 = KeyboardButton('Отменить')

kb_admin_pass = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_admin_pass.add(cc1).add(cc2)# add добавление кнопок сверху вниз, insert кнопка сбоку,

kb_admin_cal = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_admin_cal.add(c2)# add добавление кнопок сверху вниз, insert кнопка сбоку,


