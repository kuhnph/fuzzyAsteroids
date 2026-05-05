import random
import numpy as np
import math
from numpy.linalg import norm
from _DUMP.game import SpaceRocks
import random
from collections import deque
from _DUMP.philFunctions import triangular, left_shoulder, right_shoulder, sum_list_of_lists
import array
import random
from deap import algorithms, base, creator, tools
import time

#TODO
'''
Create cost function

'''


MAX_MEMORY = 100_000

# Add this function to write data to a file
def write_generation_cost(generation, best_cost, filename='generation_cost.txt'):
    with open(filename, 'a') as file:
        file.write(f'{generation},{best_cost}\n')

def map_value(value, from_low, from_high, to_low, to_high):
    # First, normalize the value to a range between 0 and 1
    normalized = (value - from_low) / (from_high - from_low)
    # Then, scale the normalized value to the target range
    mapped = normalized * (to_high - to_low) + to_low
    return mapped

#decode chromosome into input membership
def decodeInputMembership(val, chromosome,map1,map2,n_inputs):
    #normalize
    chrome = [map_value(C,0,n_inputs-1,map1,map2/n_inputs) for C in chromosome]
    
    #divide centers evenly
    C = np.linspace(map1,map2,n_inputs)

    #create triangles
    #TODO: put in loop
    x1 = triangular(val,C[0],           C[0], C[0]+chrome[0])
    x2 = triangular(val,C[1]-chrome[1], C[1], C[1]+chrome[2])
    x3 = triangular(val,C[2]-chrome[3], C[2], C[2]+chrome[4])
    x4 = triangular(val,C[3]-chrome[5], C[3], C[3]+chrome[6])
    x5 = triangular(val,C[4]-chrome[7], C[4], C[4])
    return [x1,x2,x3,x4,x5]

#decode chromosome into output membership
def decodeOutputMembership(chromosome,map1,map2,n_inputs=5):
    #normalize between 0 and .5
    chrome = [map_value(C,0,n_inputs-1,map1,map2/n_inputs) for C in chromosome]
    C = np.linspace(map1,map2,n_inputs)
    z1 = [C[0], C[0], C[0]+chrome[0]]
    z2 = [C[1]-chrome[1], C[1], C[1]+chrome[2]]
    z3 = [C[2]-chrome[3], C[2], C[2]+chrome[4]]
    z4 = [C[3]-chrome[5], C[3], C[3]+chrome[6]]
    z5 = [C[4]-chrome[7], C[4], C[4]]
    return [z1,z2,z3,z4,z5]

#decode rules from chromosome
def decodeRules(xs,ys,chromosome, n_rules=5):
    Mus = [[] for i in range(n_rules)]
    j = 0
    for i, x in enumerate(xs):
        for ii, y in enumerate(ys):
            Mus[chromosome[j]].append(min(x,y))
            j+=1
            
    return Mus

