from flask import Flask, request, jsonify, redirect, render_template
import requests

import config
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
import re
import perfcounters
from utils import GetDataFromChartink, send_telegram, send_telegram_img
import datetime as dt
#from bhavutils import process_bhav 
#from amiutils import import_data 
  

app = Flask(__name__)



    
    
@app.route('/')
def index():
    return render_template('main.html')

@app.route("/eod", methods=["GET"])
def scrape(): 
    
    scr = perfcounters.PerfCounters()
    scr.start('scrape') 
    dataframes = {}
    stocks = []
    
    queries = config.eod_queries.items()
    i=1
    for key, val in queries:
      #st = get_stocks(url,driver)
        data = GetDataFromChartink(val)    
        send_telegram(key + "\n")
        
      
        if (data.empty == False) and len(data)>1:
         
          
          #print(data)
            
            data.drop(columns=['sr','name','bsecode'],inplace=True)
            data.rename(columns= {"nsecode":"symbol"},inplace=True)
            
            #data["timestap"] = dt.datetime().now().strftime('%H:%M:%S')
            #data = data.style.background_gradient()  
            #dataframe_image.export(data, f'C:\\temp\\{key}.png')
            stocks.append(data['symbol'].to_string())
            #data['symbol']= f'<a href="https://in.tradingview.com/chart/ONnfTdXs/?symbol={ym}&target="_blank"" >{ym}</a></td>'
            send_telegram(data['symbol'].to_string())
            dataframes[key] = data 
            
          
        
    scr.stop('scrape')
    scr.report()
    
      
    return render_template('index.html', dt = dt.datetime.now().strftime("%d-%m-%Y"), dict = dataframes,stocks=stocks)

def processdata(queries):
    for key, value in queries.items():
        data = GetDataFromChartink(value)
        #print(data)
        if (data.empty == False) and len(data)>0:          
          #print(data)
          data = data.sort_values(by='per_chg',ascending=False)
          data.drop(columns=['sr', 'bsecode', "name", 'volume'],inplace=True)        
        
    return(key, data)
      

@app.route('/bullrun')
def intraday():
    now = dt.datetime.now().time()
    time_string = now.strftime("%H:%M:%S")

    
    queries = config.bullrun
    stocks = pd.DataFrame()
    print(queries.items())
    key, stocks = processdata(queries)
                    
         
    return(render_template('intraday.html', pattern = key, stocks = stocks))  


@app.route('/bulle')
def bulle():
    now = dt.datetime.now().time()
    

    
    queries = config.bullEng
    stocks = pd.DataFrame()    
    key, stocks = processdata(queries)
    print(stocks)
                    
         
    return(render_template('intraday.html', pattern = key, stocks = stocks))     


@app.route('/beare')
def beare():
    now = dt.datetime.now().time()
    queries = config.bearEng
    stocks = pd.DataFrame()
    print(queries.items())
    try:
        key, stocks = processdata(queries)
    except Exception as e:
        pass
    print(stocks)               
         
    return(render_template('intraday.html', pattern = key, stocks = stocks))  

@app.route('/new')
def new(): 
    print("in new")
    queries = config.new
    stocks = pd.DataFrame()
    key = ""
    
    
    #stocks.sort_values(by=['per_chng'], inplace=True)
    print(queries.items())
    try:
        key, stocks = processdata(queries)
    except Exception as e:
        pass
    print(stocks)               
         
    return(render_template('new.html',pattern = key, stocks = stocks)) 
''' 
@app.route('/bhav', methods=['GET','POST'])  
def bhav():
    if request.method=='POST':
        print(request.form.items())
        start_date = request.form.get('startdate')
        end_date = request.form['enddate']
        process_bhav(start_date, end_date)
        import_data()
        return "Data imported to AmiBroker"
    if request.method=="GET":
        return(render_template('dlbhav.html'))
'''
if __name__ == "__main__":
    app.run()