from flask import Flask, request, jsonify, redirect, render_template
import requests
from bs4 import BeautifulSoup
import config
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
import re
import perfcounters
from utils import GetDataFromChartink, send_telegram, send_telegram_img
import datetime as dt
import dataframe_image



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route("/test", methods=["GET"])
def scrape(): 
    
    scr = perfcounters.PerfCounters()
    scr.start('scrape') 
    dataframes = {}
    
    queries = config.eod_queries.items()
    i=1
    for key, val in queries:
      #st = get_stocks(url,driver)
      data = GetDataFromChartink(val)    
      send_telegram(key + "\n")
        
      
      if (data.empty == False) and len(data)>1:
         
          
          #print(data)
          data = data.sort_values(by='per_chg',ascending=False)
          data.drop(columns='sr',inplace=True)
          #data["timestap"] = dt.datetime().now().strftime('%H:%M:%S')
          df_styled = data.style.background_gradient()  
          dataframe_image.export(df_styled, f'{i}.png')
          dataframes[key] = data                
          send_telegram_img(f'{i}.png')
          i += 1
          
        
          #df = df.assign(Label=result)          
          
        
    scr.stop('scrape')
    scr.report()
  
      
    return render_template('index.html', dt = dt.datetime.now().strftime("%d-%m-%Y"), dict = dataframes)
  
  
@app.route('/bullrun')
def intraday():
    now = dt.datetime.now().time()
    time_string = now.strftime("%H:%M:%S")

    
    queries = config.bullrun
    print(queries.items())
    dataframes = {}
    for key, value in queries.items():
        data = GetDataFromChartink(value)
        #print(data)
        if (data.empty == False) and len(data)>0:
          
          #print(data)
          data = data.sort_values(by='per_chg',ascending=False)
          data.drop(columns=['sr', 'bsecode', "name", 'volume'],inplace=True)
          data["Time"]= time_string
          data.keys().append("Symbol")
         
          dataframes[key] = data
    return(render_template('intraday.html', dict = dataframes))  


@app.route('/bulle')
def bulle():
    now = dt.datetime.now().time()
    time_string = now.strftime("%H:%M:%S")


    queries = config.bullEng
    #print(queries.items())
    dataframes = {}
    for key, value in queries.items():
        data = GetDataFromChartink(value)
        
    if (data.empty == False) and len(data)>0:
        
        #print(data)
        data = data.sort_values(by='per_chg',ascending=False)
        data.drop(columns=['sr', 'bsecode', "name", 'volume'],inplace=True)
        data["Time"]= time_string
        
        dataframes[key] = data
    return(render_template('intraday.html', dict = dataframes))      


@app.route('/beare')
def beare():
    now = dt.datetime.now().time()
    time_string = now.strftime("%H:%M:%S")

    
    queries = config.bearEng
    print(queries.items())
    dataframes = {}
    for key, value in queries.items():
        data = GetDataFromChartink(value)
        print(data)
        if (data.empty == False) and len(data)>0:
          
          #print(data)
          data = data.sort_values(by='per_chg',ascending=False)
          data.drop(columns=['sr', 'bsecode', "name", 'volume'],inplace=True)
          data["Time"]= time_string
         
          dataframes[key] = data
    return(render_template('intraday.html', dict = dataframes))  


if __name__ == "__main__":
    app.run()