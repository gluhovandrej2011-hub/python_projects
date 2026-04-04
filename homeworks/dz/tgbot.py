import telebot
import telebot.types

bot = telebot.TeleBot("8659572926:AAE0B3nl_LS1mmabUIC-8zg_BOgBxtH8Apw")


@bot.message_handler(commands=["start"])
def command_start_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, "добрый день! это бот для поддержки хорошего настроения")


@bot.message_handler(commands=["mood"])
def command_start_handler(message: telebot.types.Message):
    reply_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_add_funny = telebot.types.KeyboardButton("веселое")
    button_add_normal = telebot.types.KeyboardButton("нормальное")
    button_add_sad = telebot.types.KeyboardButton("грустное")

    reply_keyboard.add(button_add_funny)
    reply_keyboard.add(button_add_normal)
    reply_keyboard.add(button_add_sad)

    bot.send_message(message.chat.id, "выбери настроение:", reply_markup=reply_keyboard)


@bot.message_handler(func=lambda message: message.text == "веселое")
def message_text_poka_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Отлично! Тогда сегодня будет хороший день!")


@bot.message_handler(func=lambda message: message.text == "нормальное")
def message_text_poka_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Каждый момент в жизни уникален и ценен")

@bot.message_handler(func=lambda message: message.text == "грустное")
def message_text_poka_handler(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Неудачи — это опыт, который приближает тебя к цели.")

bot.infinity_polling()