from markov import Markovchain

import yfinance as yf

from markov import Markovchain

def main():
    data = yf.download('AAPL', '2000-01-01', '2020-01-01')
    model = Markovchain(data)
    model.update()

    

if __name__ == "__main__":
    main()