#!/usr/bin/env python

# -*- coding: utf-8 -*-
# ConnectR v0.3
# 2008 Dennis Schneider
# Remember: The best things in life are free

import select
import socket
import sys
import threading
import thread
import string


class Client:
    
    def __init__(self, host, port):
        """
          Initialize the attributes
        """
        self.host = host
        self.port = port
        self.clientSocket = None
        
    def vSendMessage(self, msg):
        """
          Send a message
        """
        self.clientSocket.send(msg)
        
    def vCloseConnection(self):
        """
          Close the connection
        """
        self.clientSocket.close()
        
    def vConnect(self):
        """
          Setup a connection
        """
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
