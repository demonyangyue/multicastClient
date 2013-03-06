#!/usr/bin/python
#-*- coding=utf-8 -*-

##
# @file multicastSource.py
# @brief receive live stream data and send to the multicastServer
# @author yy
# @version 1.0
# @date 2013-03-02

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log
import fileinput

class MulticastSource(object):
    """initialize the source with the ID and configure the video.conf file"""

    conf_file_path = "video.conf"

    def __init__(self, proto):
        self._proto = proto
        self._ID = ''
        self._configureLine = ''
        self._sender = ''
        
    def configureSource(self, ID):
        self._ID = ID
        with open(self.conf_file_path, 'r') as f:
            for eachLine in f:
                if ID in eachLine and eachLine.startswith("VIDEO"):
                    self._configureLine = eachLine
        if not self._configureLine:
            log.err("wrong ID number")
            self._proto.loseConnection()
        else:
            self._destIP , self._destPort = self.getDestIPAndPort()
            self.enableStream()
            self._sender = MulticastSender(self._destIP, self._destPort)
            reactor.listenMulticast(self._destPort, self._sender, listenMultiple = True)
                
    def getDestIPAndPort(self):
        """return the IP address and portof the muticast server"""
        if not self._configureLine:
            log.err("no matched line found")
        else:
            items = self._configureLine.split(':')
            IP = items[8].split('/')[1]
            port = int(items[9])
            return (IP, port)
    
    def enableStream(self):
        """set the stream state enable"""
        for line in fileinput.input(self.conf_file_path, inplace = 1):
            if self._ID in line:
                if line.split(':')[4] == 'disable':
                    line = line.replace('disable', 'enable',1)
                elif line.split(':')[4] == 'enable':
                    #we already have a souce with the same ID, so tear down the connection .
                    self._proto.loseConnection()
                    log.msg("two sources have the same ID")
            print line,


    def disableStream(self):
        for line in fileinput.input(self.conf_file_path, inplace = 1):
            if self._ID in line and line.split(':')[4] == 'enable':
                line = line.replace('enable', 'disable',1)
            print line,

    def update(self, data):
        """send the data to the destination"""
        self._sender.send(data)
        

class MulticastSender(DatagramProtocol):
    """send the live stream data to the multicast server"""
    def __init__(self, IP, Port):
        self._destIP = IP 
        self._destPort = Port

    def startProtocol(self):
        self.transport.joinGroup(self._destIP)

    def send(self, data):
        self.transport.write(data,(self._destIP, self._destPort))

def test():
    ID = "21200"
    source = MulticastSource()
    source.configureSource(ID)
    print source.getDestIPAndPort()
    source.disableStream()

if __name__ == '__main__':
    test()


        
