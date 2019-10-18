import numpy as np
import pandas as pd
from random import randint

def play_sim(games, my_choice, total_doors=3):

	total_doors = total_doors
	my_choice = my_choice
	games = games

	i = 0
	wins = 0
	losses = 0

	while i < games:
		game = Game(total_doors)
		game.make_choice(my_choice)
		game.montys_choice()
		game.game_strategy('switch')
		if game.win is True:
			wins += 1
		elif game.win is False:
			losses += 1

		i += 1

	print('You have', wins, 'wins')
	print('You have', losses, 'losses')
	print('This yields a win percentage of:', round((wins / games) * 100, 2), '%')


def _check_for_win(my_door):
	if my_door == 1:
		result = True
	elif my_door != 1:
		result = False
	else:
		ValueError('No proper value for our chosen door!')

	return result


def _create_prize_array(doors):
	prize_array = np.zeros(doors, dtype=int)
	random_door = randint(0, doors - 1)
	prize_array[random_door] = 1

	return prize_array


def _build_simulator(doors):
	door_array = np.arange(1, doors + 1, 1)
	prize_array = _create_prize_array(doors)
	game_df = pd.DataFrame(data=prize_array, columns=['Prize'], index=door_array)

	return game_df


class Game:

	def __init__(self, doors):
		try:
			int(doors)
			self.game_df = _build_simulator(doors)
			self.doors = doors
		except ValueError:
			print(doors, 'is not an integer! Please pass and int value.')

	def make_choice(self, chosen_door):
		self.my_door = self.game_df.iloc[[chosen_door - 1]]
		self.my_door = self.my_door['Prize'].iloc[0]
		self.game_df = self.game_df.drop([chosen_door])

	def montys_choice(self):
		if self.my_door == 1:
			if self.doors == 3:
				montys_door = randint(0, 1)
				self.montys_door = self.game_df.iloc[[montys_door]]
				self.montys_door = self.montys_door['Prize'].iloc[0]
			else:
				montys_door = randint(0, self.doors - 2)
				self.montys_door = self.game_df.iloc[[montys_door]]
				self.montys_door = self.montys_door['Prize'].iloc[0]
		else:
			self.montys_door = self.game_df.loc[self.game_df['Prize'] == 1]
			self.montys_door = self.montys_door['Prize'].iloc[0]


	def game_strategy(self, strat):
		if strat in ("Switch", "switch"):
			result = _check_for_win(self.montys_door)
		elif strat in ("stay", "Stay"):
			result = _check_for_win(self.my_door)
		else:
			raise ValueError("Please pass 'stay' or 'switch'")

		if result is True:
			self.win = True
		else:
			self.win = False
