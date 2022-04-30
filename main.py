from math import remainder
import time
import threading
import string
from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import platform

from kivy.animation import Animation
from kivymd.toast import toast

Builder.load_file('main.kv')
Builder.load_file('home.kv')
Builder.load_file('howto.kv')
Builder.load_file('gamekv.kv')

if platform == 'win':
	from kivy.core.window import Window
	Window.size = (500, 900)

class HomeScreen(MDScreen):
	pass

class HowtoScreen(MDScreen):
	pass

class GameScreen(MDScreen):

	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game_init()

	def game_init(self):
		Clock.schedule_once(self.update_stringboxes, 0.01)
		self.CHANCE = 6
		self.LENGTH = 5
		self.xindex = self.yindex = 0
		self.gameover = False
		self.app = MDApp.get_running_app()
		self.doanim = False

		# A list that stores the background color of characters, etc.
		self.pressed_strings = [['', self.app.blank_color] for i in range(self.CHANCE * self.LENGTH)]

		# A dictionary that stores keyboard colors
		self.keyboard_colors = {}
		for alpha in list(string.ascii_uppercase):
			self.keyboard_colors[alpha] = self.app.keyboard_default_color

		# Game class instantiation
		import game
		self.game = game.Game(self.CHANCE, self.LENGTH)
		print(self.game.get_word())
		# self.remaining = list(self.game.get_word())
  
	def animate(self, widget, *args):
		animate = Animation(opacity=0, duration=0)
		animate += Animation(
			angle = 360,
			opacity=1,
			duration=.3)
		animate.start(widget)
		
  
	def update_stringboxes(self, dt = None):
		self.ids.stringboxes.clear_widgets()
		self.ids.stringboxes.cols = self.LENGTH
		self.app = MDApp.get_running_app()
		rowpos = ((self.yindex )* 5)
		for i in range(self.CHANCE * self.LENGTH):
			box = StringBox(
				text = str(self.pressed_strings[i][0]),
				color = self.app.theme_cls.text_color if self.pressed_strings[i][1]==self.app.blank_color else (1, 1, 1, 1),
				background_color = self.pressed_strings[i][1]
			)
			self.ids.stringboxes.add_widget(box)
			# target row, but only doanim on one row using the bool when enter pressed
			if self.pressed_strings[i][1]!=self.app.blank_color:
				if i in range(rowpos-5,rowpos):
					if self.doanim == True:
						self.animate(box)
		self.doanim = False

	def update_keyboard(self):
		# with self.ids.board.canvas:
		# 	RoundedRectangle(radius=(20,))
		for key, value in self.keyboard_colors.items():
			self.ids[key].background_color = value

	def update(self):
		self.update_stringboxes()
		self.update_keyboard()

	def string_pressed(self, text):
		if self.xindex == self.LENGTH or self.gameover == True:
			return

		self.pressed_strings[self.LENGTH * self.yindex + self.xindex][0] = text
		self.xindex += 1
		self.update()

	def enter_pressed(self):
		if self.gameover == True:
			return
		if self.xindex == self.LENGTH:
			strings = [row[0] for row in self.pressed_strings[self.LENGTH * self.yindex:self.LENGTH * self.yindex + self.LENGTH]]
			remaining = list(self.game.get_word())
			if ''.join(strings) in self.game.get_words():
				# Character position check. count is number of correct positions
				count = index = 0

				for i in range(self.LENGTH * self.yindex, self.LENGTH * self.yindex + self.LENGTH):
					if strings[index] == list(self.game.get_word())[index]:
						# Both letters and positions are correct
						count += 1
						# Remember remainders for other scenarios on first
						for k in range(self.LENGTH):
							if strings[k] == remaining[k]:
								remaining[k] = ' '
								# print(remaining)

	
						self.pressed_strings[i][1] = self.app.correct_color
		
						self.keyboard_colors[strings[index]] = self.app.correct_color
					elif strings[index] in self.game.get_word():
						# The characters are correct but the position is incorrect
						# Check for repeats and default to miss
						self.pressed_strings[i][1] = self.app.miss_color
						for j in range(self.LENGTH):
							if strings[index] == remaining[j]:
								self.pressed_strings[i][1] = self.app.close_color
								remaining[j] = ' '
								# print(remaining)
   
		
						if strings[index] in remaining:
							self.pressed_strings[i][1] = self.app.close_color

		

		
						if self.keyboard_colors[strings[index]] != self.app.correct_color:
							self.keyboard_colors[strings[index]] = self.app.close_color
					else:
						# Both are incorrect
						self.pressed_strings[i][1] = self.app.miss_color
						if self.keyboard_colors[strings[index]] == self.app.keyboard_default_color:
							self.keyboard_colors[strings[index]] = self.app.miss_color
	

					index += 1

				if count == self.LENGTH:
					self.gameover = True
					self.ids.resultlabel.text = 'Well Done!'
					self.update()
					return

				self.xindex = 0
				self.yindex += 1
				self.doanim = True

				if self.yindex == self.CHANCE:
					self.ids.resultlabel.text = self.game.get_word()
					self.gameover = True

			else:
				messagethread = threading.Thread(target=self.flash_message, args=('Not a word in wordlist',))
				messagethread.start()

			self.update()

	def back_pressed(self):
		if self.xindex == 0 or self.gameover == True:
			return

		self.xindex -= 1
		self.pressed_strings[self.LENGTH * self.yindex + (self.xindex)][0] = ''
		self.update()

	def restart(self):
		self.game_init()
		self.ids.resultlabel.text = ''
		self.update()

	# TODO: Fix threading so that text can be resized
	def flash_message(self, text):
		self.ids.resultlabel.text = text
		time.sleep(2)
		self.ids.resultlabel.text = ''

