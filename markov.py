import matplotlib.pyplot as plt
import pandas as pd
import pprint
import random
from contextlib import redirect_stdout
from math import sqrt
import numpy as np


# fuck so many iterations. trial and error fuck sakes. 

class Markovchain():
    def __init__(self, data):
        self.data = data
        self.changes = []
        self.ngram_frequency = {}
        self.std = 0

        self.transition_state = np.array([[1/43, 2/43, 12/43, 0, 13/43, 5/43, 10/43],
                                [5/52, 8/52, 13/52, 0, 16/52, 8/52, 2/52],
                                [12/475, 16/475, 177/475, 2/475, 216/475, 40/475, 12/475],
                                [0, 0, 4/7, 0, 2/7, 1/7, 0],
                                [16/536, 13/536, 214/536, 5/536, 251/536, 26/536, 11/536],
                                [2/97, 5/97, 40/97, 0, 32/97, 12/97, 6/97],
                                [7/47, 8/47, 16/47, 0, 5/47, 5/47, 6/47]])
        self.start_state = np.array([0, 0, 0, 0, 1, 0, 0])

    def calc_state(self, n):
        if n < -2*self.std:
            return "s1"
        if -2*self.std <= n < -1*self.std:
            return "s2"
        if -1*self.std <= n < 0:
            return "s3"
        if n == 0:
            return "s4"
        if 0 < n <= self.std:
            return "s5"
        if self.std < n <= 2*self.std:
            return "s6"
        if 2*self.std < n:
            return "s7"

        

    def update(self):
        self.generate_ngrams()

        # single_change = list(set(self.changes))

        # for i in range(len(single_change) - 1):
        #     state = (single_change[i], single_change[i+1])
        #     self.ngram_frequency[state] = {}

        self.std = sqrt(self.calc_var())
        for i in range(len(self.changes) - 1):
  
            state = self.calc_state(self.changes[i])
            next = self.calc_state(self.changes[i+1])

            if state not in self.ngram_frequency.keys():
                self.ngram_frequency[state] = {}
            
            if next not in self.ngram_frequency[state]:
                self.ngram_frequency[state][next] = 1 
            else: 
                self.ngram_frequency[state][next] += 1

        # print(len(self.changes))
        with open('results/out.txt', 'w') as f:
            with redirect_stdout(f):
                for i in range(250):
                    self.dot_product_matrix()
                
                    print(self.start_state)

        # with open('out.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         pprint.pprint(self.ngram_frequency)
    
        # out = {}
        # for state in self.ngram_frequency.keys():
        #     out[state] = {}
        #     for next in self.ngram_frequency[state].keys():
        #         out[state][next] = self.get_prob(state, next)


        # with open('/results/out1.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         pprint.pprint(out)


        # freq = dict(sorted(self.ngram_frequency.items(), key=lambda x: float(x[0]), reverse=False))
        # with open('graph.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         for i in self.changes:
        #             print(i)

        
        # with open('plot.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         tmp = []
        #         for i in range(5):
        #             start_state = (self.changes[len(self.changes)-1])
        #             output = []
        #             for j in range(50):
        #                 start_state = self.next_price(start_state)
        #                 output.append(start_state)
                        
        #                 # start_state = 0.11
        #                 # p # for i in range(7):
        #     for j in range(7):
        #         current_transition_state = []
        context_counter = self.ngram_frequency[state][next]
        sum_token_counter = sum(self.ngram_frequency[state].values())
            
        return(context_counter / sum_token_counter)
#

    def generate_ngrams(self):
        i = 0
        prev = 0
        cur = 0

        for index, row in self.data.iterrows():
            # print(row['Close'])
            if i == 0:
                prev = row['Close']
                
            else:
                cur = row['Close']
                change = cur - prev
                
                change = float("{:.2f}".format(change))
                # change = int(change)
                self.changes.append(change) 
                
                prev = cur      
                
            i+= 1

    def next_price(self, state):
        ngram_prob_density = {}
        sum_token_counter = sum(self.ngram_frequency[state].values())

        for next in self.ngram_frequency[state].keys():
            next_counter = self.ngram_frequency[state][next]
            ngram_prob_density[next] = next_counter / sum_token_counter

        # ngram_prob_density = dict(sorted(ngram_prob_density.items(), key=lambda x: x[0], reverse=True))
        # pprint.pprint(ngram_prob_density)

        # sort by values
        ngram_prob_density = sorted(ngram_prob_density.items(), key=lambda x: float(x[1]), reverse=True)
        # print(ngram_prob_density)
        top_ngram = ngram_prob_density[:1]
        
        ngram_prob_density = dict(ngram_prob_density)
        
  
        # did'nt know you can do this fucking black magic shit.
        # cant be fucked fixing code infront. I am a c programmer. just habits
        same_prob = []
        same_prob.append(top_ngram[0][0])

        for next in ngram_prob_density:
            if top_ngram[0][0] is not next:
                if(top_ngram[0][1] == ngram_prob_density[next]):
                    same_prob.append(next)


        if len(same_prob) == 1:
            return same_prob[0]
        else:
            # if have same prob. return random. can cause butterfly effect is predicting a chain of events.
            return random.choice(same_prob) 

    def calc_mean(self):
        sum = 0
        for x in self.changes:
            sum += x
        return sum / len(self.changes)

    def calc_var(self):
        sum = 0
        mean = self.calc_mean()
        for i in self.changes:
            sum +=  pow((i - mean), 2)
            
        return sum / len(self.changes)


    def dot_product_matrix(self):
        # for i in range(7):
        #     for j in range(7):
        #         current_transition_state = []
        self.start_state = np.dot(self.start_state, self.transition_state)

        # self.transition_state = current_transition_state
        




