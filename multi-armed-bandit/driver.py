import gym
import time
import math
import argparse
import numpy as np

class Node:
	def __init__(self, parent, action):
		self.parent = parent
		self.action = action
		self.children = []
		self.explored_children = 0
		self.visits = 0
		self.value = 0
	def add_child(self,child):
		child=Node(self, child.action)
		self.children.append(child)
	def update(self,reward):
		self.reward+=reward
		self.visits+=1
	def __repr__(self):
		s = "Node; children: %d; visits: %d; value: %f"%(len(self.children),self.visits,self.value)
		return s

def ubc(node):
	return self.value/self.vists + 1 * (math.log(node.parent.visits)/node.visits)**0.5

class SlotMachine:
	def __init__(self, probability):
		self.prob = probability
	def pull(self):
		if (np.random.randint(1, 100) <= 100 * self.prob):
			return 1
		return 0




def main(runs, slots):
	bob = SlotMachine(0.5)
	for i in range (0, 20):
		print(bob.pull())



	# for i_episode in range(20):
	#     observation = env.reset()
	#     for t in range(100):
	#         # env.render()
	#         # print(observation)
	#         print(env.action_space)

	#         action = env.action_space.sample()
	#         observation, reward, done, info = env.step(action)
	#         if done:
	#             print("Episode finished after {} timesteps".format(t+1))
	#             break




if __name__=="__main__":
	parser = argparse.ArgumentParser(description='MCTS')
	parser.add_argument('--runs', action="store", required=False, default = 100, type=int)
	parser.add_argument('--slots', action="store", required=False, default = 10, type=int)
	args=parser.parse_args()
	main(args.runs, args.slots)

