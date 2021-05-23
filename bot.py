import vk_api
import json
import time

from vk_api.longpoll 	import VkEventType
from vk_api.longpoll 	import VkLongPoll
from random 			import randint
from pprint	 			import pprint

#Свои модули
import keys
from database import DataBase

class Responser():

	'''Класс для распознования сообщения'''

	def __init__(self,database,group,phrases):
		self.user_id 		= None
		self.user_message 	= None
		self.admin_message 	= False
		self.db 			= database
		self.grp 			= group
		self.phrases 		= phrases
	
	def router(self,user_id,message):
		self.user_id 		= user_id
		self.user_message 	= message
		if user_id in self.db.waitings:
			self.waiting_response()
		elif user_id in self.db.connects:
			self.connect_messaging()
		else:
			self.lobby()
	
	def profile_render(self,user_id):
		return f"&#128150; ~ {self.db.likes[user_id]}"

	def sender(self,user_id,message,keyboard):
		self.grp.messages.send(
			user_id=user_id,
			message=message,
			random_id=randint(1,2147483647),
			keyboard = json.dumps(
				keyboard,
				ensure_ascii=False
			)
		)
	
	def connect_notify(self,users,message,keyboard):
		for user in users:
			self.sender(user,message,keyboard)
	
	def waiting_response(self):
		if self.user_message.lower() == "отменить поиск":	
			self.db.waitings.remove(self.user_id)
			self.sender(self.user_id,self.phrases["waiting"]["stop"],keys.greet_keyboard)
		else:
			self.sender(self.user_id,self.phrases["waiting"]["continue"],keys.wait_keyboard)
	
	def connect_messaging(self):
		peer_con = self.db.connects[self.user_id]
		if self.user_message.lower() == 'выход':
			self.db.disconnect(self.user_id,peer_con[0])
			self.connect_notify([self.user_id,peer_con[0]],self.phrases["connect"]["stop"],keys.greet_keyboard)
		elif self.user_message.lower() == 'симпатия':
			self.sender(peer_con[0],self.phrases["connect"]["taking_like"],keys.greet_keyboard)
			self.connect_notify([self.user_id,peer_con[0]],self.phrases["connect"]["stop"],keys.greet_keyboard)
			if not self.db.like(self.user_id,peer_con[0]):
				self.sender(peer_con[0],self.phrases["connect"]["first_like"],keys.greet_keyboard)
		else:
			if peer_con[1] == True:
				peer_con[1] = False
				self.db.connects[peer_con[0]][1] 	= True
				GUEST = self.phrases["connect"]["prefix"]
			else:
				GUEST = "" 
			self.sender(peer_con[0],GUEST+self.user_message,keys.chat_keyboard)
	
	def lobby(self):
		print(self.user_message.lower())
		if self.user_message.lower().startswith('найти собеседника'):
			self.sender(self.user_id,self.phrases["waiting"]["search"],keys.wait_keyboard)
			if self.db.add_waiting(self.user_id):
				self.connect_notify([self.user_id,self.db.connects[self.user_id][0]],self.phrases["connect"]["start"],keys.chat_keyboard)
		elif self.user_message.lower() == 'мой профиль':
			if self.db.likes.get(self.user_id) == None:
				self.sender(self.user_id,self.phrases["empty_user"],keys.greet_keyboard)
			else:	
				self.sender(self.user_id,self.profile_render(self.user_id),keys.greet_keyboard)
		else:
			items = self.grp.messages.getHistory(peer_id=self.user_id)["items"]
			if len(items) == 1:
				message = self.phrases["greeting"]
			elif time.time() - items[1]["date"] < 7200:
				message = self.phrases["lobby_phrases"][randint(0,len(self.phrases["lobby_phrases"])-1)]
			else:
				message = self.phrases["greeting"]
			self.sender(self.user_id,message,keys.greet_keyboard)

if __name__ == "__main__":

	with open('data.json',encoding="utf-8") as data:
	    data = json.loads(data.read())
	with open('personal.json',encoding="utf-8") as personal:
	    personal = json.loads(personal.read())

	group_token 	= personal["group_token"]
	group_obj 		= vk_api.VkApi(token=group_token)
	group 			= group_obj.get_api()
	group_longpoll 	= VkLongPoll(group_obj)
	
	response 		= Responser(DataBase(),group,data["messages"])

	for event in group_longpoll.listen():


		if event.from_user and event.type == VkEventType.MESSAGE_NEW and not event.from_me:
			print("Начало итерации")
			response.router(event.peer_id,event.text)
			print(response.db.connects)
			print(response.db.waitings)