class Agent:
    def __init__(self):
        self.n_games = 0
        # self.epsilon = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.init_GA = False
        self.overshoot_error = 0

        #GA variables
        self.INT_MIN = 0
        self.INT_MAX = 4
        self.TOURNSIZE = 7
        self.POPULATION_SIZE = 8
        self.CXPB = 0.6
        self.MUTPB = 0.06
        self.N = 52
        self.game = SpaceRocks(user_input=False)
    
    def evalF(self,chromosome):
        while True:
            self.get_state()
            ship_final_move, peach_final_move = self.FIS(chromosome)
            agent.game.play_step(ship_final_move, peach_final_move)
            # cost = self.overshoot_error/1000 + self.game_time/120
            cost =  self.overshoot_error/2000*self.v + self.game_time/120

            # if self.game_time %100==0:
            #     print(self.game_time)

            if self.game.RESET == True:
                break
        if self.game.current_life == self.game.START_CAPTURE_LIFE:
            cost = cost*200 + self.relative_states[0]
        # print(f'Current Cost: {cost}')
        return cost,

    def get_state(self):

        #peach states
        x1 = self.game.peach.position[0]
        y1 = self.game.peach.position[1]
        u1 = self.game.peach.velocity[0]
        v1 = self.game.peach.velocity[1]

        #adjust heading to make sense
        heading = math.atan2(self.game.peach.direction[0],self.game.peach.direction[1])
        heading2 = math.atan2(self.game.peach.direction[0],self.game.peach.direction[1])
        if 0 < heading >= np.pi/2:
            heading = heading - np.pi/2
        elif heading < 0:
            heading = heading + 2*np.pi - np.pi/2
        else:
            heading = heading + 3*np.pi/2

        xa = [i.position[0] for i in self.game.asteroids]
        ya = [i.position[1] for i in self.game.asteroids]
        ua = [i.velocity[0] for i in self.game.asteroids]
        va = [i.velocity[1] for i in self.game.asteroids]

        # target states
        xt = self.game.target.position[0]
        yt = self.game.target.position[1]

        self.states = [x1,   #peach x position
                  y1,   #peach y position
                  u1,   #peach x velocity
                  v1,   #peach y velocity
                  xa,   #list of asteroid x positions
                  ya,   #list of asteroid y positions
                  ua,   #list of asteroid x velocities
                  va,   #list of asteroid y velocities
                  xt,   #target x position
                  yt]   #target y position
        
        # Calculate relative position of peach with respect to target
        dx_peach_target = xt - x1
        dy_peach_target = yt - y1

        # Calculate magnitude and angle of relative position of peach with respect to target
        position_error = math.sqrt(dx_peach_target**2 + dy_peach_target**2)
        angle_peach_target = math.atan2(-dy_peach_target, dx_peach_target)
        angle_peach_target2 = angle_peach_target
        if angle_peach_target < 0:
            angle_peach_target += 2*np.pi
        if angle_peach_target2 > 0:
            angle_peach_target2 -= 2*np.pi
        
        heading_error = (angle_peach_target - heading)

        if (heading_error) < -np.pi:
            heading_error = heading_error + 2*np.pi
        elif heading_error > np.pi:
            heading_error = heading_error - 2*np.pi


        # Calculate relative position of peach with respect to asteroids
        relative_positions_asteroids = []
        for asteroid_x, asteroid_y in zip(xa, ya):
            dx_peach_asteroid = asteroid_x - x1
            dy_peach_asteroid = asteroid_y - y1
            magnitude_peach_asteroid = math.sqrt(dx_peach_asteroid**2 + dy_peach_asteroid**2)
            angle_peach_asteroid = math.atan2(dy_peach_asteroid, dx_peach_asteroid)
            relative_positions_asteroids.append((magnitude_peach_asteroid, angle_peach_asteroid))        

        self.relative_states = [position_error, angle_peach_target, relative_positions_asteroids, heading_error]
        
        self.game_time = self.game.ticks
        # print(self.self.game_time)
        if self.game.current_life < self.game.START_CAPTURE_LIFE:
            self.overshoot_error += position_error
        else:
            self.game_time = self.game.ticks
        return

    def train_short(self):
        if not self.init_GA:
            self.g = 0
            #Implement GA to minimize evalF using  DEAP library
            #Create fitness  object
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            #create individual object
            creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

            #Initialize toolbox
            self.toolbox = base.Toolbox()
            self.toolbox.register("attr_int", random.randint, self.INT_MIN, self.INT_MAX)
            self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_int, n=52)
            self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
            self.toolbox.register("mate", tools.cxPartialyMatched)
            # Register mutation operator in the self.toolbox
            self.toolbox.register("mutate", tools.mutUniformInt, low=self.INT_MIN, up=self.INT_MAX, indpb=.1)
            # self.toolbox.register("select", tools.selTournament, tournsize=self.TOURNSIZE)
            self.toolbox.register("select", tools.selBest)
            # self.toolbox.register("select", tools.selRoulette)
            self.toolbox.register("evaluate", self.evalF)

            self.stats = tools.Statistics(key=lambda ind: ind.fitness.values)
            self.stats.register("avg", np.mean)
            self.stats.register("std", np.std)
            self.stats.register("min", np.min)
            self.stats.register("max", np.max)

            #set population size
            self.pop = self.toolbox.population(self.POPULATION_SIZE)
        
            #Define hof to capture best individual in population
            self.hof = tools.HallOfFame(1)

            self.init_GA = True
        else:
            start_gen = time.perf_counter()
            algorithms.eaSimple(self.pop, self.toolbox, self.CXPB, self.MUTPB, 1, halloffame=self.hof, verbose=False, stats=self.stats)
            end_gen = time.perf_counter()
            best_individual = tools.selBest(self.pop, k=1)[0]
            best_cost = self.evalF(self.hof[0])[0]
            print('\n\n')
            print(f'generation time: {abs(start_gen-end_gen)}')
            print("GENERATION: ", self.g+1)
            print(f'Best Indiviudal:{best_individual}')
            print(f'best cost: {best_cost}')
            print('\n\n')

            self.g += 1

            write_generation_cost(self.g, best_cost)

    def FIS(self, chromosome):

        #Lets get fizzy
        he = self.relative_states[3]
        pe = self.relative_states[0]
        v = (self.states[2]**2 + self.states[3]**2)**.5
        self.v = v

        #Input 1: Heading error
        he1 = right_shoulder(he,0,0)
        he2 = left_shoulder(he,0,0)
        hes = [he1,he2]
        
        #Input 2: Position error
        pes = decodeInputMembership(pe,chromosome=chromosome[0:8],map1=0,map2=2203,n_inputs=5)

        #input 3: velocity
        vs = decodeInputMembership(v,chromosome=chromosome[9:17],map1=-0.01,map2=2.5,n_inputs=5)

        #Rule base
        #Starting
        Mu1 = he1   #if angle negative go clockWise
        Mu2 = he2   #if angle positive go counterWise
        Mus = [[Mu1,Mu2]]

        #rule base for output 2 velocity
        Muvs = decodeRules(pes, vs, (chromosome[18:43]))   

        #outputs
        O1 = [-1,-.1,0]
        O2 = [0,.1,1]
        Os = [O1,O2]

        #output 2: velocity
        Ovs = decodeOutputMembership(chromosome=chromosome[44:52],map1=0,map2=2.5,n_inputs=5)

        #output 1 direction
        # Inference using Scaled Output Approach
        Areas = [[]]
        for i in range(len(Mus)):
            for ii,Mu in enumerate(Mus[i]):
                Areas[i].append(.5*Mu*(Os[i][2] - Os[i][0]))
        unionAreas = sum_list_of_lists(Areas)
        Y = 0
        for i, Area in enumerate(Areas):
            for ii in range(len(Area)):
                Y += np.array(Areas[i][ii])*Os[ii][1]
        Y = np.sum(Y/unionAreas)

        #output 2: velocity
        # Inference using Scaled Output Approach
        Areas = [[] for _ in range(len(Muvs))]
        for i in range(len(Muvs)):
            for ii,Muv in enumerate(Muvs[i]):
                Areas[i].append(.5*Muv*(Ovs[i][2] - Ovs[i][0]))
        unionAreas = sum_list_of_lists(Areas)

        Y2 = 0
        for i, Area in enumerate(Areas):
            for ii in range(len(Area)):
                Y2 += np.array(Areas[i][ii])*Ovs[i][1]
        Y2 = np.sum(Y2/unionAreas)
        if np.isnan(Y2):
            pass

        angle = 'counterWise' if Y > 0 else "clockWise"
        move = 'accelerate' if Y2 > v else 'not'

        return ["shooting",'clockWise','accelerate'], [move,angle]    

def play():
    agent = Agent()
    while True:
        #get old state
        agent.get_state()

        chromosome = [3, 3, 4, 3, 4, 1, 2, 3, 1, 2, 4, 0, 3, 0, 4, 2, 3, 3, 1, 0, 4, 0, 3, 1, 3, 4, 0, 4, 4, 1, 0, 4, 3, 4, 2, 3, 1, 2, 2, 3, 4, 2, 2, 3, 3, 4, 2, 1, 0, 0, 2, 1]
        #get move
        ship_final_move, peach_final_move = agent.FIS(chromosome)

        agent.game.play_step(ship_final_move, peach_final_move)

if __name__ == '__main__':
    # agent = Agent()
    # while True:
    #     agent.train_short()
    play()