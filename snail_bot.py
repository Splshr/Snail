import telebot
import datetime
import json
from telebot import types


bot = telebot.TeleBot(' ')

admin_chat_id = '305434350'

order_text = ""  # Глобальная переменная для хранения текста заказа

#Обработка того, что пользователь отправляет рандомный стикер в чат.
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    # Обработка стикера
    bot.send_sticker(message.chat.id, message.sticker.file_id)

#Обработка старта бота
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    update_user_stats(user_id)

    # Отправляем приветственное сообщение и главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Наша місія ✉️")
    item2 = types.KeyboardButton("Замовлення 🌮")
    item3 = types.KeyboardButton("Зв'язатись з нами ☎️")
    item4 = types.KeyboardButton("Равлик Кешбек 💸")
    item5 = types.KeyboardButton("Відгуки та пропозиції 👀")
#    item6 = types.KeyboardButton("Залишити оцінку")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Вітаємо у Головному меню бота Равлик! Поки працюємо у тестовому режимі 🇺🇦", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text not in ["Наша місія ✉️", "Замовлення 🌮", "Зв'язатись з нами ☎️", "Равлик Кешбек 💸", "Відгуки та пропозиції 👀", "Доставка", "Самовивіз", "Поділитись геопозицією", "Ввести адресу вручну"])
def handle_unrecognized_commands(message):
    # Обработка незнакомых команд
    bot.send_message(message.chat.id, "Незнайома команда. Виберіть команду з Головного меню.")
    send_welcome(message)

# Обработчики для разделов меню
@bot.message_handler(func=lambda message: message.text == "Наша місія ✉️")
def mission(message):
    bot.send_message(message.chat.id, "Зараз уся команда активно працює над нашою місією, і ми обов'язково повідомимо Вам про неї незабаром. 😌")

@bot.message_handler(func=lambda message: message.text == "Зв'язатись з нами ☎️")
def contact_us(message):
    bot.send_message(message.chat.id, "Для зв'язку з нами, будь ласка, наберіть 0979360140")

@bot.message_handler(func=lambda message: message.text == "Замовлення 🌮")
# def online_order(message):
#     bot.send_message(message.chat.id, "Ми активно працюємо над введенням доставки, і дуже скоро проінформуємо Вас 😜. Поки Ви можете набрати нас за номером 0979360140 і замовити наші перекуси на бажаний Вами час  😋")
def online_order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Доставка")
    item2 = types.KeyboardButton("Самовивіз")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Оберіть тип замовлення:", reply_markup=markup)

# Обработчик выбора "Доставка"
@bot.message_handler(func=lambda message: message.text == "Доставка")
def request_order(message):
    bot.send_message(message.chat.id, "Напишіть, що ви бажаєте замовити. Зауважте, що замовлення не можна буде редагувати.")
    # Добавляем обработчик для следующего сообщения
    bot.register_next_step_handler(message, process_order)

@bot.message_handler(func=lambda message: message.text == "Самовивіз")
def request_order(message):
    bot.send_message(message.chat.id, "Напишіть, що ви бажаєте замовити. Зауважте, що замовлення не можна буде редагувати.")
    # Добавляем обработчик для следующего сообщения
    bot.register_next_step_handler(message, process_order)

# Обработчик для получения заказа
def process_order(message):
    global order_text
    order_text = message.text
    bot.send_message(message.chat.id, f"Дякуємо. Ви замовили: {order_text}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Поділитись геопозицією")
    item2 = types.KeyboardButton("Ввести адресу вручну")
    markup.add(item1, item2)

    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Оберіть спосіб доставки:", reply_markup=markup)
    # Здесь можно добавить логику для отправки заказа клиенту или обработку заказа

@bot.message_handler(func=lambda message: message.text == "Поділитись геопозицією")
def share_location(message):
    # Запрашиваем у пользователя его геопозицию с помощью клавиатуры
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item = types.KeyboardButton("Відправити геопозицію", request_location=True)
    markup.add(item)

    bot.send_message(message.chat.id, "Будь ласка, поділіться своєю геопозицією.", reply_markup=markup)

# Добавьте обработчик для получения геопозиции
@bot.message_handler(content_types=["location"])
def receive_location(message):
    global order_text
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        bot.send_message(message.chat.id, f"Ви поділилися геопозицією з координатами:\nШирота: {latitude}\nДовгота: {longitude}\n {order_text}")
        bot.send_message(admin_chat_id, f"{latitude}, {longitude}, {order_text}")
        order_text = ""
    else:
        bot.send_message(message.chat.id, "Ви не поділилися геопозицією. Будь ласка, натисніть на кнопку 'Поділитись геопозицією' та надайте доступ до своєї геопозиції. Ідіть на хуй.")

@bot.message_handler(func=lambda message: message.text == "Равлик Кешбек 💸")
def cashback(message):
    bot.send_message(message.chat.id, "Кешбек незабаром!")

@bot.message_handler(func=lambda message: message.text == "Відгуки та пропозиції 👀")
def review(message):
    bot.send_message(message.chat.id, "Тут ви можете лишити відгук та ваші пропозиції. Зауважте, що Ваш відгук абсолютно анонімний, дякуємо. 🤝")
    bot.register_next_step_handler(message, process_review)


#Обработка того, что пользователь при нажатии на кнопку отзыва, мог нажимать на другие кнопки и сразу выполнялись другие команды
def process_review(message):
    if message.text == "Наша місія ✉️":
        mission(message)
    elif message.text == "Замовлення 🌮":
        online_order(message)
    elif message.text == "Зв'язатись з нами ☎️":
        contact_us(message)
    elif message.text == "Равлик Кешбек 💸":
        cashback(message)
    elif message.text == "Відгуки та пропозиції 👀":
        review(message)
    else:
        save_review(message)

def save_review(message):
    review_text = message.text
    now = datetime.datetime.now()
    review_data = f"{now.date()} // {now.time()} // {review_text}\n"
    bot.send_message(admin_chat_id, review_data)
    # Сохраняем отзыв в файл
    with open("reviews.txt", "a") as f:
        f.write(review_data)

    bot.send_message(message.chat.id, "Ваш відгук було збережено. Дякуємо!")


#Сохранение юзерайдишек в джейсон файл
def update_user_stats(user_id):
    today = datetime.date.today().isoformat()  # Получаем текущую дату в формате ГГГГ-ММ-ДД
    user_stats = {}  # Словарь для хранения статистики пользователей

    # Попытка загрузить статистику из файла
    try:
        with open("user_stats.json", "r") as file:
            user_stats = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не существует или не содержит JSON-данных, создаем пустую структуру
        user_stats = {}

    # Обновляем статистику для текущего дня
    if today not in user_stats:
        user_stats[today] = []

    if user_id not in user_stats[today]:
        user_stats[today].append(user_id)

    # Записываем обновленную статистику обратно в файл
    with open("user_stats.json", "w") as file:
        json.dump(user_stats, file, indent=4)

# Добавьте обработчики для остальных разделов меню, а также для подразделов и действий

# Запуск бота
bot.polling()
