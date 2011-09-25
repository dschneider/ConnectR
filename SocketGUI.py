#!/usr/bin/env python

# -*- coding: utf-8 -*-
# ConnectR v0.3
# 2008 Dennis Schneider
# Remember: The best things in life are free

import socket
import sys
import thread
from Tkinter import *
from ScrolledText import *
import tkMessageBox
import tkSimpleDialog  
from SocketClient import Client
from SocketServer import Server

PROGRAM_NAME = "ConnectR"
VERSION = "0.3"
AUTHOR = "Dennis Schneider"
WEBSITE = "dev.banggang-six.de"

class SocketGUI:

    def __init__(self):      
        """ 
          Sets up the tkinter window and some attributes.
        """        
        
        # Initialize Attributes    
        self.port = 80
        self.address = '127.0.0.1'
        self.connected = False   
        self.acting_as_server = False
        self.acting_as_client = True    
        
        # Create Tkinter root window and set title
        self.root = Tk() 
        self.root.title(PROGRAM_NAME + " " + VERSION)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Create frame
        self.fpopup = Frame(self.root, width = 500) 
        self.fpopup.pack(expand = 1, fill = BOTH) 

        # Create the menus
        self.menuobj = Menu(self.root)
        self.root.config(menu=self.menuobj)
        self.filemenu=Menu(self.menuobj, tearoff = 0)
        self.menuobj.add_cascade(label = 'File', menu = self.filemenu)
        self.filemenu.add_command(label = 'Start Server', command = self.setup_server)
        self.filemenu.add_command(label = 'Stop Server', command = self.setup_server)
        self.filemenu.add_command(label = 'Connect', command = self.connect)
        self.filemenu.add_command(label = 'Disconnect', command = self.disconnect)
        self.filemenu.add_command(label = 'Exit', command = self.close) 
        self.editmenu=Menu(self.menuobj, tearoff = 0)
        self.menuobj.add_cascade(label = "Edit", menu = self.editmenu)
        self.editmenu.add_command(label = 'Configuration', command = self.configuration)
        self.helpmenu=Menu(self.menuobj, tearoff = 0)
        self.menuobj.add_cascade(label = 'Help', menu = self.helpmenu)
        self.helpmenu.add_command(label = 'About', command = self.about)  

        # Create the message window
        self.message_window = ScrolledText(self.fpopup, width = 90, height = 24, background = 'white')
        self.message_window.pack(fill = BOTH, expand = YES)

        # Create the entry field
        self.entry_field = Entry(self.fpopup, width = 60, background = 'white')
        self.entry_field.pack(side = LEFT, fill = BOTH, expand = YES)
                
        # Bindings
        self.entry_field.bind('<Return>', self.sendmessage_event)  
        self.entry_field.bind('<Control-n>', self.connect_event)
        self.message_window.bind('<Control-n>', self.connect_event)      
                
        # Create Buttons    
        self.send_button = Button(self.fpopup, text = 'Send', command = self.sendmessage)
        self.send_button.pack(side = LEFT, expand = NO)
         
        # Start the Tk main routine
        self.root.mainloop() 
    
    
    def configuration(self):
        """
          Sets up the configuration menu
        """        
        
        self.configuration_menu = Toplevel() 
        self.configuration_menu.title(PROGRAM_NAME + " - Configuration")
        
        self.port_label = Label(self.configuration_menu, text="Port:", width=40, anchor=W)
        self.port_entry_field = Entry(self.configuration_menu, width = 40, background = 'white')
        self.address_label = Label(self.configuration_menu, text="Address:", width=40, anchor=W)
        self.address_entry_field = Entry(self.configuration_menu, width = 40, background = 'white')
        self.save_configuration_button = Button(self.configuration_menu, text = 'Save', command = self.save_configuration)
        self.cancel_configuration_button = Button(self.configuration_menu, text = 'Cancel', command = self.cancel_configuration)
     
        self.port_entry_field.insert(END, str(self.port))
        self.address_entry_field.insert(END, self.address)
     
        self.port_label.grid(row = 0, columnspan = 2, sticky = W)
        self.port_entry_field.grid(row = 1, columnspan = 2, sticky = W, pady=5)
        self.address_label.grid(row = 2, columnspan = 2, sticky = W)
        self.address_entry_field.grid(row = 3, columnspan = 2, sticky = W, pady=5)
        self.save_configuration_button.grid(row = 5, columnspan = 2)
        self.cancel_configuration_button.grid(row = 5, column = 1, columnspan = 2)
    
    
    def cancel_configuration(self):
        """
          Destroys the configuration menu
        """
        
        self.configuration_menu.destroy()
        
        
    def cancel_server(self):
        """
          Destroys the server setup menu
        """
        
        self.server_menu.destroy()
        
        
    def save_configuration(self):
        """
          Saves the configuration values and closes the window
        """
        
        self.port = int(self.port_entry_field.get())
        self.address = self.address_entry_field.get()
        self.configuration_menu.destroy()
           
           
    def about(self):  
        """
          Calls the about window
        """
        
        tkMessageBox.showinfo('About', PROGRAM_NAME + ' ' + VERSION + '\n' + AUTHOR + '\n' + WEBSITE)
       
       
    def close(self):
        """
          Closes the whole application window
        """
        
        # Close the application
        if self.connected == True:
            self.clientSocket.sendmessage('/quit')
        if self.acting_as_server:
            self.serverSocket.close()
        self.root.destroy()
       
       
    def receiver(self, clientSocket, ADDR):
        """
          Receives the messages (called as a thread)
        """
        
        while 1:
            if self.connected == True:
                data = clientSocket.recv(1024)
                self.message_window.insert(END, '\n' + data)
                self.message_window.see(END)
                if data == "/quit": 
                    self.connected = False
                    return 0


    def setup_server(self):
        """
          Calls the server setup menu
        """
        
        self.server_menu = Toplevel() 
        self.server_menu.title(PROGRAM_NAME + " - Setup Server")
        
        self.server_port_label = Label(self.server_menu, text="Port:", width=40, anchor=W)
        self.server_port_entry_field = Entry(self.server_menu, width = 40, background = 'white')
        self.server_address_label = Label(self.server_menu, text="Address:", width=40, anchor=W)
        self.server_address_entry_field = Entry(self.server_menu, width = 40, background = 'white')
        self.start_server_button = Button(self.server_menu, text = 'Start', command = self.start_server)
        self.server_cancel_configuration_button = Button(self.server_menu, text = 'Cancel', command = self.cancel_server)
     
        self.server_port_label.grid(row = 0, columnspan = 2, sticky = W)
        self.server_port_entry_field.grid(row = 1, columnspan = 2, sticky = W, pady=5)
        self.server_address_label.grid(row = 2, columnspan = 2, sticky = W)
        self.server_address_entry_field.grid(row = 3, columnspan = 2, sticky = W, pady=5)
        self.start_server_button.grid(row = 5, columnspan = 2)
        self.server_cancel_configuration_button.grid(row = 5, column = 1, columnspan = 2)


    def start_server(self):
        """
          Creates a server
        """
        
        try:
            self.serverSocket = Server(self.server_address_entry_field.get(), self.server_port_entry_field.get())
            self.serverSocket.listen()
            self.serverSocket.main()
            self.message_window.insert(END, '\n' + "*** ACTING AS A SERVER: LISTENING ON PORT " + self.server_port_entry_field.get() + " ON ADDRESS " + self.server_address_entry_field.get() + " ***")
        except:
            pass
            
        self.cancel_server()
        self.acting_as_server = True
        

    def connect(self):
        """
          Connects the client to the given address and port
        """
        
        self.clientSocket = Client(self.address, self.port)
        try:
            if not self.connected:
                self.clientSocket.connect()
                self.connected = True  
                thread.start_new_thread(self.receiver, (self.clientSocket.clientSocket, (self.address, self.port)))                 
            else:
                self.message_window.insert(END, '\n' + "Already connected!")
                self.message_window.see(END)
        except socket.error, (errno, errmessage):
            self.message_window.insert(END, '\n' + "**** ERROR No." + str(errno) + " --> " + str(errmessage) + " **** ")
            if errno == 111:
                self.message_window.insert(END, '\n' + "Maybe you typed a false PORT or ADDRESS or the server has not been set up yet")
            self.message_window.see(END)
    
    
    def connect_event(self, event):
        """ 
          Used for the connect event (set event to NONE and setup general function!!)
        """
        
        self.connect()
        
        
    def sendmessage_event(self, event):
        """
          Used for the sendmessage event (set event to NONE and setup general function!!)
        """
        
        if self.connected:
            self.sendmessage()


    def disconnect(self):
        """
          Disconnects the client
        """
        
        self.clientSocket.sendmessage('/quit')
        self.connected = False
        self.clientSocket.close()


    def sendmessage(self):
        """
          Send a message
        """
        
        if self.connected:
            data = self.entry_field.get()
            self.entry_field.delete('0', END)
            if data == "/quit":
                self.clientSocket.sendmessage(data)
                self.clientSocket.close_connection()  
                self.connected = False 
            else:
                self.clientSocket.sendmessage(data)  
            self.entry_field.focus_set() 

# Start the program
socketgui = SocketGUI()
