from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Отмена')
b2 = KeyboardButton('Не добавлять фото')


kb_work = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_work.add(b1)# add добавление кнопок сверху вниз, insert кнопка сбоку,

kb_work_foto = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_work_foto.add(b2).add(b1)# add добавление кнопок сверху вниз, insert кнопка сбоку,