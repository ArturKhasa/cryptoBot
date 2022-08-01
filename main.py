import telebot
from pycoingecko import CoinGeckoAPI

# записываем токен
bot = telebot.TeleBot('5399066371:AAETXZA9KHxe0aloeaJTle7DoLcaJVSkCx0')
# инициализируем кнопка для ручного выбора
keys = telebot.types.ReplyKeyboardMarkup(True, True)

# подключаем апи
cg = CoinGeckoAPI()

# назначаем поля
keys.row('bitcoin', 'ethereum', 'litecoin')
keys.row('tether', 'binancecoin', 'solana')
keys.row('polkadot', 'dogecoin', 'matic-network')
keys.row('tron', 'chainlink', 'shiba-inu')

# метод получает на вход строку пользователя, и выдает текущий курс
def get_cyrrent_price(message):
    try:
        # в качетсве параметра отдаем строку и курс в долларах и рублях
        result1 = cg.get_price(ids=message, vs_currencies='usd')
        result2 = cg.get_price(ids=message, vs_currencies='rub')
        # result1 и result2 возвращают словари, поэтому будем обращаться по ключам
        result1 = result1[message]['usd']
        result2 = result2[message]['rub']
        # связываем результат
        result_str = message.upper() + '\n' + str(result1) + ' $\n' + str(result2) + ' ₽'
        return result_str
    except Exception as e:
        return 'Данной криптовалюты не найдено.\nПопробуйте выбрать вариант из списка.'


def get_image(id):
    try:
        flag = True
        # пробегаемся по массиву всех криптовалют и получаем у них изображение по соответствию id
        for coin in cg.get_coins_markets(vs_currency='usd'):
            if coin['id'] == id:
                flag = False
                return coin['image']
        # если изображение не найдено, веренем картинку с "изображение не найдено"
        if flag:
            return 'https://pchelp24.com/wp-content/uploads/images/05(1).png'
    except Exception as e:
        return 'https://pchelp24.com/wp-content/uploads/images/05(1).png'


def get_all_current_price():
    try:
        #получаем массив результатов
        result = cg.get_coins_markets(vs_currency='usd')
        result_str = ''
        #связываем все по имени, id и цене
        for i in result:
            coin = i['name'] + '(' + i['id'] + ')' + ' - ' + str(i['current_price']) + ' $\n'
            result_str = result_str + coin
        return result_str
    except Exception as e:
        return 'Сервер не отвечает'


@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Привет, я бот, который поможет узнать тебе текущий курс криптовалюты.'
                                      '\nТы можешь выбрать вариант из списка или ввести необходимую тебе криптовалюту в ручную.'
                                      '\nС помощью команды /allprices ты можешь вывести курс в USD для всех криптовалют', reply_markup=keys)


@bot.message_handler(commands=["allprices"])
def start(message, res=False):
    bot.send_message(message.chat.id, get_all_current_price())


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, str(get_cyrrent_price(message.text)))
    bot.send_photo(message.chat.id, get_image(message.text))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
