import random
import numpy as np
from game import SpaceRocks
from collections import deque

MAX_MEMORY = 100_000

def angleMag(vec):
    magnitude = np.linalg.norm(vec)
    direction = np.arctan2(vec[1], vec[0])
    return np.array( [direction, magnitude] )

class Agent:
    def __init__(self):
        self.n_games = 0
        # self.epsilon = 0
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        R = {}
        position_s = np.array((game.spaceship.position.x, game.spaceship.position.y))
        velocity_s = np.array((game.spaceship.position.x, game.spaceship.position.y))
        position_p = np.array((game.peach.position.x, game.peach.position.y))
        velocity_p = np.array((game.peach.position.x, game.peach.position.y))
        position_t = np.array((game.target.position.x, game.target.position.y))

        bullet_V =[0]*len(game.bullets)
        bullet_P  = [0]*len(game.bullets)
        for i, B in enumerate(game.bullets):
            bullet_P[i] = np.array((B.position.x, B.position.y))
            bullet_V[i] = np.array((B.velocity.x, B.velocity.y))

        asteroid_V = [0]*(len(game.asteroids))
        asteroid_P  = [0]*(len(game.asteroids))
        for i, A in  enumerate(game.asteroids):
            asteroid_P[i] = np.array((A.position.x, A.position.y))
            asteroid_V[i] = np.array((A.velocity.x, A.velocity.y))

        R['Peach relative to ship'] = angleMag(position_p - position_s)
        R['Ship relative to peach'] = angleMag(position_s - position_p)
        R['Asteroids relative to peach'] = [angleMag(asteroid_P[j]-position_p) for j in range(len(asteroid_P))]
        R['Bullets relative to peach'] = [angleMag(bullet_P[j]-position_p) for j in range(len(bullet_P))]
        R["Target relative to peach"] = angleMag(position_t-position_p)
        R['Asteroids relative to ship'] = [angleMag(asteroid_P[j]-position_s) for j in range(len(asteroid_P))]
        R['Bullets relative to ship'] = [angleMag(bullet_P[j]-position_s) for j in range(len(bullet_P))]

        states = [position_s,velocity_s,position_p,velocity_p,bullet_P,bullet_V,asteroid_P,asteroid_V]
        return R

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_short(self):
        pass

    def get_action(self):
        #define membership functions for peach obstacles
        #probably plan on having 2 input (distance/direction)
        #How to deal with target?


        #define output membership functions
        #2 outputs probably (rotation/velocity)


        #define rules


        #define inference system


        #Defuzzification step
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
        shiposition_final_move, peach_final_move = agent.get_action()

        #perform move and get new state
        # reward, done, score = game.play_step(shiposition_final_move, peach_final_move)
        game.play_step(shiposition_final_move, peach_final_move)
        state_new = agent.get_state(game)

if __name__ == '__main__':
    train()