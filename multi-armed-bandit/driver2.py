# import gym
# import time
import math
import argparse
import numpy as np
import random


class Node:
	def __init__(self, state):
		self.parent = None
		#tuple, first element is slot machine being pulled, 
		#second element is number of pulls we are at.
		self.state = state
		self.children = []
		#number of times we have completed a playthrough that passed through this state, or number of leaves.
		self.visits = 0
		#value of state, or our current score (how many of our playthroughs have won).
		self.value = 0;

	def machine(self):
		return self.state[0]

	def numpulls(self):
		return self.state[1]

	def numchildren(self):
		return len(self.children)

	def add_child(self, node):
		self.children.append(node)
		node.parent = self

	def add_play(self, win):
		self.visits += 1
		if win:
			self.value += 1

	#game ends when you reach the number of total pulls you can have is the number of pulls allowed.
	def terminal(self):
		return self.numpulls() == MAX_PULLS

	#return value of node, which is the slot machine pulled added onto value of parent.
	#changes every time here, which is not supposed to happen. But we can't help it because this is 
	#not a deterministic game. Our value func/MCTS would probably be better if it was a game of go.
	def value(self):
		val = machines[self.machine()].pull()
		if (not self.parent == None):
			val += Node.value(self.parent)
			# val += self.parent.value()
		return val

	def __repr__(self):
		s = "Node. On our %dth pull on machine #%d. Value of node : %d"%(self.state[1], self.state[0], self.value)
		return s


def ubc(node):
	return node.value / node.visits + (2 * math.log(node.parent.visits) / node.visits) ** 0.5

def simulate(node):
	totpulls = node.numpulls()
	score = Node.value(node.parent)
	# score = node.parent.value()
	score += machines[node.machine()].pull()
	#score of all the next random olls until TERMINAL condition needs to be added on
	for _ in range(MAX_PULLS - totpulls - 1):
		score += random.choice(machines).pull()
	return score

def playout(state, value):
	_, pulls = state
	value += machines[state[0]].pull()
	for i in range(MAX_PULLS - pulls - 1):
		value += machines[np.random.randint(0, SLOTS)].pull()
	return value

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
parser.add_argument('--win', action="store", required=False, default = 0.5, type=int)

if __name__=="__main__":
	args=parser.parse_args()
	CYCLES = args.cycles
	MAX_PULLS = args.pulls
	SLOTS = args.slots
	THRESHOLD = int(MAX_PULLS * args.win)

	machines = []
	# populate the machines array with slots
	for _ in range (0, SLOTS):
		machines.append(SlotMachine(np.random.uniform(0,1)))
	# machines = [SlotMachine(0.5) for _ in range(2)]
	# machines += [SlotMachine(1) for _ in range(1)] # sure win
	# machines += [SlotMachine(0.1) for _ in range(2)]
	# SLOTS = 5

	probs = [x.prob for x in machines]
	print(list(enumerate(probs)))

	#construct root node
	root = Node((0, 0))

	for _ in range (0, CYCLES):
		current = root
		#selection

		#selection goes on until there is a state without all possible actions branching from it
		while len(current.children) == SLOTS and not current.terminal():
			# for x in current.children:
			# 	print(x.visits)
			ubcs = [ubc(x) for x in current.children]
			current = current.children[np.argmax(ubcs)]

		if not current.terminal():
			#expansion
			machinesleft = [x for x in range(0, SLOTS)]
			for x in current.children:
				machinesleft.remove(x.machine())
			topull = random.choice(machinesleft)
			newnode = Node((topull, current.numpulls() + 1))
			current.add_child(newnode)

			#simulation
			score = simulate(newnode)
			win = False;
			if (score > THRESHOLD):
				win = True

			#backprop
			current = newnode
			while current != None:
				current.add_play(win)
				current = current.parent

	#done constructing MCTS tree.


	#Random Results
	tests = 1000
	random = 0
	mcts = 0

	for _ in range(0, tests):
		randresult = 0;
		for _ in range (0, MAX_PULLS):
			randresult += machines[np.random.randint(0, SLOTS)].pull()
		if (randresult > THRESHOLD):
			random += 1

	random = random / tests
	print("Random Result: " + str(random))

	#MCTS results.
	for _ in range(0, tests):
		current = root
		while len(current.children) == len(machines) and not current.terminal():
			ubcs = [ubc(x) for x in current.children]
			current = current.children[np.argmax(ubcs)]
		if current.terminal():
			toadd = Node.value(current)
			# toadd = current.value()
		else:
			toadd = playout((np.random.randint(0, SLOTS), current.numpulls() + 1), Node.value(current))
		# print(toadd)
		if toadd > THRESHOLD:
			mcts += 1
	mcts = mcts / tests
	print("MCTS result:" + str(mcts))



