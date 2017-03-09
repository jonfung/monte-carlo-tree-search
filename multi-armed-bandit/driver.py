# import gym
# import time
# import math
import argparse
import numpy as np
import random


class Node:
	def __init__(self, state, parent = None):
		self.parent = parent
		#tuple, first element is slot machine being pulled, 
		#second element is number of pulls we are at.
		self.state = state
		self.children = []
		#number of times we have completed a playthrough that passed through this state, or number of leaves.
		self.visits = 0
		#value of state, or our current score (how many of our playthroughs have won).
		self.value = 0;

	def machine(self):
		return state[0]

	def numpulls(self):
		return state[1]

	def add_child(self, node):
		self.children.append(child)
		node.parent = self

	#game ends when you reach the number of total pulls you can have is the number of pulls allowed.
	def terminal(self):
		return self.numpulls() == MAX_PULLS

	#return value of node, which is the slot machine pulled added onto value of parent.
	#changes every time here, which is not supposed to happen. But we can't help it because this is 
	#not a deterministic game. Our value func/MCTS would probably be better if it was a game of go.
	def value(self):
		val = machines[self.machine()]
		if (not self.parent == None):
			val += self.parent.value()
			return val

	def __repr__(self):
		s = "Node. On our %dth pull on machine #%d. Value of node : %d"%(self.state[1], self.state[0], self.value)
		return s


def ubc(node):
	return node.value / node.vists + (2 * math.log(node.parent.visits) / node.visits) ** 0.5

class SlotMachine:
	def __init__(self, probability):
		self.prob = probability
	def pull(self):
		if (np.random.randint(1, 100) <= 100 * self.prob):
			return 1
		return 0


parser = argparse.ArgumentParser(description='MCTS')
parser.add_argument('--cycles', action="store", required=False, default = 10000, type=int)
parser.add_argument('--pulls', action="store", required=False, default = 20, type=int)
parser.add_argument('--slots', action="store", required=False, default = 10, type=int)
parser.add_argument('--win', action="store", required=False, default = 0.8, type=int)

if __name__=="__main__":
	args=parser.parse_args()
	CYCLES = args.cycles
	MAX_PULLS = args.pulls
	SLOTS = args.slots
	THRESHOLD = MAX_PULLS * args.win

	machines = []
	# populate the machines array with slots
	for _ in range (0, SLOTS):
		machines.append(SlotMachine(np.random.uniform(0,1)))
	# machines = [SlotMachine(0.5) for _ in range(2)]
	# machines += [SlotMachine(1) for _ in range(1)] # sure win
	# machines += [SlotMachine(0.1) for _ in range(2)]

	probs = [x.prob for x in machines]
	print(list(enumerate(probs)))


	root = Node((0, 0))

	for _ in range (0, CYCLES):
		current = root
		#selection









	randresult = 0;
	for _ in range (0, MAX_PULLS):
		randresult += machines[np.random.randint(0, SLOTS)].pull()
	print("Random Result: " + str(randresult))
