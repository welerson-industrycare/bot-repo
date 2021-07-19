import requests
import telegram
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.models import Contact, BotHeader, BotContent
import json
from django.db import connections
import re
from django.db.models import Q
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import io
from chatbot.settings import TELEGRAM_TOKEN, BOT_URL
from common.multiservice_integrator import *


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)
URL = BOT_URL.format(TELEGRAM_TOKEN)


def proccess(data):

    """
    Function that receive a json request "data"
    """

    if "contact" in data['message']:
        msg = msg_handler(data)
        create_user(msg)

    elif 'entities' in data['message']:
       
        command = data['message']['text']
        
        replace_keys = {'/':'', '_':' '}

        cmd_formated = cmd_formatter(command, replace_keys, True)


        cmd = callback(cmd_formated)

        if cmd:
            
          make_table(cmd, data)

    else:
        msg = msg_handler(data)
        login(msg)

        

def make_table(cmd, data):

    report = query_handler(cmd)

    user_id = data['message']['from']['id']
    label_x = 'num'
    label_y = 'py'
    header_title = BotHeader.objects.get(id=cmd)
    title_h = header_title.description.replace(' ', '_')

    graph_config = {
        'h_title': title_h, 
        'y_label': label_y,
        'x_label': label_x
    }

    graph = make_plot(report, graph_config)
    bot.send_photo(user_id, photo=graph)
   
def make_plot(report, graph_config):

    plt.figure()
    plt.plot(report)
    plt.title(graph_config['h_title'])
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
   
    
    return buf

def cmd_formatter(string, replacements, ignore_case=False):


    if ignore_case:
        def normalize_old(s):
            return s.lower()

        re_mode = re.IGNORECASE

    else:
        def normalize_old(s):
            return s

        re_mode = 0

    replacements = {normalize_old(key): val for key, val in replacements.items()}

    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    
    pattern = re.compile('|'.join(rep_escaped), re_mode)

    return pattern.sub(lambda match: replacements[normalize_old(match.group(0))], string)

def callback(cmd):

    """
    Get a command name as parameter and return command name id
    """

    try:
        cmd_name = BotHeader.objects.get(name=cmd)
        return cmd_name.id
    except:
       return False

def query_handler(cmd_id):

    """
    Receive a command id as parameter and return sql query related with the specif command
    """
    query = BotContent.objects.get(header_id=cmd_id)
    cur = connections['default'].cursor()
    cur.execute(query.sql)
    report = cur.fetchall()
    cur.close()

    return report

def msg_handler(data):

    """
    Receive a json request "data" then return a user dict "msg" with user credentials
    """

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

    """
    Create a button in order to get the user phone number
    """

    reply_markup = telegram.ReplyKeyboardMarkup(
        [[telegram.KeyboardButton("Compartilhar número de telefone", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    bot.sendMessage(
        msg['user_id'], "Por favor, compartilhe o seu número de telefone \U0001F4DE	 para efetuar o seu cadastro", reply_markup=reply_markup
    )

def login(msg):

    """
    """

    try:
        contact = Contact.objects.get(user_id=msg['user_id'])
        
        if contact:
            
            return
        # chat_header = ['\U0001F537/%s: %s' % (c.name.replace(' ', '_'), c.description)
        #                for c in Contact.objects.filter(Q(user_id=contact.user_id)|Q(user_id__isnull=True))]
        # formated = str.join('\n', chat_header)
        # text_header = 'Comandos disponíveis'
        # text = '***Comandos disponíveis***\n\n' + formated
        bot.sendMessage(msg['user_id'], text)

    except Contact.DoesNotExist:

        msg_login(msg)

def verify_alerty_occurrencies(msg):
    
    return

def create_user(msg):
    """
    Create a user in botdb
    """
    orm = virtual_orm()

    if 'accounts_user' in orm:
        user = [ u for u in orm['accounts_user'] if u['phone_number'] == msg['phone_number']]
        if len(user) > 0:
            contact = Contact(
                user_id=msg["user_id"],
                contact_id=user[0]["id"],
                first_name=msg["first_name"],
                last_name=msg["last_name"],
                phone_number=msg["phone_number"],
                )
            try:
                contact.save(using='default')
                text = 'Seja bem-vindo {} {}, você foi cadastrado na lista de alertas do seu sistema IndustryCare \U0001F642'.format(msg['first_name'], msg['last_name'])
                bot.sendMessage(msg['user_id'], text)
            
            except Exception as e:
                print('Ocorreu um erro', e)
            
        else:
            bot.sendMessage(msg['user_id'], 'Sinto muito, mas este telefone não foi identificado em nossa base de dados.')
    else:
        bot.sendMessage(msg['user_id'], 'Sinto muito, mas este telefone não foi identificado em nossa base de dados.')
    

    
    
