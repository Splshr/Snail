import requests

# Замените 'YOUR_BOT_TOKEN' на реальный токен вашего бота
bot_token = ' '

# Замените 'CHAT_ID' на айди чата, в который вы хотите отправить сообщение
chat_id = ' '

# Открываем файл изображения в бинарном режиме
with open('PHOTO PATH', 'rb') as photo:
    # Отправляем POST-запрос к API Telegram с методом sendPhoto для отправки изображения
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                             data={'chat_id': chat_id, 'caption': 'Тільки у Равлику! Акція!'},
                             files={'photo': photo})

# Печатаем ответ сервера Telegram
print(response.text)
