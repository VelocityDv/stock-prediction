from markov import Markovchain
import pandas as pd
import yfinance as yf

from markov import Markovchain

def main():
    data = yf.download('AAPL', '2016-12-31', '2022-01-01')
    model = Markovchain(data)
    model.update()
    # print(model.calc_mean())
    # print(model.calc_var())
    
    # compare_data = yf.download('AAPL', '2022-12-31', '2020-02-14')
    # compare_data = yf.download('AAPL', '2020-12-31', '2021-02-15')
    # compare_data = yf.download('AAPL', '2022-01-08', '2022-01-15')
    # print(compare_data.head())
    # compare = []

    # i = 0
    # prev = 0
    # cur = 0

    # for index, row in compare_data.iterrows():
    #     # print(row['Close'])
    #     if i == 0:
    #         prev = row['Close']
            
    #     else:
    #         cur = row['Close']
    #         change = cur - prev
            
    #         change = float("{:.2f}".format(change))
    #         # change = int(change)
    #         compare.append(change) 
            
    #         prev = cur      
            
    #     i+= 1

    # print(compare)
    # print(len(compare))

    

if __name__ == "__main__":
    main()