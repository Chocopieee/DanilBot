import telebot, apiai, json
from face_rec import classify_face

bot = telebot.TeleBot('1463138854:AAG7zJ-SZAP2eva0SG4wVol0l65-gXuLj00')
print("Успешно подключено.")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)

def tomsg(message):
    msg = message.text.lower().replace('. ', ' ').replace('! ', ' ').replace('? ', ' ').replace('.', '').replace('!', '').replace('?', '').replace('-', '').replace('  ', ' ')
    return msg

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я могу распознавать людей на фото.\n\nКоманды:\n\n1. Кто это / Кто на фото\n\nПока что доступна только одна команда, но также вы можете со мной просто поговорить.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    msg = tomsg(message)

    if msg in ['привет', 'здарова', 'ку', 'ку ку']:
        bot.send_message(message.chat.id, 'Ну привет.')
    elif msg in ['пока', 'до связи', 'до свидания', 'бб']:
        bot.send_message(message.chat.id, 'До связи.')
    elif msg in ['как дела', 'как ты', 'чо как']:
        bot.send_message(message.chat.id, 'Отлично.')
    elif msg in ['ты всего лишь робот', 'ты робот', 'ты железка', 'ты не живой']:
        bot.send_message(message.chat.id, 'Ну да, и что?')
    elif msg in ['кто ты', 'ты кто', 'как тебя зовут', 'как твоё имя']:
        bot.send_message(message.chat.id, 'Я всего-лишь робот.')
    elif msg in ['кто это', 'это кто', 'кто на фото', 'распознай', '1']:
        sended_msg = bot.send_message(message.chat.id, 'Теперь отправь мне фото, которое нужно распознать.')
        bot.register_next_step_handler(sended_msg, who_is)
    else:
        bot.send_message(message.chat.id, 'Я Вас не понял.')

def who_is(message):
    if message.photo != None:
        print("Новое фото! Скачиваю...")
        file_id = message.json['photo'][0]['file_id']
        file = bot.get_file(file_id)
        downloaded_file = bot.download_file(file.file_path)
        src = (f"download/{file_id}.jpg")
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        print("Файл загружен.")
        people = []
        ans = ""
        for person in classify_face(src):
            if person == "Unknown":
                sended_msg = bot.send_message(message.chat.id, 'Я не знаю этого человека.\nСкажи мне как его называть, чтобы я запомнил его, или напиши "Отмена".')
                bot.register_next_step_handler(sended_msg, set_name, downloaded_file)
            else:
                ans = ans + person + "\n"
        if ans != "":
            bot.send_message(message.chat.id, (f"Это {ans}"))
    else:
        bot.send_message(message.chat.id, "Это не фото 🤠")

def set_name(message, pic):
    if tomsg(message) != "отмена":
        name = message.text
        bot.send_message(message.chat.id, (f'Хорошо, это {name}.'))
        print("Новая личность! Сохраняю...")
        src = (f"faces/{name}.jpg")
        with open(src, 'wb') as new_file:
            new_file.write(pic)
        print("Файл загружен, новая персона.")
    else:
        bot.send_message(message.chat.id, 'Вы отменили действие.')

bot.polling()
