import telebot, configparser
from telebot  import types, apihelper
from googletrans import Translator

config = configparser.ConfigParser()
config.read("settings.ini")
token    = config["tgbot"]["token"]

bot = telebot.TeleBot(token)

translator = Translator()

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Перевести!',callback_data=3))
    bot.send_message(message.chat.id, "Добро пожаловать!\nЯ переводчик и готов перевести слова или придложения \nК примеру :Hello-Привет, Привет-Hello. Нажми на перевести!\n Техподержка: /id", reply_markup = markup)

keyboardcode = types.InlineKeyboardMarkup()
url_button = types.InlineKeyboardButton(text="Получить код!", url="https://github.com/wefeinew/codebot/tree/main")
keyboardcode.add(url_button)

@bot.message_handler(commands=["code"])
def cmd_code(message):
    bot.send_message(message.chat.id, "Для получение исходоного кода нажмите на кнопку ниже.", reply_markup=keyboardcode)

keyboard_id = types.InlineKeyboardMarkup()
url_button = types.InlineKeyboardButton(text="Поддержка", url="https://t.me/theworldsfox")
keyboard_id.add(url_button)

@bot.message_handler(commands=["id"])
def foo(message):
    bot.send_message(message.chat.id, "Поддержка ниже.", reply_markup=keyboard)

@bot.message_handler()
def info(message: types.Message):
    bot.send_message(message.chat.id, 'Неизвестная команда⚠️\nСписок команд вы можете посмотреть в меню')

@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == "Перевести":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Русский ',callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='Англиский ', callback_data=2))

        bot.send_message(message.chat.id, "Выбери язык на который хочешь перевести текст.", reply_markup = markup)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Русский',callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='Англиский ', callback_data=2))
        bot.send_message(message.chat.id, "Выбери язык на который хочешь перевести текст.", reply_markup = markup)

def next_trans2(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'ru'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

def next_trans3(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text =  message.text
        lang = 'en'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == '1':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=4))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введи текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans2)
    elif call.data == '2':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=4))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введи текст для перевода", reply_markup = markup)
        bot.register_next_step_handler(msg, next_trans3)
    elif call.data == '3':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Русский',callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='Англиский ', callback_data=2))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Выбери язык на который хочеш перевести текст.", reply_markup = markup)
    elif call.data == '4':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Перевести', callback_data=3))
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Вы вернулись в главное меню!", reply_markup = markup)


bot.polling(none_stop=True, interval=0)
