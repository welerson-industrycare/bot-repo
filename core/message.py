import requests
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '1636613930:AAFSFWtN1wb9ueDP4lZKhLfle8f_IGOOzd4'

bot = telegram.Bot(token=TOKEN)

# def create_user(data):
#
#         msg = {
#             'user_id':user_id,
#             'first_name':first_name,
#             'last_name':last_name,
#         }
#
#
#         print('User ID:{}'.format(user_id))
#         print('First Name:{}'.format(first_name))
#         print('Last Name:{}'.format(last_name))
#         print('Phone Number:{}'.format(phone_number))

def send_message(text, chat_id):
    url = 'https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN)
    data = {'chat_id':chat_id, 'text':text}
    response = requests.post(url, data=data)
    print(response.content)



def login(user, data):
    """
    Interacts with the contact, requesting your data to authorize access.
    :param msg: Message from contact
    """
    reply_markup = telegram.ReplyKeyboardMarkup(
        [[telegram.KeyboardButton("Click para Login", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    bot.sendMessage(
        user["user_id"], "Preciso autorizar seu acesso.", reply_markup=reply_markup
    )

    print(data)
