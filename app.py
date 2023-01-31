from flask import Flask, request, jsonify, redirect, render_template
import requests
from bs4 import BeautifulSoup
import config
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
import re
import perfcounters
from utils import GetDataFromChartink, send_telegram



app = Flask(__name__)
urls = ['https://chartink.com/screener/potential-movers-2','https://chartink.com/screener/bullish-engulfing-pattern-25122702','https://chartink.com/screener/morning-star-candlestick-pattern-423','https://chartink.com/screener/evening-star-2540','https://chartink.com/screener/bearish-engulfing-pattern-209']
patterns = ["Potential Movers", "Bullish Engulfing", "Morning Star", "Evening Star", "Bearish Engulfing"]

@app.route("/", methods=["GET"])
def scrape(): 
    
    scr = perfcounters.PerfCounters()
    scr.start('scrape') 
    dataframes = {}
    count = 0
    for url in urls:
      #st = get_stocks(url,driver)
      st = GetDataFromChartink(url)
      

      # split the string by '/'
      parts = url.split('/')

      # get the last part of the split string, which is 'potential-movers-2'
      last_part = parts[-1]

      # split the last part by '-'
      parts = last_part.split('-')

      # remove the last part, which is the number '2'
      parts.pop()

      # join the parts with ' '
      result = ' '.join(parts)

      # convert to title case
      result = result.title()
      if len(st) <=1:
        send_telegram(result + "\n No stocks found")
      else:
        send_telegram(result)
        
      
      if (st.empty == False) and len(st)>1:
          
          df =pd.DataFrame(st,columns=['Sr.no','Name','Symbol','Links','%CH','Price','Vol'])
          send_telegram(df['Symbol'].to_string(index=False))
                   
          feature = ['Name','Symbol','%CH','Price']
          df = df[feature]
          dataframes[result] = df
          #df = df.assign(Label=result)          
          
        
    scr.stop('scrape')
    scr.report()
    
    return render_template('index.html',pattern_list = patterns,my_dict=dataframes)   
    

if __name__ == "__main__":
    app.run()