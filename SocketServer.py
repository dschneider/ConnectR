#!/usr/bin/env python

# -*- coding: utf-8 -*-
# ConnectR v0.3
# 2008 Dennis Schneider
# Remember: The best things in life are free

import select
import socket
import sys
import time
import datetime
import thread
import string
from copy import copy

        
class socketClass:
	  active = 0

class Server:
    
    def __init__(self, host, port):
        """
          Initialize the attributes
        """
    
        self.host = host
        self.port = int(port)
        self.backlog = 5
        self.size = 1024
        self.connections = {}
        self.clients = {}
        self.nick_flag = 1
        self.socketArray = list()
        
        
    def listen(self):
        """
          Set the server to listen mode
        """
    
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)


    def handler(self, index, zero):
        """
          Handles new clients (called as a thread)
        """
        t = datetime.datetime.now()
        EpochSeconds = time.mktime(t.timetuple())
        now = datetime.datetime.fromtimestamp(EpochSeconds)
        self.send("*** SERVER *** " + str(self.socketArray[index].ADDR) + " connected @ " + now.ctime())
        
        while 1:
		      data = self.socketArray[index].socket.recv(1024)
		      if data == '/quit': break
		      self.send (str(self.socketArray[index].ADDR) + " : " + data)
        
        self.send("*** SERVER *** " + str(self.socketArray[index].ADDR) + " disconnected.")
        
        self.socketArray[index].active = 0
        self.socketArray[index].socket.close()
        return


    def close(self):
        """
          Close the server
        """
        
        self.serverSocket.close()
        

    def send(self, message):
        """
          Sends a message to all clients
        """
        
        print message
	
        for i in range(len(self.socketArray)):
          if self.socketArray[i].active:
            self.socketArray[i].socket.send(message)


    def accept_clients(self, none, noner):
        """
          Accepts new client connections and starts the handler method as a thread
        """
    
        while 1:
            #ADDR = ('', self.port)
            self.socketArray.append(socketClass())
            self.socketArray[len(self.socketArray) - 1].socket, self.socketArray[len(self.socketArray) - 1].ADDR = copy(self.serverSocket.accept())
            self.socketArray[len(self.socketArray) - 1].active = 1
            print self.socketArray[len(self.socketArray) - 1].socket, self.socketArray[len(self.socketArray) - 1].ADDR
            
            thread.start_new_thread(self.handler, ((len(self.socketArray) - 1),0))

        serverSocket.close()
        return
        
        
    def main(self):
        """
          Start the accept_clients method as a thread
        """
        
        thread.start_new_thread(self.accept_clients, (0, 0))
