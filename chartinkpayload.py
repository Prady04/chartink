from time import sleep
import os
import warnings
import sys
warnings.filterwarnings("ignore")

import xlwings as xw
import requests


import pandas as pd
from bs4 import BeautifulSoup

import utils
import winsound

from rich_dataframe import prettify


    
    

Charting_url = 'https://chartink.com/screener/process'

#You need to copy paste condition in below mentioned Condition variable

conditions = {"bullrun":"( {-1} ( [0] 5 minute close > 1 day ago high and latest low > 1 day ago close and latest open > 1 day ago close and latest volume > latest sma ( latest volume , 20 ) * 1.2 and 1 day ago open > 1 day ago close and 1 day ago close > 1 day ago low * 0.95 and latest volume > 100000 ) )  ", "bullEng": "( {cash} ( [-1] 15 minute close > [-1] 15 minute open and [-2] 15 minute open > [-2] 15 minute close and [-1] 15 minute open < [-2] 15 minute close and [-1] 15 minute close > [-2] 15 minute open and latest volume > 50000 and [0] 15 minute high > [-1] 15 minute high ) )  " }

sleeptime = 60





try:
    if not os.path.exists('Chartink_Result.xlsm'):
        wb = xw.Book()
        wb.save('Chartink_Result.xlsm')
        wb.close()

    wb = xw.Book('Chartink_Result.xlsm')
    try:
        result = wb.sheets('Chartink_Result')
    except Exception as e:
        wb.sheets.add('Chartink_Result')
        result = wb.sheets('Chartink_Result')
except Exception as e:
    pass
stocks = None    
while True:
    
    for name, condition in conditions.items():
    
      data = utils.GetDataFromChartink(condition)
      if (data.empty):
        print("nothing found...")
      else:        
        data = data.sort_values(by='per_chg',ascending=False)
        prettify(data, clear_console=True) #print(f"\n\n{data}")
        print(name)
        winsound.Beep(440, 500)
        
        
        
        
      
        try:
            result.range('a:h').value = None
            result.range('a1').options(index=False).value = data
        except Exception as e:
          pass
      print(f'scanning again in {sleeptime * 7/60} minutes')
    sleep(sleeptime *7)
        