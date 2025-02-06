import requests
from bs4 import BeautifulSoup
import telebot


bot = telebot.TeleBot(token='')


try:
    res = requests.get('https://tengrinews.kz/weather/semey/day/')
    soup = BeautifulSoup(res.content, 'html.parser')

    temp = soup.find(class_='weather-city-all-temp-value')
    temp = temp.text.replace('\n', '').replace('  ', '') if temp else "Температура неизвестна."

    dop = soup.find(class_='weather-city-other')
    dop = dop.text.replace('\n', '').replace('  ', '') if dop else "Дополнительные данные недоступны."

    dop_parts = dop.split()
    if len(dop_parts) >= 5:
        wind = "Ветер: " + dop_parts[0] + " " + dop_parts[1]
        humidity = "Влажность: " + dop_parts[2]
        pressure = "Давление: " + dop_parts[3] + " " + dop_parts[4]
    else:
        wind = "Данные о ветре отсутствуют."
        humidity = "Данные о влажности отсутствуют."
        pressure = "Данные о давлении отсутствуют."
except Exception as e:
    temp = "Не удалось получить данные о погоде."
    wind = "Ошибка получения данных о ветре."
    humidity = "Ошибка получения данных о влажности."
    pressure = "Ошибка получения данных о давлении."


def ntext(text):
    """Возвращает длину текста"""
    return len(text)

def wordA(text):

    count_a = text.lower().count('а')
    return count_a

def glasn(text):

    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

def probel(text):

    return text.count(' ')


user_texts = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(
        user_id,
        'Саламалейкуум! Вот что я могу:\n'
        '- Рассказать о погоде (напишите "погода")\n'
        '- Вывести полезные ссылки (напишите "морген", "шекспир" или "асмр")\n'
        '- Чтобы работать с текстом, напишите "текст"\n'
    )


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    text = message.text.strip().lower()


    if text == 'привет':
        bot.send_message(user_id, 'Саламалейкуум!')
    elif text == 'погода':
        weather_info = f"Температура: {temp}\n{wind}\n{humidity}\n{pressure}"
        bot.send_message(user_id, weather_info)
    elif text == 'морген':
        bot.send_message(user_id, 'https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D1%80%D0%B3%D0%B5%D0%BD%D1%88%D1%82%D0%B5%D1%80%D0%BD')
    elif text == 'шекспир':
        bot.send_message(user_id, 'https://www.stihi-rus.ru/World/Shekspir/90.htm')
    elif text == 'асмр':
        bot.send_message(user_id, 'https://youtu.be/-SYwOAe6V_4?si=vfoZaeUGWmAXUSyQ')
    elif text == 'текст':

        bot.send_message(user_id, 'Введите текст, с которым хотите работать.')
        user_texts[user_id] = None  # Очищаем предыдущий текст, если он был
    elif user_id in user_texts and user_texts[user_id] is None:

        user_texts[user_id] = message.text
        bot.send_message(
            user_id,
            'Выберите действие с текстом:\n'
            '1 - длина текста\n'
            '2 - количество букв "а"\n'
            '3 - количество гласных\n'
            '4 - количество пробелов\n'
        )
    elif text in ['1', '2', '3', '4'] and user_id in user_texts and user_texts[user_id] is not None:

        action = text
        user_text = user_texts[user_id]

        if action == '1':
            bot.send_message(user_id, f"Длина текста: {ntext(user_text)}")
        elif action == '2':
            bot.send_message(user_id, f"Количество букв 'а': {wordA(user_text)}")
        elif action == '3':
            bot.send_message(user_id, f"Количество гласных: {glasn(user_text)}")
        elif action == '4':
            bot.send_message(user_id, f"Количество пробелов: {probel(user_text)}")
        else:
            bot.send_message(user_id, "Некорректное действие. Выберите от 1 до 4.")
    else:

        bot.send_message(
            user_id,
            "Я не понял. Если нужна работа с текстом, напишите 'текст'."
        )


bot.polling(none_stop=True)

