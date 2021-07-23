import time
import sys
import os
import json
import stomp

from django.db import IntegrityError, transaction
from core.models import Contact, MultiServiceIntegrator
from common.multiservice_integrator import current_service_integrator


def publisher():

    user = os.getenv("ACTIVEMQ_USER") or "admin"
    password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
    host = os.getenv("ACTIVEMQ_HOST") or "localhost"
    port = os.getenv("ACTIVEMQ_PORT") or 61613
    destination = sys.argv[1:2] or ["/topic/event"]
    destination = "/topic/models_botservice"

    data = current_service_integrator([Contact])

    data = json.dumps(data, indent=2)  

    conn = stomp.Connection(host_and_ports = [(host, port)])
    conn.connect(login=user,passcode=password)
    conn.send(destination, data, persistent='true')
    conn.disconnect()

def listener():

    user = os.getenv("ACTIVEMQ_USER") or "admin"
    password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
    host = os.getenv("ACTIVEMQ_HOST") or "localhost"
    port = os.getenv("ACTIVEMQ_PORT") or 61613
    mailservice = "/topic/models_mailservice"
    reposervice = "/topic/models_reposervice"
    mainservice = "/topic/models_mainservice"
    userauthservice = "/topic/models_userauthservice"

    class MyListener(object):
    
        def __init__(self, conn):
            self.conn = conn
        
        def on_error(self, message):
            print('received an error %s' % message)

        def on_message(self, message):
            data_receive = json.loads(message.body)
            insert_data(data_receive)
            

    conn = stomp.Connection(host_and_ports = [(host, port)])
    conn.set_listener('', MyListener(conn))

    conn.connect(login=user,passcode=password, wait=True, headers={'client-id':'botClient'})
    conn.subscribe(id='bot_listener_1', destination=mailservice, ack='auto', headers={'activemq.subscriptionName':'bot_mail'})
    conn.subscribe(id='bot_listener_2', destination=reposervice, ack='auto', headers={'activemq.subscriptionName':'bot_repo'})
    conn.subscribe(id='bot_listener_3', destination=mainservice, ack='auto', headers={'activemq.subscriptionName':'bot_main'})
    conn.subscribe(id='bot_listener_4', destination=userauthservice, ack='auto', headers={'activemq.subscriptionName':'bot_user'})
    

    print('sent message')

    print("Waiting for messages...")


@transaction.atomic
def insert_data(data_receive):

    data = data_receive

    try:
        with transaction.atomic():
            try:
                for d in data:
                    instance = MultiServiceIntegrator()    

                    instance.nome_msi = d['nome_msi']
                    instance.flab_msi = d['flab_msi']
                    instance.sql_msi = d['sql_msi']

                    instance.save(using='default')

            except Exception as error:
                print(error)

    except IntegrityError as error:
        print(error)