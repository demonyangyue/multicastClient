#!/usr/bin/python
#-*- coding=utf-8 -*-

##
# @file sourceState.py
# @brief describe each state of the source
# @author yy
# @version 1.0
# @date 2013-03-02

class NoIDReceivedState(object):
    """hasn't reveived the ID string yet"""
    def __init__(self, proto):
       self._proto = proto 

    def receiveLine(self, ID):
        self._proto.getSource().configureSource(ID)
        self._proto.setState(IDReceivedState(self._proto))


class IDReceivedState(object):
    """has received the ID string"""
    def __init__(self, proto):
       self._proto = proto 

    def receiveLine(self, line):
        self._delimiter = '\x00\x00\x00\x01'
        line = "".join([self._delimiter, line])
        self._proto.getSource().update(line)

        


