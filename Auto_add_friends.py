import os
import time
import random
import vk_api
import requests
from PIL import Image
import urllib.request

def captcha(url):
    urllib.request.urlretrieve(url, "./Captcha/captcha.jfif")
    Image.open("./Captcha/captcha.jfif").save("./Captcha/captcha.png")

    key = "f18cca4cadb1c07bd6b528a476e144f1" 
    data = {"key" : key}
    files = {"file": open("./Captcha/captcha.png", "rb")}

    response = requests.post("https://rucaptcha.com/in.php", data=data, files=files)
    print("Отправка запроса на решение капчи...")
    if(response.status_code == 200):
        print("Запрос отправлен успешно! Будем запрашивать ответ через 5 секунд")
        id = str(response.text).split('|')[1]
        while True:
            time.sleep(5)
            print("Запрос ответа...")
            response = requests.get("https://rucaptcha.com/res.php?key=" + key + "&action=get&id=" + id)
            if(str(response.text).split('|')[0] == "OK"):
                print("Капча готова: " + str(response.text).split('|')[1])
                return str(response.text).split('|')[1]
            elif(str(response.text) == "CAPCHA_NOT_READY"):
                print("Капча еще не готова, повторим запрос через 5 сек...")
            else:
                print("Неизвестный ответ: " + str(response.text))
                if(input("Продолжить запросы? (y/n) ").upper() == "Y"):
                    print("Повторим запрос через 5 сек...")
                    continue
                else:
                    print("Отменено пользователем.")
                    return -1

def add_firend_captcha(id, sid, key):
    api.method('friends.add', {'user_id': id, 'captcha_sid': sid, 'captcha_key':key})

os.system('clear')

print('''
░█████╗░██╗░░░██╗████████╗░█████╗░  ░█████╗░██████╗░██████╗░
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗  ██╔══██╗██╔══██╗██╔══██╗
███████║██║░░░██║░░░██║░░░██║░░██║  ███████║██║░░██║██║░░██║
██╔══██║██║░░░██║░░░██║░░░██║░░██║  ██╔══██║██║░░██║██║░░██║
██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝  ██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░  ╚═╝░░╚═╝╚═════╝░╚═════╝░

███████╗██████╗░██╗███████╗███╗░░██╗██████╗░░██████╗
██╔════╝██╔══██╗██║██╔════╝████╗░██║██╔══██╗██╔════╝
█████╗░░██████╔╝██║█████╗░░██╔██╗██║██║░░██║╚█████╗░
██╔══╝░░██╔══██╗██║██╔══╝░░██║╚████║██║░░██║░╚═══██╗
██║░░░░░██║░░██║██║███████╗██║░╚███║██████╔╝██████╔╝
╚═╝░░░░░╚═╝░░╚═╝╚═╝╚══════╝╚═╝░░╚══╝╚═════╝░╚═════╝░
''')

TOKEN = input('Введите токен>')

FRIENDS_COUNT = int(input('Сколько накрутить друзей>'))

DELAY = 5

GROUPS_IDS = (-53294903,-51445749)

ADDED_USERS = []

RUCAPTCHA  = True

api = vk_api.VkApi(token=TOKEN)

while FRIENDS_COUNT:
    time.sleep(DELAY)
    try:
        user_post = api.method('wall.get', {'owner_id':random.choice(GROUPS_IDS), 'count':1})
        user_id = user_post["items"][0]["from_id"]
        if user_id not in ADDED_USERS:

            api.method('friends.add', {'user_id':user_id})

            FRIENDS_COUNT -= 1

            ADDED_USERS.append(user_id)

            if FRIENDS_COUNT != 0:
                print(f'Добавил в друзья vk.com/id{user_id}\nОсталось накрутить {FRIENDS_COUNT}')
            elif FRIENDS_COUNT == 0:
                print('Накрутка завершена!')
    except vk_api.exceptions.Captcha as captcha:
        if RUCAPTCHA:
            try:
                captcha_compl = captcha(captcha.get_url())
                if(captcha_compl == -1):
                    print("Отмена в связи с ошибкой капчи!")
                    break
                else:
                    try:
                        add_firend_captcha(user_id, captcha.sid, captcha_compl)
                    except:
                        print("Попалась неправильная капча")
            except:
                pass
        if not RUCAPTCHA:
            try:
                captcha.sid
                print(f'Появилась капча - {captcha.get_url()}')
                captcha_key = input('Введите капчу:')
                captcha.try_again(captcha_key) 
            except:
                pass
    except vk_api.exceptions.VkApiError:
        pass

