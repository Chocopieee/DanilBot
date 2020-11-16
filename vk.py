import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import face_rec
import requests

vk_session = vk_api.VkApi(token = '')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def get_button(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }

keybrd_main_start = {
    "one_time" : True,
    "buttons" : [
        [get_button('Привет!', 'positive'), get_button('пока', 'positive')],
        [get_button('привет', 'positive'), get_button('пока', 'positive')]
    ]
}
keybrd_main_start = json.dumps(keybrd_main_start, ensure_ascii = False).encode('utf-8')
keybrd_main_start = str(keybrd_main_start.decode('utf-8'))



def send_msg(id, txt):
    session_api.messages.send(user_id = id, message = txt, random_id = 0)

def send_keyboard(id, table):
    session_api.messages.send(user_id = id, keyboard = table, random_id = 0)

def send_photo(id, url):
    session_api.messages.send(user_id = id, attachment = url, random_id = 0)



for event in longpoll.listen():
    if event.type ==  VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id

            if msg == 'привет!':
                send_msg(id, 'Привет! Ы')
              #  send_photo(id, 'photo-198781344_457239019')
              #  send_keyboard(id, keybrd_main_start)

            if msg == "кто это" or msg == "это кто":
                attachments = event.attachments
              #  info = session_api.photos.get(photo_ids=attachments['attach1'])
                if True:
                  #  photo = requests.get("https://vk.com/photo"+attachments['attach1'])
                    print(attachments)

            #    except:
            #        send_msg(id, 'Ошибка!')
    if event.type == VkEventType.USER_TYPING:
        id = event.user_id
        send_msg(id, 'чо печатаешь да')
