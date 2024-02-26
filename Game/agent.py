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
        P_s = (game.spaceship.position.x, game.spaceship.position.y)
        V_s = (game.spaceship.position.x, game.spaceship.position.y)
        P_p = (game.peach.position.x, game.peach.position.y)
        V_p = (game.peach.position.x, game.peach.position.y)
        bullet_V = []
        bullet_P  = []
        for i, B in enumerate(game.bullets):
            P_b = (B.position.x, B.position.y)
            V_b = (B.velocity.x, B.velocity.y)
            bullet_V.append(V_b)
            bullet_P.append(P_b)
        asteroid_P = []
        asteroid_V = []
        for i, A in  enumerate(game.asteroids):
            P_a = (A.position.x, A.position.y)
            V_a = (A.velocity.x, A.velocity.y)
            asteroid_P.append(P_a)
            asteroid_V.append(V_a)
            
        states = [P_s,V_s,P_p,V_p,bullet_P,bullet_V,asteroid_P,asteroid_V]
        return states

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_short(self):
        pass

    def get_action(self):
        return ["shooting",'stay','accelerate'], ["accelerate",'counterClockwise']    

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SpaceRocks(user_input=False)
    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        ship_final_move, peach_final_move = agent.get_action()

        #perform move and get new state
        # reward, done, score = game.play_step(ship_final_move, peach_final_move)
        game.play_step(ship_final_move, peach_final_move)
        state_new = agent.get_state(game)

if __name__ == '__main__':
    train()