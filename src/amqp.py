import pika
import uuid

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


class Connection():
    messageHandlers = []
    messageTypeHandlers = {}

    nodeIdentifier = "???";
    nodeVersion = "?.?.?"
    nodeType = "???";

    def __init__(self, host = None, queue = None, exchange = "ex_upsilon", callback = None):
        if host == None:
            host = "upsilon"

        self.host = host

        if queue == None:
            queue = str(uuid.uuid4())

        self.queue = queue

        self.exchange = exchange

        self.channel = newChannel(host, queue, exchange)

        if callback != None:
            self.addMessageHandler(callback)

        self.channel.basic_consume(self.callbackHelper, queue = self.queue)

    def setPingReply(self, identifier = "???", version = "?.?.?", traits = "???"):
        self.nodeIdentifier = identifier;
        self.nodeVersion = version;
        self.nodeType = traits;

        self.addMessageTypeHandler("REQ_NODE_SUMMARY", self.onPing)

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
        print "closing"
        self.channel.stop_consuming()
        self.channel.close()
        print "closed"

    def bindEverything(self):
        bindEverything(self.channel, self.queue, self.exchange);

        return self

    def bind(self, key):
        self.channel.queue_bind(queue = self.queue, exchange = self.exchange, routing_key = key)

    def addMessageTypeHandler(self, msgType, callback):
        self.messageTypeHandlers[msgType] = callback

    def addMessageHandler(self, callback):
        self.messageHandlers.append(callback)

    def callbackHelper(self, channel, delivery, properties, body):
        if "upsilon-msg-type" in properties.headers:
            msgType = properties.headers["upsilon-msg-type"]
            
            if msgType in self.messageTypeHandlers:
                callback = self.messageTypeHandlers[msgType]
                callback(channel, delivery, properties, body)

        for callback in self.messageHandlers:
            callback(channel, delivery, properties, body)
        
    def startConsuming(self):
        self.channel.start_consuming()
        print "finished consuming"

def newChannel(host, queue, exchange = "ex_upsilon"):
        params = pika.ConnectionParameters(host = host)
        amqpConnection = pika.BlockingConnection(params)

        if not amqpConnection.is_open:
            raise Exception("Could not open a connection")

        print "Connection open to", host, ' using the', exchange, 'exchange'

	channel = amqpConnection.channel();
	channel.queue_declare(queue = queue, durable = False, auto_delete = True)

	return channel

def bindEverything(channel, queue, exchange = "ex_upsilon"):
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '*')
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '#')
