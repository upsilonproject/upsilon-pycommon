import pika

def newChannel(host, queue, exchange = "ex_upsilon"):
	amqpConnection = pika.BlockingConnection(pika.ConnectionParameters(host = host))
	print "conn:", amqpConnection.is_open

	channel = amqpConnection.channel();
	channel.queue_declare(queue = queue, durable = False, auto_delete = True)
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = 'upsilon.node.serviceresults');
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '#');
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '*');

	return channel

def bindEverything(channel, queue, exchange = "ex_upsilon"):
	channel.queue_bind(queue = queue, exchange = exchange, routing_key = '*')
