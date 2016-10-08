import httplib
import socket
import sys
from urlparse import urlparse
from config import error

def getHttpClient(ssl, address, port = 80, timeout = 10):
	if ssl:
		httpClient = httplib.HTTPSConnection(address + ":" + str(port), timeout=timeout)
	else:
		httpClient = httplib.HTTPConnection(address + ":" + str(port), timeout=timeout)
	
	return httpClient

def getHttpContent(client, url):
	try:
		client.request("GET", url)
		res = client.getresponse()
	except socket.error as e:
		print "Could not even connect. Upsilon may not be running at this address & port."
		print "Socket error: " + str(e)
		sys.exit()
	except httplib.BadStatusLine as e:
		print "Connected, but could not parse HTTP response."
		print "If this server is running SSL, try again with --ssl"
		sys.exit()

	if res.status == 302 and res.getheader('Location'):
		res.read()
		return getHttpContent(client, "/" + res.getheader('Location'));
	if res.status == 301:
		res.read()
		parts = urlparse(res.getheader('Location'))
		location = parts.path
		return getHttpContent(client, location);

	if res.status != 200:
		error("Requested: %s, Expected HTTP 200, got HTTP %d" % (url, res.status))

	res = res.read()

	assert len(res) > 0, "Expected non-empty response."

	return res

