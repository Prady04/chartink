from flask import Flask, request, jsonify, redirect, render_template, make_response
import requests

import config
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
import re
import perfcounters
from utils import GetDataFromChartink
from datetime import datetime,date



app = Flask(__name__)
last_execution = None


def get_from_cache():
    return None, None, None


def save_to_cache(today, df, stocks):
    return 0

@app.context_processor
def inject_template_globals():
    return {
        'now': datetime.now(),
        'isIndex':False,
    }
    
    
@app.route('/')
def index():
        
    return render_template('dashboard.html', isIndex=True)

@app.route("/eod", methods=["GET"])
def scrape(): 
    global last_execution    
    today = date.today()    
    scr = perfcounters.PerfCounters()
    scr.start('scrape') 
    dataframes = {}
    stocks = []
    last_execution,cdataframes, cstocks = get_from_cache()
    if last_execution == today:
        return render_template('index.html', dt = datetime.now().strftime("%d-%m-%Y"), dict = cdataframes,stocks=cstocks)
    else:
        queries = config.eod_queries.items()        
        for key, val in queries:        
            data = GetDataFromChartink(val)        
            if (data.empty == False) and len(data)>1:                
                data.drop(columns=['sr','name','bsecode'],inplace=True)
                data.rename(columns= {"nsecode":"symbol"},inplace=True)
                data.rename(columns= {"per_chg":"%change"},inplace=True)                
                stocks.append(data['symbol'].to_string())
                dataframes[key] = data 
          
        scr.stop('scrape')
        scr.report()
    
        save_to_cache(date.today(),dataframes, stocks)
        resp= render_template('index.html', dt = datetime.now().strftime("%d-%m-%Y"), dict = dataframes,stocks=stocks)
        return(resp)

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
    message = ""
    
    #stocks.sort_values(by=['per_chng'], inplace=True)
    print(queries.items())
    try:
        key, stocks = processdata(queries)
    except Exception as e:
        print(e)
        pass
    print(stocks)
    if stocks.empty:
        message = 'No stocks found'               
         
    return(render_template('new.html',pattern = key, stocks = stocks, message = message)) 

@app.route('/investment')
def investment():        
    return(render_template('investment.html'))

@app.route('/swing')
def swing(): 
    stocks =['ZYDUSLIFE','GENCON','DATAPATTNS','UTIAMC','BRITTANIA','JSL']
    dat = "14-MAR-2023"  
    message = "*** market breadth - extreme bearish => prefer reversal trades *****"   
    return(render_template('swing.html', stocks = stocks, dat=dat, message = message))
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