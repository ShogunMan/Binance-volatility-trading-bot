# Available indicators here: https://python-tradingview-ta.readthedocs.io/en/latest/usage.html#retrieving-the-analysis

from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
import time
import threading

from tradingview_ta.main import get_multiple_analysis

OSC_INDICATORS = ['MACD', 'Stoch.RSI', 'Mom'] # Indicators to use in Oscillator analysis
OSC_THRESHOLD = 2 # Must be less or equal to number of items in OSC_INDICATORS 
MA_INDICATORS = ['EMA10', 'EMA20'] # Indicators to use in Moving averages analysis
MA_THRESHOLD = 2 # Must be less or equal to number of items in MA_INDICATORS 
INTERVAL = Interval.INTERVAL_5_MINUTES #Timeframe for analysis

EXCHANGE = 'BINANCE'
SCREENER = 'CRYPTO'
PAIR_WITH = 'USDT'
TICKERS = 'signalsample.txt'
TIME_TO_WAIT = 4 # Minutes to wait between analysis
FULL_LOG = False # List analysis result to console

def analyze(pairs):
    signal_coins = []
    analysis = {}
       
    if os.path.exists('signals/custsignalmod.exs'):
        os.remove('signals/custsignalmod.exs')

    try:
        analysis = get_multiple_analysis(SCREENER, INTERVAL, pairs)
    except Exception as e:
        print("Exception:")
        print(e)

    for coin in pairs:
        oscCheck=0
        maCheck=0
        for indicator in OSC_INDICATORS:
            if analysis[coin].oscillators ['COMPUTE'][indicator] == 'BUY': oscCheck +=1
      	
        for indicator in MA_INDICATORS:
            if analysis[coin].moving_averages ['COMPUTE'][indicator] == 'BUY': maCheck +=1		

        if FULL_LOG:
            print(f'Custsignalmod:{coin} Oscillators:{oscCheck}/{len(OSC_INDICATORS)} Moving averages:{maCheck}/{len(MA_INDICATORS)}')
        
        if oscCheck >= OSC_THRESHOLD and maCheck >= MA_THRESHOLD:
            signal_coins.append(coin.replace(EXCHANGE + ':',''))
  
    return signal_coins

def do_work():
    signal_coins = []
    pairs = {}

    pairs=[line.strip() for line in open(TICKERS)]
    for line in open(TICKERS):
        pairs=[EXCHANGE + ':' + line.strip() + PAIR_WITH for line in open(TICKERS)]
    
    while True:
        if not threading.main_thread().is_alive(): exit()
        print(f'Custsignalmod: Analyzing {len(pairs)} coins')
        signal_coins = analyze(pairs)
        if len(signal_coins) > 0:
            print(f'Signal detected on {signal_coins}')
            with open('signals/custsignalmod.exs','a+') as f:
                for pair in signal_coins:
                    f.write(pair + '\n')
        
        print(f'{len(signal_coins)} coins above {OSC_THRESHOLD}/{len(OSC_INDICATORS)} oscillators and {MA_THRESHOLD}/{len(MA_INDICATORS)} moving averages Waiting {TIME_TO_WAIT} minutes for next analysis.')
        
        time.sleep((TIME_TO_WAIT*60))
