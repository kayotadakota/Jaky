class KeyBoard():
	'''Класс для работы генерации клавиатур'''
	
	def __init__(self):
		self.keys = [[]]
	
	def get_keyboard(self,one_time=False):
		return {
			"one_time": one_time,
			"buttons": self.keys
		}
	
	def get_button(self,text,typeof="text",color="positive",payload="{\"button\": \"1\"}"):
		return {
			"action":{
				"type":f"{typeof}",
				"label":f"{text}",
				"payload":f"{payload}",
			},
			"color":f"{color}",
		}
	
	def add_button(self,text,typeof="text",color="positive",payload="{\"button\": \"1\"}"):
		self.keys[len(self.keys)-1].append(self.get_button(typeof=typeof,text=text,color=color,payload=payload))
		return self
	
	def add_space(self):
		self.keys.append([])
		return self

# Клавиатуры

greet_keyboard 	= KeyBoard().add_button(
	typeof="text",
	text="Найти собеседника&#127744;",
	color="primary").add_space().add_button(
	typeof="text",
	text="Мой Профиль",
	color="positive"
).get_keyboard()

wait_keyboard 	= KeyBoard().add_button(
	typeof="text",
	text="Отменить поиск",
	color="negative"
).get_keyboard()

chat_keyboard 	= KeyBoard().add_button(
	typeof="text",
	text="Симпатия",
	color="positive").add_button(typeof="text",
	text="Выход",
	color="negative"
).get_keyboard()