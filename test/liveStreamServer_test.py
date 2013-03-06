#!/usr/bin/python
#-*- coding=utf-8 -*-
##
# @file liveStreamServer_test.py
# @brief unit test for liveStreamServer.py
# @author yy
# @version 0.1
# @date 2012-07-10

from twisted.trial import unittest
from twisted.test import proto_helpers

from liveStreamServer import LiveServer

class LiveServerTestCase(unittest.TestCase):

    def test_connection(self):

        self.factory = LiveServer()
        #build a connection here
        self.transport = proto_helpers.StringTransportWithDisconnection()
        self.protocol = self.factory.buildProtocol(('127.0.0.1', 1557))
        self.transport.protocol = self.protocol
        self.protocol.makeConnection(self.transport)
        self.assertEqual(self.factory.getClientNum(), 1)

        #build another connection here
        self.transport_1 = proto_helpers.StringTransportWithDisconnection()
        self.protocol_1 = self.factory.buildProtocol(('127.0.0.1', 1557))
        self.transport_1.protocol = self.protocol_1
        self.protocol_1.makeConnection(self.transport_1)
        self.assertEqual(self.factory.getClientNum(), 2)

        #tear down the first connection
        self.protocol.transport.loseConnection()
        self.assertEqual(self.factory.getClientNum(), 1)

        #tear down the second connection
        self.protocol_1.transport.loseConnection()
        self.assertEqual(self.factory.getClientNum(), 0)

class LiveProtocolTestCase(unittest.TestCase):
    """unit test for LiveProtocol"""
    
    def setUp(self):
        self.factory = LiveServer()
        self.transport = proto_helpers.StringTransportWithDisconnection()
        self.protocol = self.factory.buildProtocol(('127.0.0.1', 1557))
        self.transport.protocol = self.protocol
        self.protocol.makeConnection(self.transport)

        self.data = ('\x32\x31\x32\x30\x30\x00\x00\x00\x01\x67\x42\x00\x0c\xe9\x02\x83\xf2'
                     '\x00\x00\x00\x01\x68\xce\x01\x0f\x20\x00\x00\x00\x01\x65\xb8\x40\x57'
                     '\xbb\xef\x00')


    #def test_lineReveived(self):
    #    self.protocol.dataReceived(self.data)
    #    self.assertEqual(self.protocol.getSource().getID(), '21200')


    def tearDown(self):
        self.protocol.transport.loseConnection()
       

