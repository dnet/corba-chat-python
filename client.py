#!/usr/bin/env python

import sys
import uuid
from omniORB import CORBA
import chat, chat__POA
import CosNaming
from threading import Thread

class ChatClientImpl (chat__POA.ChatClient):
	def update(self, nick, text):
		print '<%s> %s' % (nick, text)

class ORBThread (Thread):
	def run(self):
		# getting reference to POA
		poa = orb.resolve_initial_references('RootPOA')
		# getting reference to POA manager
		manager = poa._get_the_POAManager()
		# activating manager
		manager.activate()
		# starting orb
		orb.run()

# initializing ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# getting NameService
obj = orb.resolve_initial_references('NameService')
ncRef = obj._narrow(CosNaming.NamingContext)

# resolving servant name
obj = ncRef.resolve([CosNaming.NameComponent('chatserver_yzioaw', '')])
chatserver = obj._narrow(chat.ChatServer)

# creating servant
cc = ChatClientImpl()
# connecting servant to ORB
chatclient = cc._this()
t = ORBThread()

id = chatserver.subscribe('test.py', chatclient)

try:
	print 'Connected with ID', id
	print 'Type /quit to exit'
	t.start()
	while True:
		s = sys.stdin.readline().rstrip() # \n
		if s == '/quit':
			break
		chatserver.comment(id, s)
finally:
	print 'Unsubscribing...',
	chatserver.unsubscribe(id)
	print ' done'
	orb.destroy()
	t.join()
