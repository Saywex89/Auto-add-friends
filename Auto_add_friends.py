import os
import time
import random
import vk_api

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
        captcha.sid  
        print(f'Появилась капча - {captcha.get_url()}')
        captcha_key = input('Введите капчу:')
        captcha.try_again(captcha_key)   
    except vk_api.exceptions.VkApiError:
            pass


