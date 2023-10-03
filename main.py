import telebot
token = input()
# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я простой бот.')

# Обработчик приветствия
@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, 'Привет!')
    elif message.text.lower() == 'как дела?':
        bot.reply_to(message, 'Хорошо, спасибо!')
    else:
        bot.reply_to(message, 'Я не понимаю, что ты говоришь.')

# Запускаем бота
bot.polling()
