import telebot
import time
import re
import time
# Количество сообщений за период времени (в секундах)
MAX_MESSAGES = 80
PERIOD_SECONDS = 20

# Максимальное количество нарушений правил чата
MAX_RULE_VIOLATIONS = 8

# Список забаненных пользователей
banned_users = []

# Словарь для хранения информации о пользователях
# ключ - id пользователя
# значение - словарь с информацией о пользователе
user_data = {}

# Список матных слов
MAT_WORDS = ['пицес', 'пиздец', 'трахал', 'ахуеть', 'ахуел', 'ухуел', 'пидорас', 'пидор', 'Лох', 'пидр', 'Лох пидр', 'хуечок', 'я твою мать ебал','блядь', 'хуй', 'пизда', 'ебать', 'ебал', 'ебись', 'нахуй', 'сука', 'уебок', 'уебать', 'ебанутый', 'ебало','скуа', 'блять', 'соси хуй', 'соси член' ,'писюн' ,'сучка', 'ахуеть', 'бл', 'заебись', 'подсосник', 'я трахал твою мать', 'я трахал всех и вашу мамашу', 'я трахал всех и вашу мать']

# Регулярное выражение для поиска матерных слов в сообщениях
MAT_REGEX = re.compile('(?:\s|^)' + '|'.join(MAT_WORDS) + '(?:\s|$)')

# Создание бота
bot = telebot.TeleBot("2043194007:AAFLOo4yPUaRtI6jo8fXzBJckcGpEbOAyC4")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.username == 'Agurchik2014':  # Проверка, что команду выполняет администратор
        if message.reply_to_message:  # Проверка, что есть сообщение ответа
            user_id = message.reply_to_message.from_user.id  # Получение ID пользователя, которого нужно заблокировать
            bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)  # Блокировка пользователя
            bot.send_message(chat_id=message.chat.id, text='Пользователь был заблокирован.')  # Отправка сообщения о блокировке
        else:
            bot.send_message(chat_id=message.chat.id, text='Пожалуйста, ответьте на сообщение пользователя, которого хотите заблокировать.')
    else:
        bot.send_message(chat_id=message.chat.id, text='У вас нет прав на выполнение этой команды.')
@bot.message_handler(commands=['creator'])
def show_creator_info(message):
    bot.send_message(chat_id=message.chat.id, text='Powered HeRuTerm copyright 2023')

@bot.message_handler(func=lambda message: message.text.lower() == 'привет бот модератор')
def reply_to_greeting(message):
    bot.send_message(chat_id=message.chat.id, text=f'Привет! Учасник {message.from_user.first_name} :)')

@bot.message_handler(func=lambda message: message.text.lower() == 'секретное слово')
def reply_to_greeting(message):
    bot.send_message(chat_id=message.chat.id, text=f'меня держит учасник {message.from_user.first_name} в заложниках')
    
@bot.message_handler(func=lambda message: message.text.lower() == 'ГитХаб')
def reply_to_greeting(message):
    bot.send_message(chat_id=message.chat.id, text=f'Искодник: ')
# Основная функция обработки сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global banned_users

    # Получение id пользователя и времени текущего сообщения
    user_id = message.from_user.id
    message_time = time.time()

    # Проверяем, что сообщение было отправлено в группе/канале, а не в 1 на 1 чате
    if message.chat.type == 'private':
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста, добавьте бота в группу или канал.')
        return

    # Проверяем, что у бота есть права администратора в группе/канале
    try:
        chat_member = bot.get_chat_member(chat_id=message.chat.id, user_id=bot.get_me().id)
        if not chat_member.status == 'administrator':
            bot.send_message(chat_id=message.chat.id, text='У бота нет прав администратора в этой группе/канале.')
            return
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=f'У бота нет прав администратора в этой группе/канале Ошибка: {e}.')
        return

    # Если пользователь был заблокирован ранее, то игнорируем его сообщения
    if user_id in banned_users:
        return

    # Если пользователь отправляет сообщение первый раз, то добавляем его в словарь
    if user_id not in user_data:
        user_data[user_id] = {'message_count': 1, 'last_message_time': message_time, 'rule_violations': 0}
    else:
        user_info = user_data[user_id]

        # Если пользователь уже отправлял сообщения, то определяем количество сообщений за период времени
        if message_time - user_info['last_message_time'] > PERIOD_SECONDS:
            user_info['message_count'] = 0
        user_info['message_count'] += 1
        user_info['last_message_time'] = message_time

        # Если количество сообщений превышает допустимое значение, то удаляем сообщение
        if user_data[user_id]['message_count'] > MAX_MESSAGES:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            user_data[user_id]['rule_violations'] += 1

        # Если пользователь нарушает правило более чем указанное количество раз, то баним его
        if user_data[user_id]['rule_violations'] > MAX_RULE_VIOLATIONS:
            bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
            bot.send_message(chat_id=message.chat.id, text=f'Пользователь {message.from_user.first_name} был забанен за частые нарушения правил чата.')
            banned_users.append(user_id)
            del user_data[user_id]
            return

    # Проверяем сообщение на наличие матерных слов
    if MAT_REGEX.search(message.text.lower()):
        # Удаляем сообщение с матерным словом
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        # Отправляем пользователю предупреждение о запрете использования матерных слов
        bot.send_message(chat_id=message.chat.id, text=f'Использование матерных слов запрещено. Пожалуйста, проявите уважение к другим участникам чата, пользователь {message.from_user.first_name}.')
        user_data[user_id]['rule_violations'] += 1
        bot.send_message(chat_id=message.chat.id, text=f'У вас уже {user_data[user_id]["rule_violations"]} предупреждений, отправлено для {message.from_user.first_name}. Максимальное предуприждений: 8')

        # Если пользователь нарушает правило более чем указанное количество раз, то баним его
        if user_data[user_id]['rule_violations'] > MAX_RULE_VIOLATIONS:
            bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
            bot.send_message(chat_id=message.chat.id, text=f'Пользователь {message.from_user.first_name} был забанен за частые нарушения правил чата.')


            banned_users.append(user_id)
            del user_data[user_id]
            return


# Запуск бота
bot.polling(none_stop=True)
