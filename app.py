# Испортируем необходимые библиотеки и переменные
import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter
# Создаем объект бота, с нашим токеном
bot = telebot.TeleBot(TOKEN)

# Приветственный обработчик на команды хелп и старт с инструкцией для начала работы
@bot.message_handler(commands=['start', 'help'])
def send_help(message: telebot.types.Message):
    text = ('Привет! Я бот для конвертации валют.\n'
            'Чтобы узнать цену валюты, отправьте сообщение в формате:\n'
            '<валюта №1> <валюта №2> <количество>\n'
            'Например: евро рубль 100\n\n'
            'Доступные команды:\n'
            '/start, /help - инструкция по использованию\n'
            '/values - список доступных валют')
    bot.reply_to(message, text)

# Обработчик для ввода команды на вывод доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n' + '\n'.join(keys.keys())
    bot.reply_to(message, text)

# Обработчик запроса на конвертацию
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров. Используйте формат: валюта №1 валюта №2 количество')

        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
        # Округлим до 2 знаков для удобства
        text = f'{amount} {base} = {round(total, 2)} {quote}'
        bot.send_message(message.chat.id, text)
    # Отлавливаем ошибки типа APIException, который сами создали
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    # Отлавливаем все остальные ошибки с добавлением текста
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')

# Запускаем бота
bot.polling()