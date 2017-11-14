import numpy as np
import networkx as nx
import pandas as pd
import csv

class SZRmodel(object):
    
        ######################################
        # Main class of the simulation.      #
        # contains all essential information # 
        # to run the simulation.             #
        ######################################
        

        
        #The initializer takes a networkx object as a topology
        #and iniatializes the model at t = 0
        
        def __init__(self,topology,Znumber=1,kill_prob=0.3,inf_prob = 0.5):
            
            assert type(topology) is nx.classes.graph.Graph
            assert type(Znumber) is int
            #Probabilities of interactions
            self.kill_prob = kill_prob
            self.inf_prob = inf_prob
            assert self.kill_prob+self.inf_prob <= 1
            
            self.G = topology
            self.N = self.G.number_of_nodes()
            self.states = np.zeros(self.N)
            init_zombies =  np.random.choice(self.G.number_of_nodes(),Znumber)
            self.states[init_zombies] = 1 #SETTING ZOMBIE NODES TO STATE = 1
            self.edges = np.array(self.G.edges())
            self.df=pd.DataFrame()#creates empty dataframe

        def step(self):
            # G.size() returns number of EDGES! 
            link = int(np.random.choice(np.array(self.G.size()),1))
            #link is a randomly chosen edge
            #we check the states of the nodes on each side of link
            agent1 = self.edges[link,0]
            agent2 = self.edges[link,1]
            state1 = self.states[agent1]
            state2 = self.states[agent2]
            #In order for the states to interact one has to be human, state = 0
            #and the other has to be a zombie state = 1
            #so it is sufficient to check if state1+state2 == 1
            
            if (state1 + state2 == 1): 
                #now we have to distinguish between them
                if state1 == 0:
                    human = agent1
                    zombie = agent2
                else:
                    human = agent2
                    zombie = agent1
                roll = np.random.uniform()
                if roll < self.kill_prob: 
                    #Human wins
                    #Z --> R
                    self.states[zombie] = 2
                elif roll < self.kill_prob + self.inf_prob:
                    #Zombie wins
                    #H --> Z
                    self.states[human] = 1         
        def run(self):
            num=10000
            for i in range(num):
                self.step()
                if(i%100==0):
                    df_state = pd.DataFrame(self.states)
                    print(self.states)
                    # stores states in dataFrame
                    self.df = pd.concat([self.df, df_state], axis=1)
                    if i==num-1:
                        self.df.to_csv('nick.csv')

