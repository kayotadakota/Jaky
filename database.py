import time

class DataBase:
	def __init__(self):
		self.greets = {}
		self.connects = {}
		self.waitings = []
	def _check_waitings(self):
		self.connect(self.waitings[0],self.waitings[1])
	def connect(self,user1,user2):
		self.waitings.remove(user1)
		self.waitings.remove(user2)
		self.connects[user1] = [user2,0]
		self.connects[user2] = [user1,0]
	def disconnect(self,user1,user2):
		self.connects.pop(user1)
		self.connects.pop(user2)
	def add_waiting(self,user):
		self.waitings.append(user)
		if len(self.waitings) >= 2:
			self._check_waitings()
			return True
		else:
			return False
