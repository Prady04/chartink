from zipfile import ZipFile
from io import BytesIO
import requests
import time
import datetime
import re
import os
import sys
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
from pathlib import Path


def process_bhav(y, z):

  startDate = datetime.datetime.strptime(y, "%Y-%m-%d")

  if z == '':
	  endDate = startDate
  else:
	  endDate = datetime.datetime.strptime(z, "%Y-%m-%d")

  curDate = startDate

  # Bhavcopy data downloaded here
  while curDate <= endDate:
 
    eq = 'https://archives.nseindia.com/content/historical/EQUITIES/'+curDate.strftime(
        "%Y")+"/"+curDate.strftime("%b").upper()+"/cm"+curDate.strftime("%d%b%Y").upper()+"bhav.csv.zip"
    # Expected Bhavcopy link format: 'https://www.nseindia.com/content/historical/EQUITIES/2015/NOV/cm24NOV2015bhav.csv.zip'

    idx = 'https://www1.nseindia.com/content/indices/ind_close_all_' + \
        curDate.strftime("%d%m%Y") + '.csv'
    # Expected link for index download: https://www1.nseindia.com/content/indices/ind_close_all_22022016.csv
    try:
      res_eq = requests.get(eq, timeout=1)			# Equity data
      res_idx = requests.get(idx, timeout=1)		# Index data
    except Exception as e: 
      curDate+= datetime.timedelta(days=1)
      continue
    outfile_eq = 'C:\\Tradedb\\'+curDate.strftime("%d%m%Y")+'_NSE.txt'
    outfile_idx = 'C:\\Tradedb\\' + curDate.strftime("%d%m%Y")+'I_NSE.txt'
  

    filename = Path(outfile_eq)
    filename.touch(exist_ok=True)
    filename = Path(outfile_idx)
    filename.touch(exist_ok=True) 
    
    if res_eq.ok:
		  # read the string output from the output by previous step
      zipped_eq = ZipFile(BytesIO(res_eq.content), "r")
      print('read done')
		  # unzip and read the file content
      data_eq = zipped_eq.read(zipped_eq.namelist()[0])
      
		  # split end of line variable creates rows of securities
      x_eq = data_eq.decode().split("\n")
      
      with open(outfile_eq, 'w+') as f:
        for x1 in x_eq[1:-1]:
          # separated at comma values giving individual data points
          x1 = x1.split(",")
          if x1[1] == "EQ":
            f.write(x1[0] +',' + curDate.strftime("%d-%b-%Y") + "," + x1[2] + "," +
					          x1[3] + "," + x1[4] + "," + x1[5] + "," + x1[8] + "\n")
        f.close()
      print('Bhavcopy for '+curDate.strftime("%d-%b-%Y")+' downloaded')
      time.sleep(1)
      data_idx = res_idx.content									#read the file content - This is not zipped
      
      x_idx = data_idx.decode().split("\n")							#split end of line variable creates rows of securities
      with open(outfile_idx, 'w+') as f:
        for x2 in x_idx[1:-1]:
          x2 = x2.split(",")						#separated at comma values giving individual data points
          f.write(x2[0].replace(' ','')+','  + curDate.strftime("%d-%b-%Y") + "," + x2[2] + "," + x2[3] + "," + x2[4] + "," + x2[5] + "," + x2[8]+  "\n")
        print('Index details for '+curDate.strftime("%d-%b-%Y")+' downloaded')
						
      curDate+= datetime.timedelta(days=1)
    else:
      print('No Bhavcopy available for '+curDate.strftime("%d-%b-%Y"))
    

  