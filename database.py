import time

class DataBase:
	'''Класс для взаимодествия с базой данных'''
	
	def __init__(self):
		# Список чатов
		#Структура: {
		#	отправитель:[получатель, получатель последним отправил сообщение]
		#}
		self.connects = {}
		# Список ожидающих
		self.waitings = []
		# Позиции в интерфейсе
		self.likes = {}
	
	def _check_waitings(self):
		if len(self.waitings) >= 2:
			self.connect(self.waitings[0],self.waitings[1])
			return True
		else:
			return False
	
	def connect(self,user1,user2):
		self.waitings.remove(user1)
		self.waitings.remove(user2)
		self.connects[user1] = [user2,True]
		self.connects[user2] = [user1,True]

	def like(self,giver_id,taker_id):
		self.disconnect(giver_id,taker_id)
		if self.likes.get(taker_id) == None:
			self.likes[taker_id] = 1
			return False
		else:
			self.likes[taker_id] += 1
			return True
	
	def disconnect(self,user1,user2):
		self.connects.pop(user1)
		self.connects.pop(user2)
	
	def add_waiting(self,user):
		self.waitings.append(user)
		return self._check_waitings()
