#!/usr/bin/python
#-*- coding=utf-8 -*-
##
# @file liveStreamServer.py
# @brief accpept live stream
# @author yy
# @version 0.1
# @date 2012-07-10

from twisted.internet import protocol, reactor
from twisted.protocols import basic
from twisted.protocols.policies import TimeoutMixin
from twisted.application import service,internet


from twisted.python import log
from sourceState import NoIDReceivedState, IDReceivedState

from multicastSource import MulticastSource

class LiveProtocol(basic.LineReceiver, TimeoutMixin):
    """accept live stream data and parse it"""
    delimiter = '\x00\x00\x00\x01'
    #TODO the default MAX_LENGTH is 16384, enough?

    def __init__(self):
        self._source = MulticastSource(self)
        self._state = NoIDReceivedState(self)
        
    def getSource(self):
        return self._source

    def setState(self, state):
        self._state = state

    def connectionMade(self):
        self.setTimeout(10)
        self.factory.addSource(self._source)
        print 'live stream connects from %s' % self.transport.getPeer()

    def lineReceived(self, line):
        #in case of "00 00 00 01 00 00 00 01"
        self.resetTimeout()
        if line:
            self._state.receiveLine(line)
        else:
            log.msg("receive an empty line")

    def timeoutConnection(self):
        log.err('client timeout')
        self.transport.loseConnection()

    def connectionLost(self, reason):
        self.setTimeout(None)
        print 'live stream connection lost from %s' % self.transport.getPeer()
        #set the config line "disable"
        self._source.disableStream()

        self.factory.removeSource(self._source)
        self.factory.connectionLost(reason)

    def lineLengthExceeded(self, line): 
        print "too long frame received"

class LiveServer(protocol.ServerFactory):
    """listen for live stream connection"""

    protocol = LiveProtocol
    
    def __init__(self):
        self._clientNum = 0
        self._sources = []

    def getClientNum(self):
        return self._clientNum


    def buildProtocol(self, addr):
        self._clientNum = self._clientNum + 1
        return protocol.ServerFactory.buildProtocol(self, addr)

    def addSource(self, source):
        self._sources.append(source)

    def removeSource(self, source):
        self._sources.remove(source)

    
    def connectionLost(self, reason):
        self._clientNum = self._clientNum - 1
        log.msg("live source connection lost because %s" %(reason))

def main():
    port = reactor.listenTCP(1557, LiveServer())
    print "live stream server starts at %s" %(port.getHost() )
    log.startLogging(open("log.txt",'w'),setStdout = False)
    reactor.run()

if __name__ == '__main__':
    main()
elif __name__=='__builtin__':
    reactor.callLater(1, main)
    application=service.Application('hello')
