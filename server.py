#!/usr/bin/env python

import sys
import uuid
from omniORB import CORBA
import chat, chat__POA
import CosNaming

class ChatServerImpl (chat__POA.ChatServer):
	def __init__(self):
		self.nicks = set()
		self.clients = {}

	def subscribe(self, nick, client):
		if nick in self.nicks:
			raise chat.NameAlreadyUsed()
		self.nicks.add(nick)
		id = str(uuid.uuid4())
		print 'subscribe:', nick, '->', id
		self.clients[id] = (nick, client)
		return id

	def unsubscribe(self, id):
		print 'unsubscribe:', id
		try:
			nick, c = self.clients[id]
		except:
			raise chat.UnknownID()
		self.nicks.remove(nick)
		del self.clients[id]

	def comment(self, id, text):
		try:
			nick, c = self.clients[id]
		except:
			raise chat.UnknownID()
		print 'comment:', text, 'by', id, '[%s]' % nick
		for i, (n, to) in self.clients.iteritems():
			to.update(nick, text)

# initializing ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# getting referenec to POA
poa = orb.resolve_initial_references('RootPOA')
# getting reference to POA manager
manager = poa._get_the_POAManager()
# activating manager
manager.activate()

# getting NameService
obj = orb.resolve_initial_references('NameService')
ncRef = obj._narrow(CosNaming.NamingContext)

# creating servant
cs = ChatServerImpl()
# connecting servant to ORB
chatserver = cs._this()
# binding servant reference to NameService
ncRef.rebind([CosNaming.NameComponent('chatserver_yzioaw', '')],
	chatserver)

print 'Object activated'
# starting orb
orb.run()
