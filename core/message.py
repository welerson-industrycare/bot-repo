import requests
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.models import Contact
import json

TOKEN = '1636613930:AAFSFWtN1wb9ueDP4lZKhLfle8f_IGOOzd4'

bot = telegram.Bot(token=TOKEN)

def proccess(data):
    user =  user_handler(data)
    login(user, data)


def user_handler(data):

        user_id = data['message']['from']['id']
        first_name = data['message']['from']['first_name']
        last_name = data['message']['from']['last_name']

        user = {
            'user_id':user_id,
            'first_name':first_name,
            'last_name':last_name,
        }

        return user

def login(user, data):

    reply_markup = telegram.ReplyKeyboardMarkup(
        [[telegram.KeyboardButton("Click para Login", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    bot.sendMessage(
        user["user_id"], "Preciso autorizar seu acesso.", reply_markup=reply_markup
    )

    user["phone_number"] = data['message']['contact']['phone_number']

    if user['phone_number']:
         Contact(
                        user_id=user["user_id"],
                        first_name=user["first_name"],
                        last_name=user["last_name"],
                        phone_number=user["phone_number"],
                    ).save()



# def send_message(text, chat_id):
#     url = 'https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN)
#     data = {'chat_id':chat_id, 'text':text}
#     response = requests.post(url, data=data)
#     print(response.content)
#
#
#
