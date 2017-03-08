from upsilon import amqp
import unittest

class BasicConnection(unittest.TestCase):
    def testConn(self):
        conn = amqp.Connection("upsilon")

        self.assertIsNotNone(conn)
