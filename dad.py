import os
import time
import threading
import random
from colorama import init
init()
class txcolors:
    WARNING = '\033[93m'
    DEFAULT = '\033[39m'
    
INTERVAL = 2 #Timeframe for text
TEXT_FILE = 'dad.txt'

#if __name__ == '__main__':
def do_work():
    random.seed
    texts=[line.strip() for line in open(TEXT_FILE)]
      
    while True:
        if not threading.main_thread().is_alive(): exit()
        time.sleep((INTERVAL*60))
        print(f'{txcolors.WARNING}{texts[random.randrange(0, len(texts))]}{txcolors.DEFAULT}')
