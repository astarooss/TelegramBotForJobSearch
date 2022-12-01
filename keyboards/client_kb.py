from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Меню вакансий')
b2 = KeyboardButton('Для работодателей')
b3 = KeyboardButton('Помощь в поиске работы')


kb_client_menu = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client_menu.add(b1).insert(b2).add(b3)# add добавление кнопок сверху вниз, insert кнопка сбоку, 

ba1 = KeyboardButton('Выбрать тип работы')
ba2 = KeyboardButton('Показать новые')
ba3 = KeyboardButton('Меню')


kb_client_menu_hesteg = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client_menu_hesteg.add(ba1).add(ba2).add(ba3)# add добавление кнопок сверху вниз, insert кнопка сбоку, 

b4 = KeyboardButton('Изменить анкету')
b5 = KeyboardButton('Наши контакты')
b6 = KeyboardButton('Меню')

kb_client_menu_anketa = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client_menu_anketa.add(b4).add(b5).insert(b6)# add добавление кнопок сверху вниз, insert кнопка сбоку, 


bc3 = KeyboardButton('Мои вакансии')
bс2 = KeyboardButton('Добавить вакансию')
bc1 = KeyboardButton('Меню')



kb_client_menu_с = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_menu_с.add(bс2).add(bc3).add(bc1)


a1 = KeyboardButton('Заполнить анкету')
a2 = KeyboardButton('Связатся с нами')
a3 = KeyboardButton('Пропустить')

kb_client_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_start.add(a1).add(a2).insert(a3)




a1 = KeyboardButton('Я работодатель')
a2 = KeyboardButton('Я ищу работу')


kb_client_start_2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_start_2.add(a1).add(a2)


a4 = KeyboardButton('Прoпустить') #Fake FSM
a44 = KeyboardButton('Отмена') #Fake FSM

kb_client_pass = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_pass.add(a4).add(a44)


a5 = KeyboardButton('Продолжить')

kb_client_continue = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_continue.add(a5)


c1 = KeyboardButton('Мужской')
c2 = KeyboardButton('Женский')


kb_gender = ReplyKeyboardMarkup(resize_keyboard=True)
kb_gender.add(c1).insert(c2).add(a4)


e1 = KeyboardButton('Да')
e2 = KeyboardButton('Нет')
e3 = KeyboardButton('Отмена')

kb_yes_no = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yes_no.add(e1).insert(e2).add(a4).add(e3)


f1 = KeyboardButton('Дальше')
f2 = KeyboardButton('Меню')

kb_fuski_yes = ReplyKeyboardMarkup(resize_keyboard=True)
kb_fuski_yes.add(f1).add(f2)



