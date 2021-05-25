from tradingview_ta import *
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob
import re
import string
import time

MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
TA_BUY_THRESHOLD = 18 # How many of the 26 indicators to indicate a buy
PAIR_WITH = 'USDT'
TICKERS = 'signalsample.txt'
TIME_TO_WAIT = 4 # Minutes to wait between analysis
FULL_LOG = False # List anylysis result to console

def analyze(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = []
    first_analysis = {}
    second_analysis = {}
   
    if os.path.exists('signals/signalsample.exs'):
        os.remove('signals/signalsample.exs')
          
    try:
        first_analysis = get_multiple_analysis(MY_SCREENER, MY_FIRST_INTERVAL, pairs)
        second_analysis = get_multiple_analysis(MY_SCREENER, MY_SECOND_INTERVAL, pairs)
    except Exception as e:
        print("Exeption:")
        print(e)
        print (pairs)
        exit()
    for coin in pairs:        
        first_tacheck = first_analysis[coin].summary['BUY']
        second_tacheck = second_analysis[coin].summary['BUY']
        if FULL_LOG: print (f'Coin:{coin} TA1: {first_tacheck} TA2: {second_tacheck}')
        if first_tacheck > taMax:
            taMax = first_tacheck
            taMaxCoin = coin.replace(MY_EXCHANGE + ':','')

        if first_tacheck > TA_BUY_THRESHOLD and second_tacheck > TA_BUY_THRESHOLD:
            signal_coins.append(coin.replace(MY_EXCHANGE + ':',''))

    print(f'Max signal by {taMaxCoin} at {taMax} on shortest timeframe')
    return signal_coins

def do_work():
    signal_coins = []
    pairs = {}

    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[MY_EXCHANGE + ':' + line.strip() + PAIR_WITH for line in open(TICKERS)] 
    
    while True:
        print(f'Analyzing {len(pairs)} coins')
        signal_coins = analyze(pairs)
        if len(signal_coins) > 0:
            print(f'Signal detected on {signal_coins}')
            with open('signals/signalsample.exs','a+') as f:
                for pair in signal_coins:
                    f.write(pair + '\n')
            print(f'{len(signal_coins)} coins above {TA_BUY_THRESHOLD} treshold on both timeframes')
        else:
            print(f'No coins above {TA_BUY_THRESHOLD} threshold')
             
        print(f'Waiting {TIME_TO_WAIT} minutes for next analysis')
        time.sleep((TIME_TO_WAIT*60))
