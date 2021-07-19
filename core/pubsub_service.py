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
    destination = "models_botservice"

    data = current_service_integrator([Contact])

    data = json.dumps(data, indent=2)  

    conn = stomp.Connection(host_and_ports = [(host, port)])
    # conn.start()
    conn.connect(login=user,passcode=password)
    
    conn.send(destination, data, persistent='true')
    
    conn.send(destination, "SHUTDOWN", persistent='true')

    conn.disconnect()

def listener():

    user = os.getenv("ACTIVEMQ_USER") or "admin"
    password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
    host = os.getenv("ACTIVEMQ_HOST") or "localhost"
    port = os.getenv("ACTIVEMQ_PORT") or 61613
    destination = sys.argv[1:2] or ["/topic/event"]
    destination = "models_mailservice"
    destination2 = "models_reposervice"
    destination3 = "models_mainservice"
    destination4 = "models_userauthservice"

    class MyListener(object):
    
        def __init__(self, conn):
            self.conn = conn
            self.count = 0
            self.start = time.time()
        
        def on_error(self, message):
            print('received an error %s' % message)

        def on_message(self, message):
            if message.body == "SHUTDOWN":
        
                diff = time.time() - self.start
                print("Received %s in %f seconds" % (self.count, diff))
                conn.disconnect()
                sys.exit(0)
            
            else:
                if self.count==0:
                    data_receive = json.loads(message.body)
                    self.start = time.time()
                    insert_data(data_receive)
            
                self.count += 1
                if self.count % 2 == 0:
                    print("Received %s messages." % self.count)

    conn = stomp.Connection(host_and_ports = [(host, port)])
    conn.set_listener('', MyListener(conn))

    conn.connect(login=user,passcode=password)
    conn.subscribe(id='stomp_listener', destination=destination, ack='auto')
    conn.subscribe(id='stomp_listener', destination=destination2, ack='auto')
    conn.subscribe(id='stomp_listener', destination=destination3, ack='auto')
    conn.subscribe(id='stomp_listener', destination=destination4, ack='auto')
    

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