class StringBox(Button):
	pass

class NavigationBar(MDBoxLayout):
	pass

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super(Manager, self).__init__(**kwargs)
		self.transition = NoTransition()
  
	def switch_highcontrast(self):
		# perform spaghetti code
		self.app = MDApp.get_running_app()
		if self.app.high_contrast:
			print("Change to not Highcontrast")
			self.show_toast("Changing to Default Contrast")
			for i in range(self.ids.gameclass.CHANCE * self.ids.gameclass.LENGTH):
				if self.ids.gameclass.pressed_strings[i][1] == self.app.correct_color:
					self.ids.gameclass.pressed_strings[i][1] = [0, .5, 0, 1]
				if self.ids.gameclass.pressed_strings[i][1] == self.app.close_color:
					self.ids.gameclass.pressed_strings[i][1] = [.8, .8, 0, 1]   
			for alpha in list(string.ascii_uppercase):
				if self.ids.gameclass.keyboard_colors[alpha] == self.app.correct_color:
					self.ids.gameclass.keyboard_colors[alpha] = [0, .5, 0, 1]     
				if self.ids.gameclass.keyboard_colors[alpha] == self.app.close_color:
					self.ids.gameclass.keyboard_colors[alpha] = [.8, .8, 0, 1]     
			self.app.correct_color = [0, .5, 0, 1]
			self.app.close_color   = [.8, .8, 0, 1]
			self.app.high_contrast = False
		else:
			print("Change to Highcontrast")
			self.show_toast("Changing to High Contrast")   
			for i in range(self.ids.gameclass.CHANCE * self.ids.gameclass.LENGTH):
				if self.ids.gameclass.pressed_strings[i][1] == self.app.correct_color:
					self.ids.gameclass.pressed_strings[i][1] = [0, 0, 1, 1]
				if self.ids.gameclass.pressed_strings[i][1] == self.app.close_color:
					self.ids.gameclass.pressed_strings[i][1] = [1, 0, 0, 1]
			for alpha in list(string.ascii_uppercase):
				if self.ids.gameclass.keyboard_colors[alpha] == self.app.correct_color:
					self.ids.gameclass.keyboard_colors[alpha] = [0, 0, 1, 1]
				if self.ids.gameclass.keyboard_colors[alpha] == self.app.close_color:
					self.ids.gameclass.keyboard_colors[alpha] = [1, 0, 0, 1]

			self.app.correct_color = [0, 0, 1, 1]
			self.app.close_color   = [1, 0, 0, 1]
			self.app.high_contrast = True
		# Finally update the screen
		self.ids.gameclass.update()

	def switch_themetoggle(self):
		self.app = MDApp.get_running_app()
		self.show_toast("Switching theme")
		if self.app.theme_cls.theme_style == "Dark":
			self.app.theme_cls.theme_style = "Light"
		else:
			self.app.theme_cls.theme_style = "Dark"
		# Experiment with manager class
		#self.manager.testing()
		# Access Game Class via id to update the theme colors on stringboxes/ guessletters
		self.ids.gameclass.update_stringboxes()

	def show_toast(self, msg):
		'''Displays a toast on the screen.'''
		toast(msg,duration=1.5)  

class GameApp(MDApp):
	navigation_active_color = ListProperty([0, 1, 0, 1])
	correct_color = ListProperty([0, .5, 0, 1])
	close_color = ListProperty([.8, .8, 0, 1])
	miss_color = ListProperty([.5, .5, .5, 1])
	keyboard_default_color = ListProperty([.8, .8, .8, .8])
	blank_color = ListProperty([0, 0, 0, 0])
	high_contrast = False
	def __init__(self, **kwargs):
		super(GameApp, self).__init__(**kwargs)
		self.title = 'Wordle'
		# windows icon
		self.icon = 'res/images/icon.png'
 
	def build(self):
		# self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Green"
		self.theme_cls.accent_palette = "Green"
		# main.kv load
		return NavigationBar()

if __name__ == '__main__':
	GameApp().run()