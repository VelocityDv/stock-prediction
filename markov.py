import matplotlib.pyplot as plt
import pandas as pd
import pprint

# dont need to optimize time.
# dont care since its for maths. ahhahahah :)

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

        for i in range(len(self.changes) - 2):
            state = (self.changes[i], self.changes[i+1])
            next = self.changes[i+2]

            if state not in self.ngram_frequency.keys():
                self.ngram_frequency[state] = {}
            
            if next not in self.ngram_frequency[state]:
                self.ngram_frequency[state][next] = 1 
            else: 
                self.ngram_frequency[state][next] += 1

          # freq = dict(sorted(self.ngram_frequency.items(), key=lambda x: float(x[0]), reverse=False))


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
                change = prev - cur
                
                change = float("{:.2f}".format(change))
                # change = int(change)
                self.changes.append(change) 
                
                prev = cur      
                
            i+= 1
        

    def get_prob(self):
        pprint.pprint(self.ngram_frequency)


    def next_price(self):
        pass


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