import random

class Game():
	
	def __init__(self, chance, length):
		self.chance = chance
		self.length = length
		self.words = []

		with open('./glove_five_letter_common-5000.txt') as f:
			for line in f:
				self.words.append(line.strip().upper())

		# Randomly decide this word
		random.shuffle(self.words)
		self.word = self.words[0]
        
	def get_words(self):
		return self.words

	def contain_word_in_words(self, text):
		if text in self.words:
			return True

		return False

	def get_word(self):
		return self.word