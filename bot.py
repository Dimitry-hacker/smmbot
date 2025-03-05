import telebot
from telebot import types

# Укажите токен вашего Telegram-бота
TOKEN = '7869394460:AAESHFkHVeuVQQqaJVTReJqB8FTgMxcf1c0'
ADMIN_CHAT_ID = '6309643502'  # Ваш ID для получения уведомлений в личку
bot = telebot.TeleBot(TOKEN)

# Начальные значения
user_data = {}

# Цены
PRICES = {
    'stories': 50000,
    'reels': 150000,
    'targeting': 250000,
    'uni_100': 1000000,
    'uni_150': 1500000,
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'stories': 0, 'reels': 0, 'targeting': 0}
    markup = main_menu()
    bot.send_message(chat_id, '📸 Мобилография тарифлари', reply_markup=markup)

# Функция для главного меню
def main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🛠 Конструктор', callback_data='constructor'))
    markup.add(types.InlineKeyboardButton('📦 Uni 100', callback_data='uni_100_info'))
    markup.add(types.InlineKeyboardButton('📦 Uni 150', callback_data='uni_150_info'))
    return markup

# Функция для генерации клавиатуры конструктора
def get_constructor_markup(data):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(f'📝 Stories: {data["stories"]} (50,000 сум/мес)', callback_data='none'),
        types.InlineKeyboardButton('+1', callback_data='stories+'),
        types.InlineKeyboardButton('-1', callback_data='stories-')
    )
    markup.add(
        types.InlineKeyboardButton(f'🎬 Reels: {data["reels"]} (150,000 сум/мес)', callback_data='none'),
        types.InlineKeyboardButton('+1', callback_data='reels+'),
        types.InlineKeyboardButton('-1', callback_data='reels-')
    )
    markup.add(
        types.InlineKeyboardButton(f'🎯 Targeting: {"250,000 сум" if data["targeting"] else "Yo'q"}', callback_data='targeting')
    )
    markup.add(types.InlineKeyboardButton('🛒 Buyurtma berish', callback_data='order_constructor'))
    markup.add(types.InlineKeyboardButton('⬅️ Orqaga', callback_data='main_menu'))
    return markup

# Функция для меню тарифов Uni
def get_uni_markup(tarif):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🛒 Buyurtma berish', callback_data=f'order_{tarif}'))
    markup.add(types.InlineKeyboardButton('⬅️ Orqaga', callback_data='main_menu'))
    return markup

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    username = call.message.chat.username or 'Неизвестный пользователь'
    data = user_data.get(chat_id, {'stories': 0, 'reels': 0, 'targeting': 0})
    updated = False

    if call.data == 'constructor':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='🛠 Конструктор тарифлари',
            reply_markup=get_constructor_markup(data)
        )

    elif call.data == 'main_menu':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='📸 Мобилография тарифлари',
            reply_markup=main_menu()
        )

    elif call.data == 'uni_100_info':
        info = (
            '📦 Uni 100 Tarifi\n'
            '💰 Narxi: 1.000.000 Sum/oy\n'
            '🎬 8 Reels\n'
            '📝 3 Stories\n'
            '🎥 Videoga olish ichida!'
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=info, reply_markup=get_uni_markup('uni_100'))

    elif call.data == 'uni_150_info':
        info = (
            '📦 Uni 150 Tarifi\n'
            '💰 Narxi: 1.500.000 Sum/oy\n'
            '🎬 10 Reels\n'
            '📝 5 Stories\n'
            '🎥 Videoga olish ichida!\n'
            '🎨 1 ta logotip (Aksiya boyicha!)'
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=info, reply_markup=get_uni_markup('uni_150'))

    elif call.data in ['stories+', 'stories-']:
        change = 1 if '+' in call.data else -1
        if 0 <= data['stories'] + change <= 10:
            data['stories'] += change
            updated = True

    elif call.data in ['reels+', 'reels-']:
        change = 1 if '+' in call.data else -1
        if 0 <= data['reels'] + change <= 10:
            data['reels'] += change
            updated = True

    elif call.data == 'targeting':
        data['targeting'] = not data['targeting']
        updated = True

    elif call.data == 'order_constructor':
        total = data['stories'] * PRICES['stories'] + data['reels'] * PRICES['reels']
        if data['targeting']:
            total += PRICES['targeting']
        order_text = (
            f'📥 Новый заказ от @{username}!'
            f'📦 Тариф: Конструктор'
            f'📝 Stories: {data["stories"]}'
            f'🎬 Reels: {data["reels"]}'
            f'🎯 Targeting: {"Да" if data["targeting"] else "Нет"}'
            f'💰 Итоговая сумма: {total} сум'
        )
        bot.send_message(ADMIN_CHAT_ID, order_text)
        bot.send_message(chat_id, "✅ Buyurtmangiz Qabul qilindi! tez orada siz bilan bog'lanamiz")

    if updated:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='🛠 Конструктор тарифлари',
            reply_markup=get_constructor_markup(data)
        )

# Запуск бота
bot.polling(none_stop=True)

