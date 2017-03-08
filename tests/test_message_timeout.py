from upsilon import amqp
import unittest
import pytest

class BasicConnection(unittest.TestCase):
    @pytest.mark.timeout(5)
    def testConn(self):
        conn = amqp.Connection("upsilon", consumeTimeout = 3)

        msg = amqp.UpsilonMessage("REQ_UNKNOWN")

        conn.publishMessage(msg)

        try:
            conn.startConsuming()
        except amqp.ConsumeTimeout:
            print "consume timeout"
