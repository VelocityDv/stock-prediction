import matplotlib.pyplot as plt
import pandas as pd
import pprint
import random
from contextlib import redirect_stdout


# fuck so many iterations. trial and error fuck sakes. 

class Markovchain():
    def __init__(self, data):
        self.data = data
        self.changes = []
        self.ngram_frequency = {}

    def update(self):
        self.generate_ngrams()

        # single_change = list(set(self.changes))

        # for i in range(len(single_change) - 1):
        #     state = (single_change[i], single_change[i+1])
        #     self.ngram_frequency[state] = {}

        for i in range(len(self.changes) - 1):
            state = (self.changes[i])
            next = self.changes[i+1]

            if state not in self.ngram_frequency.keys():
                self.ngram_frequency[state] = {}
            
            if next not in self.ngram_frequency[state]:
                self.ngram_frequency[state][next] = 1 
            else: 
                self.ngram_frequency[state][next] += 1

        # print(len(set(self.changes)))
        # with open('out.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         pprint.pprint(self.ngram_frequency)
    
        # freq = dict(sorted(self.ngram_frequency.items(), key=lambda x: float(x[0]), reverse=False))

        
        with open('plot.txt', 'w') as f:
            with redirect_stdout(f):
                tmp = []
                for i in range(5):
                    start_state = (self.changes[len(self.changes)-1])
                    output = []
                    for j in range(50):
                        start_state = self.next_price(start_state)
                        output.append(start_state)
                        
                        # start_state = 0.11
                        # print(self.next_price(start_state))
                    tmp.append(output)
                print(tmp)


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