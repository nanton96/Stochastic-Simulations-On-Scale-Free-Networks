
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

class SZRmodel(object):
    
        ######################################
        # Main class of the simulation.      #
        # contains all essential information # 
        # to run the simulation.             #
        ######################################
        
        #Probabilities of interactions are defined as class variables
        
        kill_prob = 0.3
        inf_prob = 0.2
        assert kill_prob+inf_prob <= 1
        
        #The initializer takes a networkx object as a topology
        #and iniatializes the model at t = 0
        
        def __init__(self,topology,Znumber=1):
            
            assert type(topology) is nx.classes.graph.Graph
            assert type(Znumber) is int
            
            self.G = topology
            self.N = self.G.number_of_nodes()
            self.states = np.zeros([1,self.N])
            init_zombies =  np.random.choice(self.G.number_of_nodes(),Znumber)
            self.states[0,init_zombies] = 1 #SETTING ZOMBIE NODES TO STATE = 1
            self.edges = np.array(g.edges())
        
        def step(self):
            # G.size() returns number of EDGES! 
            link = int(np.random.choice(np.array(self.G.size()),1))
            #link is a randomly chosen edge
            #we check the states of the nodes on each side of link
            agent1 = self.edges[link,0]
            agent2 = self.edges[link,1]
            state1 = self.states[0,agent1]
            state2 = self.states[0,agent2]
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
                if roll < kill_prob: 
                    #Human wins
                    #Z --> R
                    self.states[0,zombie] = 2
                elif roll < kill_prob + inf_prob:
                    #Zombie wins
                    #H --> Z
                    self.states[0,human] = 1
                
        def run(self, niter = 10**6):
            i=0
            while (i < niter):
                self.step()
            #NEED TO SAVE DATA DURING THE SIMULATION
