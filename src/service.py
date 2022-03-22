import urllib.request, urllib.error, urllib.parse
import sys
from subprocess import Popen, PIPE
import json

# Taken from PyNag.
OK, WARNING, CRITICAL, UNKNOWN = 0, 1, 2, 3

def http_req(auth_url, auth_req_data):
        auth_req = urllib.request.Request(auth_url, data=auth_req_data)
        auth_resp = urllib.request.urlopen(auth_req)
        auth_resp_content = auth_resp.read()

        return auth_resp_content;

def http_req_json(url, data = None):
        if data == None:
                data = {}

        return json.loads(req(url, json.dumps(data)));

def easyexec(command):
    p = Popen(command, stdout = PIPE, stderr = PIPE)
    out, err = p.communicate()

    return out.decode("utf-8").strip(), err.decode("utf-8").strip()

class ServiceController(dict):
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

    def exitOk(self, message = None):
        self.exit(OK, message)

    def exitWarning(self, message = None):
        self.exit(WARNING, message)

    def exitCritical(self, message = None):
        self.exit(CRITICAL, message)

    def exitUnknown(self, message = None):
        self.exit(UNKNOWN, message)

    def exit(self, status = OK, message = None):
        print(("<json>%s</json>" % json.dumps(self, indent = 4)))

        if message is not None:
            print(message)

        sys.exit(status);

