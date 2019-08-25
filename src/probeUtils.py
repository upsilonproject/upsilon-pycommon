import urllib2
import sys
from subprocess import Popen, PIPE
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

def easyexec(command):
    p = Popen(command, stdout = PIPE, stderr = PIPE)
    out, err = p.communicate()

    return out.strip(), err

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
        print "<json>%s</json>" % json.dumps(metadata, indent = 4)

    print message
    sys.exit(status);

class clsmetadata(dict):
    def __init__(self):
        self['metrics'] = list()
        self['entities'] = list()

    def addSubresult(self, name, karma = "GOOD", value = "", comment = None):
        return self.addEntity(name, "subresult", karma, value, comment);

    def addEntity(self, name, classType = "", karma = "GOOD", value = "", comment = None):
        entity = {"name": name, "type": classType, "karma": karma, "value": value, "comment": comment, "properties": dict()}

        self['entities'].append(entity);

        return entity;

    def addMetric(self, name, value, karma = "GOOD"):
        metric = {"name": name, "value": value, "karma": karma}

        self['metrics'].append(metric)

        return metric
