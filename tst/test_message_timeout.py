from upsilon import amqp
import unittest

class BasicConnection(unittest.TestCase):
    def onTimeout(self):
        print "timeout"

    def testConn(self):
        conn = amqp.Connection("upsilon", connect = False)
        conn.addTimeout(4, self.onTimeout)
        conn.connect()

        msg = amqp.UpsilonMessage("REQ_UNKNOWN")

        conn.publishMessage(msg)
