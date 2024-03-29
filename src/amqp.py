import pika
import uuid
import logging
from threading import Thread
from time import sleep

class UpsilonMessage():
    routingKey = "*"
    headers = {}
    replyTo = ""
    body = ""

    def __init__(self, msgType):
        if msgType != None:
            self.headers["upsilon-msg-type"] = msgType

    def getProperties(self):
        return pika.BasicProperties(
            headers = self.headers,
            reply_to = self.replyTo
            );

class Heartbeater:
    amqp = None
    identifier = None
    version = None
    traits = None
    
    def setIdentitiy(self, identifier = None, version = None, traits = None):
        self.identifier = identifier
        self.version = version
        self.traits = traits

    def setAmqpConnection(self, amqpConnection):
        self.amqp = amqpConnection

    def tick(self):
        while True:
            try: 
                logging.info("Sending heartbeat with identifier: " + self.identifier)

                message = UpsilonMessage("HEARTBEAT");
                message.routingKey = "upsilon.node.heartbeats"
                message.headers["node-identifier"] = self.identifier
                message.headers["node-version"] = self.version
                message.headers["node-type"] = self.traits

                self.amqp.publishMessage(message)

                sleep(60)
            except Exception as e:
                logging.error("Error in heartbeater", e)
                

    def start(self):
        Thread(target = self.tick).start()

class ConsumeTimeout(Exception):
    pass

class UpsilonDelivery(object):
    channel = None
    delivery = None
    properties = None
    body = None

    def __init__(self, channel, delivery, properties, body):
        self.channel = channel
        self.delivery = delivery
        self.properties = properties
        self.body = body

class Connection():
    messageHandlers = []
    messageTypeHandlers = {}

    consumeTimeout = 0

    expectedMessage = ()

    nodeIdentifier = "???"
    nodeVersion = "?.?.?"
    nodeType = "???"

    def __init__(self, host = None, queue = None, exchange = "ex_upsilon", callback = None, connect = True, consumeTimeout = 0):
        if host == None:
            host = "upsilon"

        self.host = host

        if queue == None:
            queue = "untitled"

        self.queue = queue + '-' + str(uuid.uuid4())
        self.exchange = exchange

        if callback != None:
            self.addMessageHandler(callback)

        if consumeTimeout > 0:
            self.consumeTimeout = consumeTimeout

        if connect:
            self.connect()

    def setConsumeTimeout(self, seconds):
        self.consumeTimeout = seconds

    def onConsumeTimeout(self):
        raise ConsumeTimeout("Consume timeout")
    
    def connect(self): 
        self.conn = self.newConn(self.host, self.queue, self.exchange)
        self.channel = self.newChannel()
 
        self.channel._impl.add_on_close_callback(self.onClose)
        self.channel.basic_consume(self.callbackHelper, queue = self.queue)
     
    def newConn(self, host, queue, exchange = "ex_upsilon"):
        params = pika.ConnectionParameters(host = host)
        amqpConnection = pika.BlockingConnection(params)

        if self.consumeTimeout > 0:
            amqpConnection.add_timeout(self.consumeTimeout, self.onConsumeTimeout)

        if not amqpConnection.is_open:
            raise Exception("Could not open a connection")

        logging.log("AMQP Connection open to " + host + ' using the ' + exchange + ' exchange')

        return amqpConnection

    def newChannel(self):
        channel = self.conn.channel();
        channel.queue_declare(queue = self.queue, durable = False, auto_delete = True)

        return channel

    def onClose(self, channel, reply_code, reply_text):
        logging.log("AMQP Connection closed on channel " + str(channel) + ' . Reply code: ' + str(reply_code) + '. Reply text: ' + str(reply_text))

    def setPingReply(self, identifier = "???", version = "?.?.?", traits = "???"):
        self.nodeIdentifier = identifier;
        self.nodeVersion = version;
        self.nodeType = traits;

        self.bind("upsilon.cmds")

        self.addMessageTypeHandler("REQ_NODE_SUMMARY", self.onPing)

    def startHeartbeater(self):
        heartbeater = Heartbeater()
        heartbeater.setIdentitiy(self.nodeIdentifier, self.nodeVersion, self.nodeType);
        heartbeater.setAmqpConnection(self)
        heartbeater.start()


    def onPing(self, channel, delivery, properties, body):
        msg = UpsilonMessage("RES_NODE_SUMMARY")
        msg.routingKey = "upsilon.res"
        msg.headers["node-identifier"] = self.nodeIdentifier;
        msg.headers["node-version"] = self.nodeVersion;
        msg.headers["node-type"] = self.nodeType;

        self.publishMessage(msg)
        
    def publish(self, key, headers, body, replyTo = None):
        properties = pika.BasicProperties(headers = headers, reply_to = replyTo)

        self.channel.basic_publish(exchange = self.exchange, routing_key = key, properties = properties, body = body) 

    def publishMessage(self, msg):
        self.channel.basic_publish(exchange = self.exchange, routing_key = msg.routingKey, properties = msg.getProperties(), body = msg.body)

    def close(self):
        self.channel.stop_consuming()
        self.channel.close()

    def bindEverything(self):
        bindEverything(self.channel, self.queue, self.exchange);

        return self

    def bind(self, key):
        self.channel.queue_bind(queue = self.queue, exchange = self.exchange, routing_key = key)

    def addMessageTypeHandler(self, msgType, callback):
        self.messageTypeHandlers[msgType] = callback

    def addMessageHandler(self, callback):
        self.messageHandlers.append(callback)

    def onExpectedMessage(self, channel, delivery, properties, body):
        self.expectedMessage = UpsilonDelivery(channel, delivery, properties, body)
        self.close()

    def consumeUntilMessage(self, msgType): 
        self.addMessageTypeHandler(msgType, self.onExpectedMessage)

        self.startConsuming()

        return self.expectedMessage

    def callbackHelper(self, channel, delivery, properties, body):
        try:
            if "upsilon-msg-type" in properties.headers:
                msgType = properties.headers["upsilon-msg-type"]
                
                if msgType in self.messageTypeHandlers:
                    callback = self.messageTypeHandlers[msgType]
                    callback(channel, delivery, properties, body)

            for callback in self.messageHandlers:
                callback(channel, delivery, properties, body)
        except Exception as e:
            logging.error("Exception in callback helper: " + str(e))

    def startConsuming(self):
        self.channel.start_consuming()
        logging.debug("finished consuming")

def newChannel(host, queue, exchange = "ex_upsilon"):
    params = pika.ConnectionParameters(host = host)
    amqpConnection = pika.BlockingConnection(params)

    if not amqpConnection.is_open:
        raise Exception("Could not open a connection")
    
    logging.log("AMQP Connection open to " + host + ' using the ' + exchange + ' exchange')
    
    channel = amqpConnection.channel();
    channel.queue_declare(queue = queue, durable = False, auto_delete = True)
    
    return channel

def bindEverything(channel, queue, exchange = "ex_upsilon"):
    channel.queue_bind(queue = queue, exchange = exchange, routing_key = '*')
    channel.queue_bind(queue = queue, exchange = exchange, routing_key = '#')
