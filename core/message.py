import requests
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.models import Contact, ChatHeader
import json

TOKEN = '1636613930:AAFSFWtN1wb9ueDP4lZKhLfle8f_IGOOzd4'

bot = telegram.Bot(token=TOKEN)


def proccess(data):

    if 'entities' in data['message']:
        indented = json.dumps(data, indent=2)
        print(indented)

    elif "contact" in data['message']:
        msg = msg_handler(data)
        create_user(msg)

    else:
        msg = msg_handler(data)
        login(msg)


def msg_handler(data):

    user_id = data['message']['from']['id']
    first_name = data['message']['from']['first_name']
    last_name = data['message']['from']['last_name']

    msg = {
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
    }

    if 'contact' in data['message']:
        msg['phone_number'] = data['message']['contact']['phone_number']

    return msg


def msg_login(msg):

    reply_markup = telegram.ReplyKeyboardMarkup(
        [[telegram.KeyboardButton("Compartilhar número de telefone", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    bot.sendMessage(
        msg['user_id'], "Por favor, compartilhe o seu número de telefone para efetuar o seu cadastro", reply_markup=reply_markup
    )


def login(msg):

    try:
        contact = Contact.objects.get(user_id=msg['user_id'])
        chat_header = ['\U0001F537/%s: %s' % (c.name.replace(' ', '_'), c.description)
                       for c in ChatHeader.objects.all()]
        formated = str.join('\n', chat_header)
        # text_header = 'Comandos disponíveis'
        text = '***Comandos disponíveis***\n\n' + formated
        bot.sendMessage(msg['user_id'], text)

    except Contact.DoesNotExist:

        msg_login(msg)


def create_user(msg):

    Contact(
        user_id=msg["user_id"],
        first_name=msg["first_name"],
        last_name=msg["last_name"],
        phone_number=msg["phone_number"],
    ).save()

    text = 'Seja bem-vindo {} {} \U0001F642'.format(msg['first_name'], msg['last_name'])
    bot.sendMessage(msg['user_id'], text)
