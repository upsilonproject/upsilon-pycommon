import pika
import uuid

class Connection():
    messageHandlers = []

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

    def addMessageHandler(self, callback):
        self.messageHandlers.append(callback)

    def callbackHelper(self, channel, delivery, headers, body):
        for callback in self.messageHandlers:
            callback(channel, delivery, headers, body)
        
    def startConsuming(self):
        self.channel.start_consuming()
        print "finished consuming"

def newChannel(host, queue, exchange = "ex_upsilon"):
        params = pika.ConnectionParameters(host = host)
        amqpConnection = pika.BlockingConnection(params)

        if not amqpConnection.is_open:
            raise Exception("Could not open a connection")

	channel = amqpConnection.channel();
	channel.queue_declare(queue = queue, durable = False, auto_delete = True)

	return channel

def bindEverything(channel, queue, exchange = "ex_upsilon"):
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '*')
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '#')
