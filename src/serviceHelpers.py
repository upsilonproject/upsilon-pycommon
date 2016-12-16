import urllib2
import sys
import json

# Taken from PyNag.
OK, WARNING, CRITICAL, UNKNOWN = 0, 1, 2, 3

def req(auth_url, auth_req_data):
		auth_req = urllib2.Request(auth_url, data=auth_req_data)
		auth_resp = urllib2.urlopen(auth_req)
		auth_resp_content = auth_resp.read()

		return auth_resp_content;

def reqJson(url, data = None):
		if data == None:
				data = {}

		return json.loads(req(url, json.dumps(data)));

def exitOk(metadata = None, message = None):
        exit(OK, metadata, message)

def exitWarning(metadata = None, message = None):
        exit(WARNING, metadata, message)

def exitCritical(metadata = None, message = None):
        exit(CRITICAL, metadata, message)

def exitUnknown(metadata = None, message = None):
        exit(UNKNOWN, metadata, message)

def exit(status = OK, metadata = None, message = None):
	if not metadata == None:
		print "<json>%s</json>" % json.dumps(metadata)

	print message
	sys.exit(status);

class clsmetadata(dict):
	def __init__(self):
		self['metrics'] = list()
		self['subresults'] = list()

	def addSubresult(self, name, karma = "GOOD", comment = None):
		self['subresults'].append({"name": name, "karma": karma, "comment": comment});

	def addMetric(self, name, value, karma = "GOOD"):
                metric ={"name": name, "value": value, "karma": karma}

		self['metrics'].append(metric)

                return metric
