import random
import numpy as np
from game import SpaceRocks
from collections import deque

MAX_MEMORY = 100_000

class Agent:
    def __init__(self):
        self.n_games = 0
        # self.epsilon = 0
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_short(self):
        pass

    def get_action(self):
        return "shooting", "accelerate"    

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SpaceRocks()
    while True:
        #get old state
        # state_old = agent.get_state(game)

        #get move
        ship_final_move, peach_final_move = agent.get_action()

        #perform move and get new state
        reward, done, score = game.play_step(ship_final_move, peach_final_move)
        # state_new = agent.get_state(game)

if __name__ == '__main__':
    train()