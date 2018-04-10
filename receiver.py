import logging
import time
import sys
import uuid
from azure.servicebus import ServiceBusService


def start():
    #init
    receiver = init_receiver()

    try:
        while True:
            msg = receiver.receive_from_subscription()

            #ignore empty messages
            if msg.body is None:
                continue
            
            id = str(uuid.uuid4())
            msg_file = open(id, "w")
            msg_file.write(str(msg.as_batch_body()))
            msg.delete()
            msg_file.close()
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')


def init_receiver():
    config = {}
    exec(open("config.conf").read(), config)
    namespace = config['namespace']
    acc_name = config['acc_name']
    acc_key = config['acc_key']
 
    sbs = ServiceBusService(namespace, shared_access_key_name=acc_name, shared_access_key_value=acc_key)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('receiver.log')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    #TODO validated the args
    topic = sys.argv[1]
    subscription = sys.argv[2]

    logger.info("Starting receiving process for topic:%s subscription:%s" % (topic, subscription) )

    return Receiver(sbs, logger, topic, subscription)

class Receiver():
    def __init__(self, sbs, logger, topic, subscription):
        self.__sbs = sbs
        self.__logger = logger
        self.__topic = topic
        self.__subscription = subscription
    
    def receive_from_subscription(self):
        #messages won't be deleted until the delete method is called.
        return self.__sbs.receive_subscription_message(self.__topic, self.__subscription, peek_lock=True)
    
if __name__=='__main__':
    start()
    
    