import vk_api
import json
import time
from database import DataBase
import keys
from vk_api.longpoll import VkEventType
from vk_api.longpoll import VkLongPoll
from random import randint
from pprint import pprint

class Locator():
	def __init__(self,database,group,phrases):
		self.user_id = None
		self.user_message = None
		self.db = database
		self.grp = group
		self.admin_message = False
		self.phrases = phrases
	def router(self,user_id,message):
		self.user_id = user_id
		self.user_message = message
		if user_id in self.db.waitings:
			self.waiting_response()
		if user_id in self.db.connects:
			self.connect_messaging()
		else:
			self.lobby()
	def sender(self,user_id,message,keyboard):
		self.grp.messages.send(user_id=user_id,message=message,random_id=randint(1,2147483647),keyboard = json.dumps(keyboard,ensure_ascii=False))
	def connect_notify(self,users,message,keyboard):
		for user in users:
			self.sender(user,message,keyboard)
	def waiting_response(self):
		if self.user_message.lower().startswith('oтменить поиск'):	
			self.sender(self.user_id,self.phrases["waiting"]["stop"],keys.wait_keyboard)
		else:
			self.db.waitings.remove(self.user_id)
			self.sender(self.user_id,self.phrases["waiting"]["continue"],keys.greet_keyboard)
			self.admin_message = True
	def connect_messaging(self):
		if self.user_message.lower() != 'выход':
			if self.db.connects[self.user_id][1] != 1:
				self.db.connects[self.user_id][1] = 1
				self.db.connects[self.db.connects[self.user_id][0]][1] = 0
				GUEST = self.phrases["connect"]["prefix"]
			else:
				GUEST = ""
			self.sender(self.db.connects[self.user_id][0],GUEST+self.user_message,keys.chat_keyboard)
		else:
			self.connect_notify([self.user_id,self.db.connects[self.user_id][0]],self.phrases["connect"]["stop"],keys.greet_keyboard)
			self.admin_message = True
			self.db.disconnect(self.user_id,self.db.connects[self.user_id][0])
	def lobby(self):
		if self.user_message.lower().startswith('найти собеседника'):
			if self.db.add_waiting(self.user_id):
				self.connect_notify([self.user_id,self.db.connects[self.user_id][0]],"Собеседник найден!",keys.chat_keyboard)
			else:
				self.sender(self.user_id,self.phrases["waiting"]["search"],keys.wait_keyboard)
		else:
			if not self.admin_message: 
				# print( time.time() - self.grp.messages.getHistory(peer_id=self.user_id)["items"][1]["date"])
				# print( time.time() )
				# print( self.grp.messages.getHistory(peer_id=self.user_id)["items"][-1]["date"] )
				items = self.grp.messages.getHistory(peer_id=self.user_id)["items"]
				# print(items)
				# print(len(items))
				if len(items) == 1:
					message = self.phrases["greeting"]
					keyboard = keys.greet_keyboard
				elif time.time() - items[1]["date"] < 7200:
					message = self.phrases["lobby_phrases"][randint(0,len(self.phrases["lobby_phrases"])-1)]
					keyboard = keys.greet_keyboard
				else:
					message = self.phrases["greeting"]
					keyboard = keys.greet_keyboard
				group.messages.send(user_id=self.user_id,message=message,random_id=randint(1,2147483647),keyboard=json.dumps(keyboard,ensure_ascii=False))
			else:
				self.admin_message = False

if __name__ == "__main__":

	with open('data.json',encoding="utf-8") as data:
	    data = json.loads(data.read())

	group_token 	= data["personal"]["group_token"]
	group_obj 		= vk_api.VkApi(token=group_token)
	group 			= group_obj.get_api()
	group_longpoll 	= VkLongPoll(group_obj)
	
	locator 		= Locator(DataBase(),group,data["messages"])

	# while True:	
		# try:
	for event in group_longpoll.listen():

		if event.from_user and event.type == VkEventType.MESSAGE_NEW and not event.from_me:
			# print('\n')
			# pprint(event.__dict__)
			locator.router(event.peer_id,event.text)
			# print(data.waitings)
			# print(data.connects)
		# except:
		# 	continue