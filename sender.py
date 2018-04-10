import logging
from flask import Flask
from azure.servicebus import Message
from flask import request
from flask import Response
from azure.servicebus import ServiceBusService

app = Flask(__name__)

@app.route('/',methods = ['POST'])
def recieve_msg():
    #send msg from payload...
    if 'msg' not in request.form:
        resp = Response("No message(msg) specified", status=400)
        return resp
   
    if 'topic' not in request.form:
        resp = Response("No topic specified", status=400)
        return resp

    topic = request.form.get('topic')
    msg = request.form.get('msg')

    send_msg(topic, msg) 
    
    app.log.info("topic:%s message:%s" % (topic, msg) )
    return Response("Okay", status=200)


def send_msg(topic, msg):
    sb_msg = Message(msg)
    app.sbs.send_topic_message(topic, sb_msg)

def init():
    config = {}
    exec(open("config.conf").read(), config)
    namespace = config['namespace']
    acc_name = config['acc_name']
    acc_key = config['acc_key']
 
    app.sbs = ServiceBusService(namespace, shared_access_key_name=acc_name, shared_access_key_value=acc_key)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('sender.log')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    app.log = logger

if __name__=='__main__':
    init()
    app.run()
    