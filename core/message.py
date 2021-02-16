import requests
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '1636613930:AAFSFWtN1wb9ueDP4lZKhLfle8f_IGOOzd4'


def create_user(data):
        user_id = data['message']['from']['id']
        first_name = data['message']['from']['first_name']
        last_name = data['message']['from']['last_name']
        phone_number = data['message']['text']
        print('User ID:{}'.format(user_id))
        print('First Name:{}'.format(first_name))
        print('Last Name:{}'.format(last_name))
        print('Phone Number:{}'.format(phone_number))

def send_message(text, chat_id):
    url = 'https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN)
    data = {'chat_id':chat_id, 'text':text}
    response = requests.post(url, data=data)
    print(response.content)


# def msg_login(msg):
#     """
#     Interacts with the contact, requesting your data to authorize access.
#     :param msg: Message from contact
#     """
#     reply_markup = telegram.ReplyKeyboardMarkup(
#         [[telegram.KeyboardButton("Click para Login", request_contact=True)]],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#     )
#     bot.sendMessage(
#         msg["user_id"], "Preciso autorizar seu acesso.", reply_markup=reply_markup
#     )
